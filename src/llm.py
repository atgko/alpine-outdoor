"""Provider wrapper. One call() for every provider, with counted retries.

The SDK's own retries are turned off (max_retries=0) so that every rate limit
or API error passes through our loop and is recorded in `errors`. Nothing is
silently dropped: a call that still fails after MAX_RETRIES returns ok=False.
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

from src import config


@dataclass(frozen=True)
class LLMResponse:
    ok: bool
    text: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_seconds: float = 0.0
    stop_reason: str | None = None
    attempts: int = 0
    errors: tuple[str, ...] = ()  # every failed attempt, including retried ones
    request_id: str | None = None

    @property
    def cost_usd(self) -> float | None:
        prices = config.PRICES_PER_MTOK.get(self.model)
        if prices is None:
            return None
        return (self.input_tokens * prices[0] + self.output_tokens * prices[1]) / 1_000_000


@dataclass
class AnthropicClient:
    model: str
    effort: str = config.EFFORT
    max_tokens: int = config.MAX_TOKENS
    delay_seconds: float = config.DELAY_BETWEEN_CALLS_SECONDS
    provider: str = "anthropic"
    _client: object = field(default=None, repr=False)

    def _sdk(self):
        if self._client is None:
            import anthropic  # imported lazily so tests run without the SDK
            self._client = anthropic.Anthropic(max_retries=0)  # key from ANTHROPIC_API_KEY
        return self._client

    def call(self, system: str, user: str) -> LLMResponse:
        import anthropic

        errors: list[str] = []
        for attempt in range(1, config.MAX_RETRIES + 2):
            time.sleep(self.delay_seconds)
            start = time.monotonic()
            try:
                msg = self._sdk().messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    output_config={"effort": self.effort},
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
            except anthropic.RateLimitError as exc:
                errors.append(f"attempt {attempt}: rate_limit 429")
                _backoff(attempt, exc.response.headers.get("retry-after"))
                continue
            except anthropic.APIStatusError as exc:
                errors.append(f"attempt {attempt}: api_error {exc.status_code}")
                if exc.status_code < 500:  # 4xx other than 429 will not succeed on retry
                    break
                _backoff(attempt, None)
                continue
            except anthropic.APIConnectionError as exc:  # includes timeouts
                errors.append(f"attempt {attempt}: connection_error {type(exc).__name__}")
                _backoff(attempt, None)
                continue
            text = "".join(b.text for b in msg.content if b.type == "text")
            ok = msg.stop_reason == "end_turn"
            if not ok:
                errors.append(f"attempt {attempt}: stop_reason {msg.stop_reason}")
            return LLMResponse(
                ok=ok, text=text, provider=self.provider, model=self.model,
                input_tokens=msg.usage.input_tokens, output_tokens=msg.usage.output_tokens,
                latency_seconds=round(time.monotonic() - start, 3), stop_reason=msg.stop_reason,
                attempts=attempt, errors=tuple(errors), request_id=getattr(msg, "_request_id", None),
            )
        return LLMResponse(ok=False, text="", provider=self.provider, model=self.model,
                           attempts=len(errors), errors=tuple(errors))


def _backoff(attempt: int, retry_after: str | None) -> None:
    if retry_after and retry_after.replace(".", "", 1).isdigit():
        delay = float(retry_after)
    else:
        delay = config.BACKOFF_BASE_SECONDS * 2 ** (attempt - 1) + random.uniform(0, 1)
    time.sleep(min(delay, config.BACKOFF_MAX_SECONDS))


def make_client(alias: str):
    """Build a client from a config alias such as 'small' or 'large'."""
    spec = config.MODELS[alias]
    if spec["provider"] == "anthropic":
        return AnthropicClient(model=spec["name"])
    raise ValueError(f"provider not configured: {spec['provider']}")
