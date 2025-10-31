#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Codex CVDP agent implementation for the agentic workflow.
This agent reads prompt.json and makes changes to files in the mounted directories.
"""

import sys
import subprocess
from prompts import KNOWLEDGE_GATHERING_PROMPT, NEXTPNR_OPTIMIZE_PROMPT, YOSYS_OPTIMIZE_PROMPT, RTL_CODE_OPTIMIZE_PROMPT

def build_prompt(base_prompt: str, prior_outputs: list[str]) -> str:
    """Augment the base prompt with prior Codex outputs for additional context."""
    history = "\n\n".join(output for output in prior_outputs if output)
    if not history:
        return base_prompt
    return f"{base_prompt}\n\nPrevious Codex outputs:\n{history}"

def codex_exec(prompt: str):
    """Run a codex exec command with the given prompt and return the output."""
    cmd = [
        "codex",
        "exec",                                         # run without human intervention
        "-m", "gpt-5-mini",                             # specify model
        "--dangerously-bypass-approvals-and-sandbox",   # full control for docker images
        "--skip-git-repo-check",                        # automatic write privilege
        prompt,                                         # prompt for codex
    ]

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Running codex exec (attempt {attempt}/{max_attempts})...")
            codex_cmd = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
            )
        except subprocess.TimeoutExpired as exc:
            print(f"Codex execution timed out on attempt {attempt}: {exc}")
            if attempt == max_attempts:
                print("Maximum retries reached. Skipping to next step.")
            continue
        except Exception as exc:
            print(f"Codex execution failed on attempt {attempt} with error: {exc}")
            if attempt == max_attempts:
                print("Maximum retries reached. Skipping to next step.")
            continue

        if codex_cmd.returncode == 0:
            print(f"Codex output:\n{codex_cmd.stdout}\n\nCodex thoughts:\n{codex_cmd.stderr}")
            return codex_cmd

        print(
            f"Codex returned non-zero exit code {codex_cmd.returncode} on attempt {attempt}.\n"
            f"Stdout:\n{codex_cmd.stdout}\n\nStderr:\n{codex_cmd.stderr}"
        )

        if attempt == max_attempts:
            print("Maximum retries reached. Skipping to next step.")

    return None

def main():
    """Main agent function"""
    print("Starting CVDP codex-agent...")
    try:
        codex_outputs = []
        print("Step 1: Knowledge Gathering")
        step1 = codex_exec(KNOWLEDGE_GATHERING_PROMPT)
        codex_outputs.append((step1.stdout if step1 else "").strip())

        print("Step 2: Yosys Optimization")
        step2 = codex_exec(build_prompt(YOSYS_OPTIMIZE_PROMPT, codex_outputs))
        codex_outputs.append((step2.stdout if step2 else "").strip())

        print("Step 3: NextPNR Optimization")
        step3 = codex_exec(build_prompt(NEXTPNR_OPTIMIZE_PROMPT, codex_outputs))
        codex_outputs.append((step3.stdout if step3 else "").strip())

        print("Step 4: RTL Code Optimization")
        codex_exec(build_prompt(RTL_CODE_OPTIMIZE_PROMPT, codex_outputs))


    except Exception as e:
        print(f"An unexpected error occurred during simulation: {str(e)}")

    print("Agent execution completed successfully")
    sys.exit(0)

if __name__ == "__main__":
    main() 
