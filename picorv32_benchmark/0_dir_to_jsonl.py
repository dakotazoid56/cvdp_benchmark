#!/usr/bin/env python3
"""
repack_cvdp_workspace.py

Reverse of create_cvdp_workspace.py.

Given an output directory (default: temp/) that contains:
  - input.jsonl  (1 JSON object line with non-file keys)
  - a bunch of files/dirs (the workspace you created/edited)

This script reconstructs a single JSONL line that merges:
  - non-file keys loaded from input.jsonl
  - "context": { path -> content }
  - "harness": { path -> content }    (heuristics: docker-compose.yml, src/**, verif/test_runner.py, etc.)
  - "patch":   { path -> unified-diff } (heuristic: content looks like a unified diff)

Binary files are stored as {"__b64__": "<base64>"}.
"""

import argparse
import base64
import json
from pathlib import Path

# Files we’ll ignore when gathering workspace files
IGNORE_NAMES = {"input.jsonl", ".DS_Store"}

# Heuristics to classify harness files
def is_harness_path(rel: Path) -> bool:
    # Common harness bits used in your example payload:
    #   verif/docker-compose.yml
    #   verif/src/** (python tests, .env, helpers)
    #   verif/test_runner.py (or src/test_runner.py depending on layout)
    s = rel.as_posix()
    return (
        s.endswith("docker-compose.yml")
        or s.startswith("src/")
        or s.startswith("verif/src/")
        or s.endswith("verif/test_runner.py")
        or s.endswith("src/test_runner.py")
        or s.endswith("verif/.env")
        or s.endswith("src/.env")
    )

# Heuristic to detect unified-diff-ish content (for "patch")
def looks_like_unified_diff(text: str) -> bool:
    # Catch common patterns:
    #   --- old
    #   +++ new
    #   @@ -x,y +a,b @@
    # or git format: "diff --git a/... b/..."
    head = text.splitlines()[:10]
    joined = "\n".join(head)
    if "diff --git " in joined:
        return True
    has_markers = any(l.startswith(("--- ", "+++ ", "@@ ")) for l in head)
    return has_markers

def read_text_or_b64(p: Path):
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"__b64__": base64.b64encode(p.read_bytes()).decode("ascii")}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="picorv32_datapoint", help="Workspace directory to repack (default: temp)")
    ap.add_argument("--out", default="output.jsonl", help="Output JSONL path (default: output.jsonl)")
    args = ap.parse_args()

    base = Path(args.dir).resolve()
    if not base.exists():
        raise SystemExit(f"Workspace not found: {base}")

    # 1) Load non-file keys from input.jsonl (first line only)
    input_jsonl = base / "input.jsonl"
    if not input_jsonl.exists():
        raise SystemExit(f"Missing {input_jsonl}")
    with input_jsonl.open("r", encoding="utf-8") as f:
        first_line = f.readline()
    if not first_line.strip():
        raise SystemExit(f"{input_jsonl} is empty")
    payload = json.loads(first_line)

    # 2) Walk all files under base, excluding input.jsonl
    context = {}
    harness = {}
    patch = {}

    for p in base.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(base)
        if rel.name in IGNORE_NAMES:
            continue

        content = read_text_or_b64(p)
        # Classify
        if isinstance(content, str) and looks_like_unified_diff(content):
            patch[rel.as_posix()] = content
        elif is_harness_path(rel):
            harness[rel.as_posix()] = content
        else:
            context[rel.as_posix()] = content

    # 3) Build final line and write
    final_obj = dict(payload)
    final_obj["context"] = context
    final_obj["harness"] = harness
    final_obj["patch"] = patch

    outp = Path(args.out).resolve()
    with outp.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(final_obj, ensure_ascii=False) + "\n")

    # Quick summary
    print(f"Wrote {outp}")
    print(f"  context files: {len(context)}")
    print(f"  harness files: {len(harness)}")
    print(f"  patch files  : {len(patch)}")

if __name__ == "__main__":
    main()
