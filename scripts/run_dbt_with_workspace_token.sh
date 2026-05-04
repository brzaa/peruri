#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADC_FILE="${ROOT_DIR}/.gcloud/application_default_credentials.json"

if [[ ! -f "${ADC_FILE}" ]]; then
  echo "Missing ${ADC_FILE}. Run ./scripts/sync_gcloud_config.sh first." >&2
  exit 1
fi

ACCESS_TOKEN="$(
  CLOUDSDK_CONFIG="${ROOT_DIR}/.gcloud" \
  CLOUDSDK_PYTHON=python3 \
  gcloud auth print-access-token
)"

IFS=$'\t' read -r REFRESH_TOKEN CLIENT_ID CLIENT_SECRET TOKEN_URI <<< "$(
  python3 - <<'PY'
import json
from pathlib import Path

adc = json.loads(Path(".gcloud/application_default_credentials.json").read_text())
print(
    "\t".join(
        [
            adc["refresh_token"],
            adc["client_id"],
            adc["client_secret"],
            adc.get("token_uri", "https://oauth2.googleapis.com/token"),
        ]
    )
)
PY
)"

export DBT_PROFILES_DIR="${ROOT_DIR}/profiles"
export DBT_BIGQUERY_ACCESS_TOKEN="${ACCESS_TOKEN}"
export DBT_BIGQUERY_REFRESH_TOKEN="${REFRESH_TOKEN}"
export DBT_BIGQUERY_CLIENT_ID="${CLIENT_ID}"
export DBT_BIGQUERY_CLIENT_SECRET="${CLIENT_SECRET}"
export DBT_BIGQUERY_TOKEN_URI="${TOKEN_URI}"

cd "${ROOT_DIR}"
.venv/bin/dbt "$@" --profiles-dir profiles --target workspace_token
