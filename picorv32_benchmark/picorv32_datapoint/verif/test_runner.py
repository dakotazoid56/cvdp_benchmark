#!/usr/bin/env python3
from __future__ import annotations

###### COPY OF THE TEST_RUNNER.PY FOR THE AGENT ####
###### FINAL GRADE DONE BY EXTERNAL COPY ######

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, Any

ROOT   = Path("/code").resolve()              # adjust if needed
RUNDIR = (ROOT / "rundir").resolve()
RUNDIR.mkdir(parents=True, exist_ok=True)

SIM_SH     = ROOT / "rtl" / "0_sim.sh"
YOSYS_SH   = ROOT / "rtl" / "1_yosys.sh"
NEXTPNR_SH = ROOT / "rtl" / "2_nextpnr.sh"

def run_script(path: Path) -> subprocess.CompletedProcess[str]:
    """Run a script through bash to avoid shebang/exec-format issues."""
    if not path.exists():
        raise FileNotFoundError(f"Script not found: {path}")
    cp = subprocess.run(
        ["/usr/bin/env", "bash", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,  # don't raise; we still want to parse output on non-zero
    )
    # Save raw log beside metrics for debugging
    log_path = RUNDIR / (path.stem + ".log")
    log_path.write_text(cp.stdout, encoding="utf-8")
    return cp

def parse_sim_output(text: str) -> Dict[str, Any]:
    """
    Expect lines like:
      Cycle counter ......... 420454
      Instruction counter .... 89450
      CPI: 4.70
      DONE
    """
    cycle_m = re.search(r"Cycle\s+counter\s*\.{2,}\s*([0-9_,]+)", text, re.IGNORECASE)
    instr_m = re.search(r"Instruction\s+counter\s*\.{2,}\s*([0-9_,]+)", text, re.IGNORECASE)
    cpi_m   = re.search(r"\bCPI:\s*([0-9]+(?:\.[0-9]+)?)", text)

    def to_int_num(s: str) -> int:
        return int(s.replace("_", "").replace(",", ""))

    out: Dict[str, Any] = {}
    if cycle_m:
        out["0_cycle_counter"] = to_int_num(cycle_m.group(1))
    if instr_m:
        out["0_instruction_counter"] = to_int_num(instr_m.group(1))
    if cpi_m:
        out["0_cpi"] = float(cpi_m.group(1))

    out["0_done_seen"] = bool(re.search(r"^\s*DONE\s*$", text, re.MULTILINE))
    return out

def parse_yosys_output(text: str) -> Dict[str, Any]:
    """
    Expect line like:
      Found and reported 0 problems.
    """
    m = re.search(r"Found and reported\s+([0-9]+)\s+problems\.", text, re.IGNORECASE)
    return {"1_yosys_problems": int(m.group(1))} if m else {}

def parse_nextpnr_output(text: str) -> Dict[str, Any]:
    """
    Expect line like:
      ERROR: Max frequency for clock 'clk': 53.39 MHz (FAIL at 100.00 MHz)
    We extract 53.39 as fmax_mhz (float).
    """
    m = re.search(
        r"Max\s+frequency\s+for\s+clock\s+'[^']+':\s*([0-9]+(?:\.[0-9]+)?)\s*MHz",
        text,
        re.IGNORECASE,
    )
    return {"2_fmax_mhz": float(m.group(1))} if m else {}

def main() -> None:
    metrics: Dict[str, Any] = {}

    # 0) Simulation
    sim_cp = run_script(SIM_SH)
    metrics.update(parse_sim_output(sim_cp.stdout))
    metrics["0_sim_exit_code"] = sim_cp.returncode

    # 1) Yosys
    yosys_cp = run_script(YOSYS_SH)
    metrics.update(parse_yosys_output(yosys_cp.stdout))
    metrics["1_yosys_exit_code"] = yosys_cp.returncode

    # 2) nextpnr
    pnr_cp = run_script(NEXTPNR_SH)
    metrics.update(parse_nextpnr_output(pnr_cp.stdout))
    metrics["2_nextpnr_exit_code"] = pnr_cp.returncode

    # Write metrics artifact
    out_json = RUNDIR / "metrics.json"
    out_json.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    # Pretty print summary for console
    print("=== Metrics ===")
    for k in sorted(metrics.keys()):
        print(f"{k}: {metrics[k]}")

    # Exit code policy:
    # - Prefer success if we parsed the three key values; otherwise bubble up a non-zero
    required = ["0_cycle_counter", "0_instruction_counter", "0_cpi", "1_yosys_problems", "2_fmax_mhz"]
    missing  = [k for k in required if k not in metrics]
    if missing:
        print(f"[WARN] Missing metrics: {', '.join(missing)}")
        # If any stage failed hard (non-zero), reflect that
        combined_rc = sim_cp.returncode or yosys_cp.returncode or pnr_cp.returncode
        raise SystemExit(combined_rc if combined_rc != 0 else 2)
    else:
        # Optionally ensure sim reported DONE
        if not metrics.get("done_seen", False):
            print("[WARN] 'DONE' not observed in simulation log.")
        raise SystemExit(0)

if __name__ == "__main__":
    main()
