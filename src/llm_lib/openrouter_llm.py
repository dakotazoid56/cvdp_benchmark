# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import openai
import logging
from typing import Optional
from .openai_llm import OpenAI_Instance
from src.config_manager import config

logging.basicConfig(level=logging.INFO)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

class OpenRouter_Instance(OpenAI_Instance):
    """
    OpenRouter model instance using OpenAI-compatible API.

    Supports multiple model providers available through OpenRouter (Qwen, Moonshot AI, etc.).
    Uses the OpenAI Python SDK with a custom base_url pointing to OpenRouter's API.
    """

    def __init__(self, context: str = "You are a helpful assistant.",
                 key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize OpenRouter model instance.

        Args:
            context: System context/prompt
            key: OpenRouter API key (optional, reads from OPENROUTER_API_KEY env var)
            model: Model name in format "provider/model-name[:variant]"
                   Examples: "qwen/qwen3-coder-30b-a3b-instruct",
                            "moonshotai/kimi-k2-thinking",
                            "moonshotai/kimi-k2-0905:exacto"

        Raises:
            ValueError: If model name is not provided or API key is missing
        """
        if model is None:
            raise ValueError("Model name is required for OpenRouter models")

        self.context = context
        self.model = self._resolve_model_name(model)
        self.debug = False

        # Get API key from parameter or environment
        api_key = key or config.get("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is required for OpenRouter models. "
                "Please set it in your .env file or pass via 'key' parameter."
            )

        # Create OpenAI client with OpenRouter base URL and required headers
        # OpenRouter requires specific headers for proper routing
        self.chat = openai.OpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://github.com/dakotabarnes/poRTLe",  # Optional: for rankings
                "X-Title": "poRTLe CVDP Benchmark"  # Optional: shows in dashboard
            }
        )

        self.set_debug(False)
        logging.info(f"Created OpenRouter Model. Using model: {self.model}")

    def _resolve_model_name(self, model_name: str) -> str:
        """
        Resolve model names to OpenRouter model IDs.

        OpenRouter expects model IDs in the format: "provider/model-name[:variant]"

        Supports:
        - Full paths with provider: "qwen/qwen3-coder-30b-a3b-instruct" -> as-is
        - Full paths with variants: "moonshotai/kimi-k2-0905:exacto" -> as-is
        - With "openrouter/" prefix: "openrouter/qwen/model" -> "qwen/model"

        Args:
            model_name: Model identifier in any supported format

        Returns:
            Full OpenRouter model ID (e.g., "qwen/qwen3-coder-30b-a3b-instruct")

        Raises:
            ValueError: If model name doesn't include provider prefix
        """
        if not model_name:
            raise ValueError("Model name is required")

        # Strip "openrouter/" prefix if present
        if model_name.startswith("openrouter/"):
            model_name = model_name[len("openrouter/"):]
            logging.debug(f"Stripped 'openrouter/' prefix: {model_name}")

        # If already has provider prefix (e.g., "qwen/..." or "moonshotai/..."), use as-is
        # This includes variant suffixes like ":exacto"
        if "/" in model_name:
            logging.debug(f"Using full model path: {model_name}")
            return model_name

        # If no provider prefix, this is an error - user must specify provider
        raise ValueError(
            f"Model name '{model_name}' must include provider prefix. "
            f"Examples: 'qwen/qwen3-coder-30b-a3b-instruct', "
            f"'moonshotai/kimi-k2-thinking', 'qwen/qwen3-235b-a22b-2507'"
        )

    # All other methods inherited from OpenAI_Instance:
    # - prompt() - Sends prompts to OpenRouter API and handles responses
    # - set_debug() - Enables/disables debug logging
    # - key() - Updates API key
    # - requires_evaluation property - Returns True (requires harness evaluation)
