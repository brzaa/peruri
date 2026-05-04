#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${ROOT_DIR}/.gcloud"
rsync -a --delete "${HOME}/.config/gcloud/" "${ROOT_DIR}/.gcloud/"
echo "Mirrored gcloud config into ${ROOT_DIR}/.gcloud"
echo "Use with:"
echo "  export CLOUDSDK_CONFIG=${ROOT_DIR}/.gcloud"
echo "  export CLOUDSDK_PYTHON=python3"

