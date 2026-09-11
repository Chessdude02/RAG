#!/usr/bin/env bash
# Provisions an Amazon Linux 2023 t3.micro EC2 instance to run the RAG pipeline
# API under systemd. Run on the instance as root (e.g. `sudo bash provision_ec2.sh`).
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
SWAP_FILE="/swapfile"
SWAP_SIZE_MB=2048

: "${REPO_URL:?Set REPO_URL to your git remote, e.g. REPO_URL=https://github.com/you/rag-pipeline.git}"

echo "== Installing system packages =="
dnf update -y
dnf install -y python3 python3-pip git
python3 --version  # confirm >= 3.10 before continuing; install python3.11 via dnf if not

echo "== Creating app user =="
id -u "$APP_USER" &>/dev/null || useradd --system --create-home --shell /usr/sbin/nologin "$APP_USER"

echo "== Setting up swap (t3.micro only has 1GB RAM - embedding model + torch need headroom) =="
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
sudo -u "$APP_USER" python3 -m venv "$APP_DIR/venv"
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
