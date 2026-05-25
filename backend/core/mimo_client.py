"""OpenAI-compatible MiMo client wrapper.

The demo does not require credentials. Set MIMO_API_KEY and MIMO_BASE_URL to
switch from deterministic local mode to live MiMo calls.
"""
from __future__ import annotations
from typing import Any, Dict
import os, httpx

class MiMoClient:
    def __init__(self):
        self.api_key = os.getenv("MIMO_API_KEY") or os.getenv("XIAOMI_API_KEY")
        self.base_url = os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
        self.model = os.getenv("MIMO_MODEL", "mimo-v2.5-pro")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def chat(self, prompt: str, max_tokens: int = 1200) -> Dict[str, Any]:
        if not self.enabled:
            return {"mode": "local", "content": prompt[:240], "usage": {"total_tokens": len(prompt.split()) * 3}}
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(
                f"{self.base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
            )
            res.raise_for_status()
            return res.json()
