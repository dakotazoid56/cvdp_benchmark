#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PICORV32_DIR="${SCRIPT_DIR}/picorv32"

cd "${PICORV32_DIR}"
make test TOOLCHAIN_PREFIX=riscv64-unknown-elf-
