#!/bin/sh 

# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Build without platform flag for native architecture (x86)
docker build -f Dockerfile-base -t cvdp-codex-struct-agent-base .
docker build -f Dockerfile-agent -t cvdp-codex-struct-agent --no-cache .
docker build -f Dockerfile-harness -t cvdp-harness --no-cache .

# Build with platform flag for x86 emulation on M1/Apple Silicon
# docker build --platform linux/amd64 -f Dockerfile-base -t cvdp-codex-struct-agent-base .
# docker build --platform linux/amd64 -f Dockerfile-agent -t cvdp-codex-struct-agent --no-cache .
