# Deploying to AWS EC2 (t3.small recommended) with systemd

> **Memory: `t3.micro` (1 GB RAM) is no longer sufficient.** The app now loads an
> embedding model, a cross-encoder reranker, and an in-memory BM25 index over the
> full chunk corpus (hybrid retrieval), in addition to Chroma's HNSW index. Measured
> RSS for the models/indexes alone (embedding model + cross-encoder + BM25 index) is
> **~896 MB** — before Chroma's own HNSW index, the OS, sshd, systemd-journald, or
> any concurrent request overhead are added on top (see "Memory footprint" below for
> the full breakdown, which puts total warmed-up process RSS around ~1.0 GB). 896 MB
> is already too close to `t3.micro`'s 1 GB ceiling for safe operation on its own, so
> we chose `t3.small` (2 GB RAM) as the default; `t3.micro` + swap is documented below
> only as a degraded fallback, not a recommended path.

Files referenced below live in `deploy/`:
- `rag-pipeline.service` - systemd unit
- `rag-pipeline.env.example` - template for the secrets file
- `provision_ec2.sh` - automates steps 3-8 below
- `backup_chroma_to_s3.sh` - optional off-instance backup of the Chroma DB

## 1. Launch the instance

- AMI: Amazon Linux 2023 (free tier eligible)
- Instance type: **`t3.small` (2 GB RAM, 2 vCPU burstable) - recommended.** `t3.small`
  is not covered by the AWS free tier (`t3.micro` is); see "Memory footprint" below
  for why the upgrade is worth the cost. If you need to stay on the free tier, read
  the `t3.micro` fallback notes in step 2 first and expect noticeably higher query
  latency from swap use.
