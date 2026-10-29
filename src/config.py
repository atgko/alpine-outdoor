"""All model names, prices and run settings live here, in one place.

API keys are never stored here. They come from environment variables
(ANTHROPIC_API_KEY, GEMINI_API_KEY) and are never written to files or logs.
"""

# Model aliases used on the command line (--model small | large).
MODELS = {
    "small": {"provider": "anthropic", "name": "claude-haiku-5-5"},
    "large": {"provider": "anthropic", "name": "claude-opus-5-5"},
    # Gemini is added only after the current Google docs are checked and the
    # team confirms model names and free tier limits.
}

# USD per million tokens (input, output). Source: Anthropic pricing table,
# cached 2026-10-06. Used for approximate cost only.
PRICES_PER_MTOK = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-opus-5-5": (4.00, 20.00),
}

# Effort is set explicitly because both models default to "medium".
EFFORT = "medium"
MAX_TOKENS = 8000

# Rate limit handling: our own retry loop so every retry is counted and logged.
MAX_RETRIES = 4
BACKOFF_BASE_SECONDS = 2.0
BACKOFF_MAX_SECONDS = 60.0
DELAY_BETWEEN_CALLS_SECONDS = 1.0

# Spend guard: runs above this many estimated calls need --yes.
CONFIRM_ABOVE_CALLS = 200
