# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import logging
from typing import Optional
from mistralai import Mistral
from src.config_manager import config
from src.model_helpers import ModelHelpers

logging.basicConfig(level=logging.INFO)


class Mistral_Instance:
    """
    Mistral model instance using the Mistral AI SDK.

    Supports Mistral models including mistral-medium, mistral-large, etc.
    """

    # Model name mappings for convenience
    MODEL_ALIASES = {
        "mistral-medium": "mistral-medium-latest",
        "mistral-large": "mistral-large-latest",
        "mistral-small": "mistral-small-latest",
        "codestral": "codestral-latest",
    }

    def __init__(self, context: str = "You are a helpful assistant.",
                 key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Mistral model instance.

        Args:
            context: System context/prompt
            key: Mistral API key (optional, reads from MISTRAL_API_KEY env var)
            model: Model name (e.g., "mistral-medium", "mistral-medium-latest")

        Raises:
            ValueError: If model name is not provided or API key is missing
        """
        if model is None:
            raise ValueError("Model name is required for Mistral models")

        self.context = context
        self.model = self._resolve_model_name(model)
        self.debug = False

        # Get API key from parameter or environment
        api_key = key or config.get("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError(
                "MISTRAL_API_KEY is required for Mistral models. "
                "Please set it in your .env file or pass via 'key' parameter."
            )

        # Create Mistral client
        self.client = Mistral(api_key=api_key)

        self.set_debug(False)
        logging.info(f"Created Mistral Model. Using model: {self.model}")

    def _resolve_model_name(self, model_name: str) -> str:
        """
        Resolve model names to Mistral model IDs.

        Args:
            model_name: Model identifier

        Returns:
            Full Mistral model ID (e.g., "mistral-medium-latest")
        """
        if not model_name:
            raise ValueError("Model name is required")

        # Check for alias
        if model_name in self.MODEL_ALIASES:
            resolved = self.MODEL_ALIASES[model_name]
            logging.debug(f"Resolved model alias '{model_name}' to '{resolved}'")
            return resolved

        # Use as-is
        return model_name

    def key(self, key: str):
        """Assign a new API key."""
        self.client = Mistral(api_key=key)

    @property
    def requires_evaluation(self) -> bool:
        """
        Whether this model requires harness evaluation.

        Returns:
            bool: True (Mistral models require evaluation)
        """
        return True

    def set_debug(self, debug: bool = True) -> None:
        """
        Enable or disable debug mode.

        Args:
            debug: Whether to enable debug mode (default: True)
        """
        self.debug = debug
        logging.info(f"Debug mode {'enabled' if debug else 'disabled'}")

    def prompt(self, prompt: str, schema: str = None, prompt_log: str = "",
               files: Optional[list] = None, timeout: int = 60,
               category: Optional[int] = None):
        """
        Send a prompt to the Mistral model and get a response.

        Args:
            prompt: The user prompt/query
            schema: Optional JSON schema for structured output
            prompt_log: Path to log the prompt (if not empty)
            files: List of expected output files (if any)
            timeout: Timeout in seconds for the API call (default: 60)
            category: Optional integer indicating the category/problem ID

        Returns:
            The model's response as text
        """
        if self.client is None:
            raise ValueError("Unable to detect Mistral Model")

        # Import and use ModelHelpers
        helper = ModelHelpers()
        system_prompt = helper.create_system_prompt(self.context, schema, category)

        # Use timeout from config if not specified
        if timeout == 60:
            timeout = config.get("MODEL_TIMEOUT", 60)

        # Determine if we're expecting a single file (direct text mode)
        expected_single_file = files and len(files) == 1 and schema is None
        expected_file_name = files[0] if expected_single_file else None

        if self.debug:
            logging.debug(f"Requesting prompt using the model: {self.model}")
            logging.debug(f"System prompt: {system_prompt}")
            logging.debug(f"User prompt: {prompt}")
            if files:
                logging.debug(f"Expected files: {files}")
                if expected_single_file:
                    logging.debug(f"Using direct text mode for single file: {expected_file_name}")
            logging.debug(f"Request parameters: model={self.model}, timeout={timeout}")

        # Create directories for prompt log if needed
        if prompt_log:
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(prompt_log), exist_ok=True)

                # Write to a temporary file first
                temp_log = f"{prompt_log}.tmp"
                with open(temp_log, "w+") as f:
                    f.write(system_prompt + "\n\n----------------------------------------\n" + prompt)

                # Atomic rename to final file
                os.replace(temp_log, prompt_log)
            except Exception as e:
                logging.error(f"Failed to write prompt log to {prompt_log}: {str(e)}")
                # Don't continue if we can't write the log file
                raise

        try:
            # Create a new chat completion
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096,
            )

            # Print response details if debug is enabled
            if self.debug:
                logging.debug(f"Response received:\n{response}")

            # Get the response content
            for choice in response.choices:
                message = choice.message
                if self.debug:
                    logging.debug(f"  - Message: {message.content}")

                content = message.content.strip()

                # Process the response using the default helper functions
                if expected_single_file:
                    # For direct text response (no schema), no JSON parsing needed
                    pass
                elif schema is not None and content.startswith('{') and content.endswith('}'):
                    # Fix common JSON formatting issues
                    content = helper.fix_json_formatting(content)

                # Call parse_model_response with the correct parameter order
                return helper.parse_model_response(content, files, expected_single_file)

        except Exception as e:
            # Raise a specific error like the internal implementations
            raise ValueError(f"Unable to get response from Mistral model: {str(e)}")
