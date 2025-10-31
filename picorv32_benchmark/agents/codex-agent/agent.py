#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Codex CVDP agent implementation for the agentic workflow.
This agent reads prompt.json and makes changes to files in the mounted directories.
"""

import sys
import subprocess
from prompts import CODEX_SYSTEM_PROMPT

def main():
    """Main agent function"""
    print("Starting CVDP codex-agent...")
    try:

        cmd = [
            "codex",
            "exec",                                         # run without human intervention
            "-m", "gpt-5-mini",                             # specify model
            "--dangerously-bypass-approvals-and-sandbox",   # full control for docker images
            "--skip-git-repo-check",                        # automatic write privilege
            CODEX_SYSTEM_PROMPT,                            # prompt for codex
        ]

        codex_cmd = subprocess.run(cmd, check=False, capture_output=True, text=True)
        
        print(f"Codex output:\n{codex_cmd.stdout}\n\nCodex thoughts:\n{codex_cmd.stderr}")

    except Exception as e:
        print(f"An unexpected error occurred during simulation: {str(e)}")

    print("Agent execution completed successfully")
    sys.exit(0)

if __name__ == "__main__":
    main() 