"""One client for every model call: `client.messages.create(**anthropic_style_request)`.

Models named `claude-*` go to the Anthropic API unchanged. Gemini models
(`gemini-*`) and Mistral models (`mistral-*`, `ministral-*`, `magistral-*`, ...)
go to that provider's OpenAI-compatible endpoint (free tiers), with the request
translated there and the response translated back into the Anthropic shape the
callers already read (`content` blocks, `stop_reason`, `usage`).

Translated: system prompt, text messages, max_tokens, temperature,
structured outputs (`output_config.format` -> `response_format` json_schema),
forced tool use (`tools` / `tool_choice` -> function calling), and
`thinking={"type": "disabled"}` (-> reasoning_effort "none" on Gemini models
that allow it; ignored on Mistral). Anything else is rejected rather than
silently dropped.

Free tiers limit request rates, so each provider's calls are spaced at least
<PROVIDER>_MIN_INTERVAL_S apart (GEMINI_..., MISTRAL_...) and retried with
backoff on 429/5xx, up to <PROVIDER>_MAX_RETRIES times with waits capped at
<PROVIDER>_MAX_BACKOFF_S. Under load Gemini's free tier answers 503 "high
demand" for minutes at a time, so unattended runs should raise the retry
budget (e.g. 20 retries x 60s ~= 20 minutes).
Errors that survive the retries are raised as LLMError with "Error code: N"
in the message, the same marker Anthropic's SDK uses.

This file is kept identical in rag-pipeline (scripts/llm_client.py) and
eval-harness (eval/llm_client.py): the deployed app must not depend on the
harness. tests/test_llm_client.py in each repo fails if the copies drift.
"""
from __future__ import annotations

import json
import os
import random
import threading
import time
from types import SimpleNamespace
from typing import Any, Optional

import httpx

# provider -> model-name prefixes, endpoint, key variable, default spacing between calls
PROVIDERS = {
    "gemini": {
        "prefixes": ("gemini-",),
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "key_env": "GEMINI_API_KEY",
        "min_interval_s": 6.0,
    },
    "mistral": {
        "prefixes": ("mistral-", "ministral-", "magistral-", "open-mistral-", "codestral-", "devstral-", "pixtral-"),
        "base_url": "https://api.mistral.ai/v1",
        "key_env": "MISTRAL_API_KEY",
        "min_interval_s": 1.1,  # free tier: 1 request per second
    },
}
RETRY_STATUSES = {429, 500, 502, 503, 504}
FINISH_TO_STOP = {
    "stop": "end_turn",
    "length": "max_tokens",
    "tool_calls": "tool_use",
    "function_call": "tool_use",
    "content_filter": "refusal",
}
SUPPORTED_KEYS = {"model", "max_tokens", "system", "messages", "temperature",
                  "output_config", "tools", "tool_choice", "thinking"}


class LLMError(RuntimeError):
    pass


def provider_of(model: str) -> str:
    """'gemini', 'mistral', or 'anthropic' (everything else, e.g. claude-*)."""
    for name, cfg in PROVIDERS.items():
        if model.startswith(cfg["prefixes"]):
            return name
    return "anthropic"


def _strip_additional_properties(schema: Any) -> Any:
    """Gemini's schema subset rejects `additionalProperties`; the shape is
    still enforced by `required` + `properties`. Stripped for every provider so
    one request shape behaves the same everywhere."""
    if isinstance(schema, dict):
        return {k: _strip_additional_properties(v) for k, v in schema.items() if k != "additionalProperties"}
    if isinstance(schema, list):
        return [_strip_additional_properties(v) for v in schema]
    return schema


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for block in content:
        if block.get("type") != "text":
            raise LLMError(f"unsupported content block type {block.get('type')!r}")
        parts.append(block["text"])
    return "".join(parts)


def to_openai_request(request: dict) -> dict:
    unknown = set(request) - SUPPORTED_KEYS
    if unknown:
        raise LLMError(f"request keys not supported off Anthropic: {sorted(unknown)}")
    model = request["model"]
    messages = []
    if request.get("system"):
        messages.append({"role": "system", "content": _text_of(request["system"])})
    for m in request["messages"]:
        messages.append({"role": m["role"], "content": _text_of(m["content"])})

    out: dict[str, Any] = {"model": model, "messages": messages, "max_tokens": request["max_tokens"]}
    if "temperature" in request:
        out["temperature"] = request["temperature"]

    thinking = request.get("thinking")
    if (thinking and thinking.get("type") == "disabled" and provider_of(model) == "gemini"
            and "-pro" not in model):
        out["reasoning_effort"] = "none"  # Gemini Pro models cannot turn thinking off

    fmt = (request.get("output_config") or {}).get("format")
    if fmt:
        if fmt.get("type") != "json_schema":
            raise LLMError(f"unsupported output format {fmt.get('type')!r}")
        out["response_format"] = {"type": "json_schema", "json_schema": {
            "name": "output", "schema": _strip_additional_properties(fmt["schema"])}}
        if provider_of(model) == "mistral":
            # Without strict, Ministral models were seen returning a bare list
            # instead of the schema's top-level object.
            out["response_format"]["json_schema"]["strict"] = True

    if request.get("tools"):
        out["tools"] = [{"type": "function", "function": {
            "name": t["name"],
            "description": t.get("description", ""),
            "parameters": _strip_additional_properties(t["input_schema"]),
        }} for t in request["tools"]]
    choice = request.get("tool_choice")
    if choice:
        if choice.get("type") == "tool":
            out["tool_choice"] = {"type": "function", "function": {"name": choice["name"]}}
        elif choice.get("type") == "any":
            out["tool_choice"] = "required"
        else:
            out["tool_choice"] = "auto"
    return out


