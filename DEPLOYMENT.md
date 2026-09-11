# Deploying to AWS EC2 (t3.micro, free tier) with systemd

Files referenced below live in `deploy/`:
- `rag-pipeline.service` - systemd unit
- `rag-pipeline.env.example` - template for the secrets file
- `provision_ec2.sh` - automates steps 3-8 below
- `backup_chroma_to_s3.sh` - optional off-instance backup of the Chroma DB

## 1. Launch the instance

- AMI: Amazon Linux 2023 (free tier eligible)
- Instance type: `t3.micro` (1 GB RAM, 2 vCPU burstable)
- Storage: default 8 GB gp3 root volume is fine (free tier covers up to 30 GB)
- Security group:
  - SSH (22) - restrict to your IP, not `0.0.0.0/0`
  - Custom TCP 8000 - only from IPs/CIDRs that should reach the API (the Anthropic API calls this triggers cost money per request - don't leave it open to the world)
- Key pair: create or reuse one for SSH access

## 2. Add swap (t3.micro only has 1 GB RAM)

`sentence-transformers` + its PyTorch dependency plus Chroma's HNSW index push memory tight on 1 GB. Add a 2 GB swap file so the process gets OOM-killed only under real pressure instead of routinely:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

The `/etc/fstab` line re-enables the swap file automatically on every reboot.

## 3-8: Automated provisioning

`deploy/provision_ec2.sh` does the rest: installs Python/git, creates a dedicated `raguser` system user, clones the repo, builds the venv, installs `requirements.txt`, lays down the systemd unit, and enables it (does not start it yet - you still need to set the API key and populate the DB).

```bash
scp -i your-key.pem deploy/provision_ec2.sh ec2-user@<instance-ip>:~/
ssh -i your-key.pem ec2-user@<instance-ip>
REPO_URL=https://github.com/you/rag-pipeline.git sudo -E bash provision_ec2.sh
```

Or run the equivalent steps manually - read the script, it's short and commented.

## 9. Set the Anthropic API key

```bash
sudo nano /etc/rag-pipeline/rag-pipeline.env
# set: ANTHROPIC_API_KEY=sk-ant-...
sudo chown raguser:raguser /etc/rag-pipeline/rag-pipeline.env
sudo chmod 600 /etc/rag-pipeline/rag-pipeline.env
```

Never commit this file (or a real key) to git - `deploy/rag-pipeline.env.example` is the template, not the real thing.

## 10. Populate the Chroma DB

The API only works once `/opt/rag-pipeline/data/chroma_db` has embedded chunks in it. Two options:

**Option A - build it on the instance** (simplest, slower - downloads papers + models over the instance's network):

```bash
cd /opt/rag-pipeline
sudo -u raguser venv/bin/python scripts/download_papers.py
sudo -u raguser venv/bin/python scripts/chunk_papers.py
sudo -u raguser venv/bin/python scripts/embed_and_store.py
```

**Option B - build locally and copy it over** (recommended - avoids re-downloading ~45 MB of PDFs and re-running embeddings on a slow burstable instance):

```bash
# From your machine, after running the pipeline locally:
rsync -avz -e "ssh -i your-key.pem" data/chroma_db/ ec2-user@<instance-ip>:/tmp/chroma_db/
ssh -i your-key.pem ec2-user@<instance-ip> \
  "sudo rsync -a /tmp/chroma_db/ /opt/rag-pipeline/data/chroma_db/ && sudo chown -R raguser:raguser /opt/rag-pipeline/data/chroma_db && rm -rf /tmp/chroma_db"
```

## 11. Start the service

```bash
sudo systemctl start rag-pipeline
sudo systemctl status rag-pipeline
curl http://localhost:8000/health
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How does RAG reduce hallucination?"}'
```

Since the unit is `enable`d, it also starts automatically on every future boot.

## 12. Persisting the Chroma DB across restarts

This is mostly already handled by how EC2 storage works, but it's worth being explicit about what "persists" and what doesn't:

- **Service restart** (crash, `systemctl restart`, `systemctl daemon-reload`): the process exits and a new one starts, but `data/chroma_db` on disk is untouched - `chromadb.PersistentClient` just reopens the same directory. Nothing to configure.
- **Instance reboot / stop-start**: `t3` instances are EBS-backed only (no ephemeral instance store), and the root EBS volume survives both a `reboot` and a `stop` + `start`. The `swapon`/fstab entry and the systemd `enable` both make sure the service comes back the same way. **No data loss here.**
- **Instance termination**: by default the root EBS volume has "delete on termination" set, so terminating the instance destroys `data/chroma_db` along with everything else. This is the actual gap to plan for:
  - Easiest: don't terminate - stop the instance instead when not in use (still free-tier friendly).
  - Better for real durability: take periodic EBS snapshots of the root volume, or run `deploy/backup_chroma_to_s3.sh` on a cron schedule to sync `data/chroma_db` to S3, then restore it (Option B above, from S3 instead of your laptop) onto any replacement instance.
  - Snapshot/backup on the same schedule you'd tolerate re-embedding for - Chroma DB here is fully reproducible by re-running `download_papers.py` -> `chunk_papers.py` -> `embed_and_store.py`, so backups are a convenience for fast recovery, not the only copy of anything irreplaceable.

## 13. Updating the app

```bash
cd /opt/rag-pipeline
sudo -u raguser git pull
sudo -u raguser venv/bin/pip install -r requirements.txt
sudo systemctl restart rag-pipeline
```

## 14. Logs and troubleshooting

```bash
sudo journalctl -u rag-pipeline -f      # tail logs
sudo systemctl status rag-pipeline      # current state, recent log lines
free -h                                 # check RAM/swap pressure
```

If the service repeatedly restarts, check `journalctl` first for an OOM kill (`dmesg | grep -i oom`) - the swap file from step 2 should prevent most of these, but a t3.micro is genuinely tight for an embedding model + API server. If it keeps happening, the next lever is a bigger instance (t3.small has 2 GB RAM) rather than more swap.

## Notes on the free tier and cost

- EC2 free tier covers 750 hrs/month of `t3.micro` for 12 months on new accounts (check current AWS terms - this has changed over time).
- The EC2 side is free-tier eligible; **Anthropic API calls are not** - every `/query` request costs money regardless of how the server is hosted. Keep the security group restrictive and consider adding a simple API key check in `main.py` before exposing this beyond your own testing.