- Storage: default 8 GB gp3 root volume is fine (free tier covers up to 30 GB)
- Security group:
  - SSH (22) - restrict to your IP, not `0.0.0.0/0`
  - Custom TCP 8000 - only from IPs/CIDRs that should reach the API (the Anthropic API calls this triggers cost money per request - don't leave it open to the world)
- Key pair: create or reuse one for SSH access

## 2. Memory footprint (measured) and swap

The embedding model, cross-encoder, Chroma/HNSW index, and BM25 index are all loaded
into memory at process startup (`main.py`'s `lifespan` warms up all four before
accepting requests). Measured resident memory (RSS) at each stage, on the current
corpus (17,881 chunks from ~700 papers):

| Stage | RSS | Delta |
|---|---:|---:|
| Python process baseline | 17 MB | - |
| `import query_rag` (loads PyTorch/transformers) | 500 MB | +483 MB |
| Embedding model loaded (`all-MiniLM-L6-v2`) | 516 MB | +16 MB |
| Cross-encoder loaded (`ms-marco-MiniLM-L-6-v2`) | 521 MB | +5 MB |
| Chroma collection opened + first query (HNSW index) | 623 MB | +102 MB |
| BM25 index built (full corpus, in-memory) | **1007 MB** | **+384 MB** |

That is, the models and BM25 index alone (everything except Chroma's HNSW index) account
for **~896 MB** of resident memory (1007 MB total − 102 MB Chroma/HNSW ≈ 896 MB) — this
is the number that drove the `t3.small` decision above, since 896 MB is already
uncomfortably close to `t3.micro`'s full 1 GB before Chroma, the OS, or a single
request are accounted for. Total process RSS including Chroma lands around ~1.0 GB.

Two things stand out:
- **PyTorch itself is the single biggest fixed cost** (~483 MB) just from being
  imported, before any model weights are loaded - this was already true before hybrid
  retrieval was added, but it means there's no cheap way to shave memory off the
  embedding/reranking side without dropping `sentence-transformers` entirely.
- **The BM25 index is the largest addition from hybrid retrieval** (~384 MB): it
  keeps a tokenized copy of every chunk in the corpus in memory
  (`get_bm25_index()`/`rank_bm25.BM25Okapi`), on top of the full chunk text already
  held for building context. This cost scales with corpus size - it will grow if the
  ~700-paper corpus grows.

**Bottom line: the warmed-up process alone uses ~1.0 GB, matching or exceeding the
entire physical RAM of a `t3.micro`.** That leaves nothing for the OS, sshd,
`systemd-journald`, or per-request allocations (query embeddings, retrieval
candidate pools, generation buffers), so a `t3.micro` will be swapping continuously
in steady state, not just under occasional load spikes as the swap file was
originally intended to cover. On `t3.small` (2 GB), the same ~1.0 GB footprint still
leaves roughly 1 GB of headroom, which is what swap was meant to be a safety net for
in the first place.

If you still want to run on `t3.micro` (e.g. to stay on the free tier), add a 2 GB
swap file - but treat this as a workaround for a machine that's undersized for this
workload, not a fix, and expect materially higher p99 latency from routine swapping:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

The `/etc/fstab` line re-enables the swap file automatically on every reboot. On
`t3.small`, the same swap file is still worth adding as a buffer against transient
spikes (e.g. concurrent requests), just not as the primary way the process fits in
RAM.

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

**Option B - build locally and copy it over** (recommended - avoids re-downloading ~1.1 GB of PDFs and re-running embeddings on a slow burstable instance):

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
  - Easiest: don't terminate - stop the instance instead when not in use (see "Cost management" below - stopping costs only a few cents/month in EBS storage).
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

If the service repeatedly restarts, check `journalctl` first for an OOM kill (`dmesg | grep -i oom`). If you're on `t3.small` as recommended, this shouldn't happen in steady state - investigate concurrent request volume or a corpus size increase before adding swap. If you're on `t3.micro`, this is expected under any real load: the ~1.0 GB measured footprint (see "Memory footprint" in step 2) already saturates the instance's RAM, so the fix is moving to `t3.small`, not tuning swap further.

## 15. Cost management: stop the instance when not in use

`t3.small` is not in the always-free tier (unlike `t3.micro`), so this is a
low-cost deployment, not a zero-cost one. On-demand `t3.small` runs approximately
**~$0.02/hour** (region-dependent; check current EC2 pricing for the exact rate) -
roughly $15/month if left running continuously, versus a few cents for an occasional
demo session.

Since `data/chroma_db` persists on the root EBS volume independent of whether the
instance is running (see step 12), there's no reason to pay for idle compute:

```bash
# stop when you're done demoing (from your machine, with AWS CLI configured)
aws ec2 stop-instances --instance-ids <instance-id>

# start again before the next demo
aws ec2 start-instances --instance-ids <instance-id>
```

Or use the EC2 console's Instance State > Stop/Start. A few things to keep in mind:

- A stopped instance still costs a small amount for its EBS root volume (gp3 storage,
  billed per GB-month regardless of running state) - this is a few cents/month for
  the default 8 GB volume, not the ~$0.02/hour compute rate.
- Stopping (not terminating) preserves the instance, its EBS volume, and
  `data/chroma_db` exactly as they were - starting it back up does not require
  re-running any of the provisioning or ingestion steps above.
- The instance gets a new public IP on each start unless you attach an Elastic IP
  (which has its own small cost when not attached to a running instance) - update
  DNS/bookmarks accordingly, or just re-check the console each time.
- The systemd unit is `enable`d, so `rag-pipeline` starts automatically as soon as the
  instance boots - no manual restart needed after `start-instances`.

## Notes on the free tier and cost

- EC2 free tier covers 750 hrs/month of `t3.micro` for 12 months on new accounts (check current AWS terms - this has changed over time). `t3.small` is not covered by the free tier - budget for its on-demand hourly rate if you follow the `t3.small` recommendation above (see "Cost management" above).
- The EC2 side is (partially) free-tier eligible; **Anthropic API calls are not** - every `/query` request costs money regardless of how the server is hosted. Keep the security group restrictive and consider adding a simple API key check in `main.py` before exposing this beyond your own testing.
