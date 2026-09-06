"""HTTP client for SocialBee API."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_BASE = "https://api.socialbee.io/v1"

class SocialBeeClient:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_BASE).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-SocialBee-Connector/1.0.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/profiles", headers=self.headers)
                if resp.status_code in (200, 201):
                    return {"status": "ok", "data": resp.json()}
                return {"status": "error", "error": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def list_profiles(self) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/profiles", headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", data) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            return []

    async def list_categories(self) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/categories", headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", data) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            return []

    async def list_posts(self, category_id: Optional[str] = None, limit: int = 20) -> list[dict[str, Any]]:
        params = {"limit": limit}
        if category_id:
            params["category_id"] = category_id
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/posts", headers=self.headers, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", data) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            return []

    async def create_post(self, category_id: str, text: str, profile_ids: list[str]) -> dict[str, Any]:
        payload = {"category_id": category_id, "text": text, "profiles": profile_ids}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.base_url}/posts", headers=self.headers, json=payload)
            return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status_code": resp.status_code}

    async def delete_post(self, post_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.delete(f"{self.base_url}/posts/{post_id}", headers=self.headers)
            return resp.status_code in (200, 204)
