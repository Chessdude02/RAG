#!/usr/bin/env bash
# Optional: sync the persistent Chroma DB to S3 for durability beyond this
# instance's EBS volume (protects against accidental termination, not just
# stop/reboot). Requires the AWS CLI and an IAM role/profile with s3:PutObject
# on the target bucket.
#
# Usage:
#   S3_BUCKET=my-rag-backups bash backup_chroma_to_s3.sh
#
# To run nightly, add a cron entry for the raguser user, e.g.:
#   0 3 * * * S3_BUCKET=my-rag-backups /opt/rag-pipeline/deploy/backup_chroma_to_s3.sh >> /var/log/rag-backup.log 2>&1
set -euo pipefail

APP_DIR="/opt/rag-pipeline"
: "${S3_BUCKET:?Set S3_BUCKET to the target bucket name}"

aws s3 sync "$APP_DIR/data/chroma_db" "s3://$S3_BUCKET/chroma_db" --delete
echo "$(date -Iseconds) - synced $APP_DIR/data/chroma_db to s3://$S3_BUCKET/chroma_db"
