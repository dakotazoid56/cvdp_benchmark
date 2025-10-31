#!/bin/sh 

# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

docker build -f Dockerfile-base -t cvdp-human-agent-base .
docker build -f Dockerfile-agent -t cvdp-human-agent --no-cache .
docker build -f Dockerfile-harness -t cvdp-human-harness --no-cache .
