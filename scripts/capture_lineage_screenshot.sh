#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8081}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PID_FILE="${ROOT_DIR}/assets/dbt-docs.pid"

cd "${ROOT_DIR}"
export DBT_PROFILES_DIR="${ROOT_DIR}/profiles"

./scripts/run_dbt_with_workspace_token.sh docs generate --empty-catalog

cleanup() {
  if [[ -f "${PID_FILE}" ]]; then
    kill "$(cat "${PID_FILE}")" >/dev/null 2>&1 || true
    rm -f "${PID_FILE}"
  fi
}

trap cleanup EXIT

./scripts/run_dbt_with_workspace_token.sh docs serve --port "${PORT}" >/tmp/peruri_dbt_docs.log 2>&1 &
echo $! > "${PID_FILE}"
sleep 5

"${CHROME_BIN}" \
  --headless \
  --disable-gpu \
  --window-size=1600,1200 \
  --screenshot="${ROOT_DIR}/assets/dbt-lineage.png" \
  "http://127.0.0.1:${PORT}/#!/overview"

cleanup
