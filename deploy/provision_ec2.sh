#!/usr/bin/env bash
# Provisions an Amazon Linux 2023 t3.small EC2 instance to run the RAG pipeline
# API under systemd. Run on the instance as root (e.g. `sudo bash provision_ec2.sh`).
#
# Instance sizing: use t3.small (2 GB RAM) - see DEPLOYMENT.md "Memory footprint"
# for measured numbers. Models + BM25 index alone measure ~896 MB RSS, before
# Chroma's HNSW index, the OS, or a single request - too close to t3.micro's 1 GB
# ceiling for safe operation (full warmed-up process lands around ~1.0 GB). This
# script also works on t3.micro, where the swap file below becomes load-bearing
# rather than a spike buffer - see SWAP_SIZE_MB below. t3.small isn't in the
# always-free tier (see DEPLOYMENT.md "Cost management") - stop the instance when
# not in use.
#
# Required env var:
#   REPO_URL - git remote to clone, e.g. https://github.com/you/rag-pipeline.git
#
# Usage:
#   REPO_URL=https://github.com/you/rag-pipeline.git sudo -E bash provision_ec2.sh
set -euo pipefail

APP_USER="raguser"
APP_DIR="/opt/rag-pipeline"
ENV_DIR="/etc/rag-pipeline"
# 1 GB, not 2 GB: on the recommended t3.small (2048 MB RAM), the warmed-up app
# already measures ~1007 MB RSS (see DEPLOYMENT.md "Memory footprint"), leaving
# ~800-900 MB of real headroom before swap is even touched once Amazon Linux's own
# baseline (sshd, systemd-journald, etc., roughly 150-200 MB) is accounted for. A
# 1 GB swap file is a proportionate buffer for transient concurrent-request spikes
# on top of that, not the load-bearing 2 GB it needed to be on t3.micro, where the
# same ~1007 MB app footprint alone exceeds the instance's total 1 GB of RAM.
#
# Running this on t3.micro instead (unsupported fallback - see DEPLOYMENT.md):
# override with `SWAP_SIZE_MB=2048 REPO_URL=... sudo -E bash provision_ec2.sh`,
# since 1 GB of swap on top of only 1 GB of physical RAM isn't enough headroom
# for a ~1007 MB app footprint plus OS overhead.
SWAP_FILE="/swapfile"
SWAP_SIZE_MB="${SWAP_SIZE_MB:-1024}"

: "${REPO_URL:?Set REPO_URL to your git remote, e.g. REPO_URL=https://github.com/you/rag-pipeline.git}"

echo "== Installing system packages =="
dnf update -y
# Amazon Linux 2023's default `python3` is 3.9; sentence-transformers==6.0.1 needs
# >=3.10, so install python3.11 explicitly and use it by name everywhere below
# rather than relying on whatever `python3` happens to resolve to.
dnf install -y python3.11 python3.11-pip git
python3.11 --version

echo "== Creating app user =="
id -u "$APP_USER" &>/dev/null || useradd --system --create-home --shell /usr/sbin/nologin "$APP_USER"

echo "== Setting up ${SWAP_SIZE_MB}MB swap (buffer on t3.small; override SWAP_SIZE_MB=2048 if running on t3.micro, where it's load-bearing) =="
if [ ! -f "$SWAP_FILE" ]; then
    fallocate -l "${SWAP_SIZE_MB}M" "$SWAP_FILE"
    chmod 600 "$SWAP_FILE"
    mkswap "$SWAP_FILE"
    swapon "$SWAP_FILE"
    grep -q "^$SWAP_FILE " /etc/fstab || echo "$SWAP_FILE none swap sw 0 0" >> /etc/fstab
else
    echo "  -> $SWAP_FILE already exists, skipping"
fi

echo "== Cloning / updating repo =="
if [ -d "$APP_DIR/.git" ]; then
    sudo -u "$APP_USER" git -C "$APP_DIR" pull
else
    git clone "$REPO_URL" "$APP_DIR"
    chown -R "$APP_USER:$APP_USER" "$APP_DIR"
fi

echo "== Creating virtualenv and installing dependencies =="
sudo -u "$APP_USER" python3.11 -m venv "$APP_DIR/venv"
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install --upgrade pip
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "== Setting up environment file =="
mkdir -p "$ENV_DIR"
if [ ! -f "$ENV_DIR/rag-pipeline.env" ]; then
    cp "$APP_DIR/deploy/rag-pipeline.env.example" "$ENV_DIR/rag-pipeline.env"
    echo "  -> Created $ENV_DIR/rag-pipeline.env - edit it and set ANTHROPIC_API_KEY before starting the service"
fi
chown "$APP_USER:$APP_USER" "$ENV_DIR/rag-pipeline.env"
chmod 600 "$ENV_DIR/rag-pipeline.env"

echo "== Ensuring data directory exists and is writable by the app user =="
mkdir -p "$APP_DIR/data/chroma_db" "$APP_DIR/data/papers" "$APP_DIR/data/chunks"
chown -R "$APP_USER:$APP_USER" "$APP_DIR/data"

echo "== Installing systemd unit =="
cp "$APP_DIR/deploy/rag-pipeline.service" /etc/systemd/system/rag-pipeline.service
systemctl daemon-reload
systemctl enable rag-pipeline.service

cat <<EOF

== Provisioning complete. Next steps ==
  1. Edit $ENV_DIR/rag-pipeline.env and set your real ANTHROPIC_API_KEY.
  2. Populate $APP_DIR/data/chroma_db - either:
       a) rsync/scp a pre-built data/chroma_db from your machine, or
       b) run the pipeline scripts on this instance (see DEPLOYMENT.md).
  3. Start the service:  sudo systemctl start rag-pipeline
  4. Check status:       sudo systemctl status rag-pipeline
  5. Tail logs:          sudo journalctl -u rag-pipeline -f
EOF