def from_openai_response(data: dict, model: str) -> SimpleNamespace:
    if not data.get("choices"):
        raise LLMError(f"Error code: 200 - no choices in response: {json.dumps(data)[:500]}")
    choice = data["choices"][0]
    message = choice.get("message") or {}
    content = []
    if message.get("content"):
        content.append(SimpleNamespace(type="text", text=message["content"]))
    for call in message.get("tool_calls") or []:
        try:
            args = json.loads(call["function"].get("arguments") or "{}")
        except json.JSONDecodeError as exc:
            raise LLMError(f"tool call arguments are not JSON: {exc}") from exc
        content.append(SimpleNamespace(type="tool_use", id=call.get("id"),
                                       name=call["function"]["name"], input=args))
    usage = data.get("usage") or {}
    return SimpleNamespace(
        model=model,
        content=content,
        stop_reason=FINISH_TO_STOP.get(choice.get("finish_reason"), choice.get("finish_reason")),
        usage=SimpleNamespace(
            input_tokens=usage.get("prompt_tokens", 0),
            # Thinking may be reported separately; count it, as Anthropic's usage does.
            output_tokens=(usage.get("completion_tokens", 0)
                           + (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0)),
        ),
    )


class _OpenAICompatBackend:
    def __init__(self, provider: str, http: Optional[httpx.Client] = None,
                 min_interval_s: Optional[float] = None, max_retries: Optional[int] = None,
                 max_backoff_s: Optional[float] = None, sleep=time.sleep):
        self.provider = provider
        self._cfg = PROVIDERS[provider]
        env = provider.upper()
        self._http = http
        self.min_interval_s = (float(os.environ.get(f"{env}_MIN_INTERVAL_S", self._cfg["min_interval_s"]))
                               if min_interval_s is None else min_interval_s)
        self.max_retries = int(os.environ.get(f"{env}_MAX_RETRIES", "6")) if max_retries is None else max_retries
        self.max_backoff_s = (float(os.environ.get(f"{env}_MAX_BACKOFF_S", "60"))
                              if max_backoff_s is None else max_backoff_s)
        self._sleep = sleep
        self._lock = threading.Lock()
        self._last_call = 0.0

    def _client(self) -> httpx.Client:
        if self._http is None:
            key = os.environ.get(self._cfg["key_env"])
            if not key:
                raise LLMError(f"Error code: 401 - {self._cfg['key_env']} is not set")
            self._http = httpx.Client(base_url=self._cfg["base_url"], timeout=180,
                                      headers={"Authorization": f"Bearer {key}"})
        return self._http

    def _wait_turn(self) -> None:
        with self._lock:
            wait = self._last_call + self.min_interval_s - time.monotonic()
            if wait > 0:
                self._sleep(wait)
            self._last_call = time.monotonic()

    def create(self, **request) -> SimpleNamespace:
        body = to_openai_request(request)
        for attempt in range(self.max_retries + 1):
            self._wait_turn()
            try:
                resp = self._client().post("/chat/completions", json=body)
            except httpx.TransportError as exc:
                if attempt == self.max_retries:
                    raise LLMError(f"Error code: transport - {exc}") from exc
                self._sleep(min(self.max_backoff_s, 2 ** attempt) + random.random())
                continue
            if resp.status_code == 200:
                return from_openai_response(resp.json(), request["model"])
            if resp.status_code in RETRY_STATUSES and attempt < self.max_retries:
                retry_after = resp.headers.get("retry-after")
                delay = float(retry_after) if retry_after and retry_after.replace(".", "").isdigit() \
                    else min(self.max_backoff_s, 2 ** (attempt + 1))
                self._sleep(delay + random.random())
                continue
            raise LLMError(f"Error code: {resp.status_code} - {resp.text[:500]}")
        raise LLMError("Error code: retries exhausted")


class _Messages:
    def __init__(self, owner: "LLMClient"):
        self._owner = owner

    def create(self, **request):
        provider = provider_of(request["model"])
        if provider == "anthropic":
            return self._owner.anthropic().messages.create(**request)
        return self._owner.backend(provider).create(**request)


class LLMClient:
    """Drop-in for `anthropic.Anthropic()` as far as `.messages.create` goes;
    routes each call by its model name."""

    def __init__(self, backends: Optional[dict] = None, anthropic_client=None):
        self._backends = dict(backends or {})
        self._anthropic = anthropic_client
        self.messages = _Messages(self)

    def backend(self, provider: str) -> "_OpenAICompatBackend":
        if provider not in self._backends:
            self._backends[provider] = _OpenAICompatBackend(provider)
        return self._backends[provider]

    def anthropic(self):
        if self._anthropic is None:
            import anthropic  # only needed when a claude-* model is actually used

            self._anthropic = anthropic.Anthropic()
        return self._anthropic


_default: Optional[LLMClient] = None


def get_client() -> LLMClient:
    """Process-wide client, so each provider's rate-limit spacing is shared by every caller."""
    global _default
    if _default is None:
        _default = LLMClient()
    return _default
