#!/usr/bin/env python3

"""
Runner for the agent which will build and run the benchmark with the specified agent.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---- Hardcoded settings you can tweak if needed ----
AGENT_NAME = "human-agent"
RUNS_DIR = Path(__file__).parent / "agents" / AGENT_NAME / "runs"
DATASET = "picorv32_benchmark/output.jsonl"
TEST_NAME = "cvdp_agentic_picorv32_dakota_0001"


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def next_run_dir(base: Path) -> Path:
    ensure_dir(base)
    max_id = 0
    for child in base.iterdir():
        m = re.fullmatch(r"run-(\d{4})", child.name)
        if m:
            max_id = max(max_id, int(m.group(1)))
    nxt = max_id + 1
    return base / f"run-{nxt:04d}"

def run(cmd, cwd: Path | None = None):
    print(f"\n$ {' '.join(cmd)} (cwd={cwd or Path.cwd()})")
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)

def copy_agent_code(src: Path, dest: Path):
    if not src.is_dir():
        raise SystemExit(f"ERROR: agent directory not found: {src}")
    ensure_dir(dest)
    shutil.copyfile(src / "agent.py", dest / "agent.py")
    #shutil.copyfile(src / "prompts.py", dest / "prompts.py")

def build_agent(agent_dir: Path):
    build_script = agent_dir / "build_agent.sh"
    if not build_script.exists():
        raise SystemExit(f"ERROR: build script not found at: {build_script}")
    run(["bash", build_script.name], cwd=agent_dir)

def run_benchmark(output_dir: Path, project_root: Path, repo_root: Path, test_name: str):
    cmd = [
        "./run_benchmark.py",
        "-f",
        DATASET,
        "-i",
        test_name,
        "-l",
        "-g",
        f"cvdp-{AGENT_NAME}:latest",
        "-p",
        str((project_root / output_dir).resolve()),
    ]
    print(f"\n$ {' '.join(cmd)} (cwd={repo_root})")
    process = subprocess.Popen(
        cmd,
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Check if Benchmark Passed or Failed
    found_zero_result = False
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")
        if '"result": 0' in line:
            found_zero_result = True
    return_code = process.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)
    return found_zero_result



def main():
    test_name = TEST_NAME
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        print(f"Overriding test name with CLI argument: {test_name}")

    script_dir = Path(__file__).parent
    agent_root = script_dir / "agents" / AGENT_NAME
    repo_root = script_dir.parent

    print(f"Agent root: {agent_root}")
    print(f"Repo root: {repo_root}")
    if not agent_root.is_dir():
        raise SystemExit(f"ERROR: '{AGENT_NAME}' directory not found at: {agent_root}")

    run_dir = next_run_dir(RUNS_DIR)
    ensure_dir(run_dir)
    print(f"==> New run dir: {run_dir}")

    build_agent(agent_root)

    copy_agent_code(agent_root, run_dir)

    zero_result_reported = run_benchmark(run_dir, agent_root, repo_root, test_name)
    if zero_result_reported:
        print('\nBenchmark PASSED: YAYA!')
    else:
        print('\nBenchmark FAILED: WHOMP WHOMP.')

    print(f"\nAll done! Result output is in: {run_dir}")

if __name__ == "__main__":
    main()
