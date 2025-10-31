#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PICOSOC_DIR="${SCRIPT_DIR}/picorv32/picosoc"

cd "${PICOSOC_DIR}"
nextpnr-ecp5 \
  --45k --package CABGA381 --speed 6 \
  --json picosoc.json \
  --out-of-context \
  --freq 100 \
  --report pnr_report.json \
  --write pnr_routed.json


