from typing import Any, AsyncIterator

import httpx
import pytest

from src.webapp.app import app


class Client(httpx.AsyncClient):
    async def rpc(
        self,
        path: str,
        body: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> Any:
        resp = await self.post(
            path,
            headers=headers or {},
            json=body,
        )
        return resp.json()


@pytest.fixture()
async def cli() -> AsyncIterator[Client]:
    async with Client(app=app, base_url="https://sticker_api.test") as client:
        yield client
