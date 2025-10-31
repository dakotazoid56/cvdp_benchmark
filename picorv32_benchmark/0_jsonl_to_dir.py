#!/usr/bin/env python3
"""
create_cvdp_workspace.py

Usage:
  python create_cvdp_workspace.py payload.json  [--out temp]

- Creates files from:
    - context (path -> content)
    - patch   (path -> unified diff content)
    - harness (path -> content)
  under the output folder (default: temp/), preserving relative paths.

- Writes all remaining top-level keys (id, categories, system_message, prompt, etc.)
  to temp/input.jsonl as a single JSON line.
"""

import argparse
import json
import sys
from pathlib import Path

FILE_KEYS = {"context", "patch", "harness"}

def write_mapping(base: Path, mapping: dict, label: str):
    """Write a path->content mapping to disk under base/."""
    if not mapping:
        return 0
    count = 0
    for relpath, content in mapping.items():
        # normalize and ensure we're strictly inside base
        rel = Path(relpath)
        out_path = (base / rel).resolve()
        # prevent escaping outside base
        if base not in out_path.parents and out_path != base:
            raise ValueError(f"{label}: path escapes base dir: {relpath}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Coerce to string for safety (content is expected to be text)
        out_path.write_text(str(content), encoding="utf-8", newline="\n")
        count += 1
    return count

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Path to JSON payload (single object).")
    ap.add_argument("--out", default="temp", help="Output directory (default: temp)")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Split file-like sections vs the “non-file” metadata
    context = payload.get("context", {})
    patch   = payload.get("patch", {})
    harness = payload.get("harness", {})

    # Write files
    n_ctx = write_mapping(out_dir, context, "context")
    n_pat = write_mapping(out_dir, patch, "patch")
    n_har = write_mapping(out_dir, harness, "harness")

    # Save the non-file top-level keys to input.jsonl
    non_file = {k: v for k, v in payload.items() if k not in FILE_KEYS}
    input_jsonl = out_dir / "input.jsonl"
    with input_jsonl.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(non_file, ensure_ascii=False) + "\n")

    # Friendly summary
    print(f"Output directory: {out_dir}")
    print(f"  Wrote {n_ctx} context file(s)")
    print(f"  Wrote {n_pat} patch file(s)")
    print(f"  Wrote {n_har} harness file(s)")
    print(f"  Wrote non-file keys to: {input_jsonl}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
