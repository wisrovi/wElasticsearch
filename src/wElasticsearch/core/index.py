from typing import Any, Optional
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from wElasticsearch.core.connection import ConnectionManager
from wElasticsearch.exceptions import IndexNotFoundError


class IndexManager:
    def __init__(self, connection: ConnectionManager):
        self._connection = connection

    @property
    def client(self) -> Elasticsearch:
        return self._connection.get_sync_client()

    async def get_async_client(self):
        return await self._connection.get_async_client()

    def create_index(
        self,
        index: str,
        mappings: Optional[dict[str, Any]] = None,
        settings: Optional[dict[str, Any]] = None,
        aliases: Optional[dict[str, Any]] = None,
        exist_ok: bool = True,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if settings:
            body["settings"] = settings
        if mappings:
            body["mappings"] = mappings
        if aliases:
            body["aliases"] = aliases
        if not exist_ok and self.exists(index):
            from wElasticsearch.exceptions import WElasticsearchError

            raise WElasticsearchError(f"Index '{index}' already exists")
        return self.client.indices.create(
            index=index, body=body if body else None, error_trace=True
        )

    async def create_index_async(
        self,
        index: str,
        mappings: Optional[dict[str, Any]] = None,
        settings: Optional[dict[str, Any]] = None,
        aliases: Optional[dict[str, Any]] = None,
        exist_ok: bool = True,
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        body: dict[str, Any] = {}
        if settings:
            body["settings"] = settings
        if mappings:
            body["mappings"] = mappings
        if aliases:
            body["aliases"] = aliases
        if not exist_ok and await self.exists_async(index):
            from wElasticsearch.exceptions import WElasticsearchError

            raise WElasticsearchError(f"Index '{index}' already exists")
        return await client.indices.create(index=index, body=body if body else None)

    def delete_index(self, index: str, ignore_missing: bool = False) -> dict[str, Any]:
        try:
            return self.client.indices.delete(index=index)
        except Exception as e:
            if not ignore_missing and "not_found" in str(e).lower():
                raise IndexNotFoundError(f"Index '{index}' not found")
            return {"acknowledged": True}

    async def delete_index_async(
        self, index: str, ignore_missing: bool = False
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        try:
            return await client.indices.delete(index=index)
        except Exception as e:
            if not ignore_missing and "not_found" in str(e).lower():
                raise IndexNotFoundError(f"Index '{index}' not found")
            return {"acknowledged": True}

    def exists(self, index: str) -> bool:
        return self.client.indices.exists(index=index)

    async def exists_async(self, index: str) -> bool:
        client = await self.get_async_client()
        return await client.indices.exists(index=index)

    def get_mapping(self, index: str) -> dict[str, Any]:
        if not self.exists(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return self.client.indices.get_mapping(index=index)

    async def get_mapping_async(self, index: str) -> dict[str, Any]:
        client = await self.get_async_client()
        if not await self.exists_async(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return await client.indices.get_mapping(index=index)

    def put_mapping(self, index: str, mappings: dict[str, Any]) -> dict[str, Any]:
        if not self.exists(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return self.client.indices.put_mapping(index=index, body=mappings)

    async def put_mapping_async(
        self, index: str, mappings: dict[str, Any]
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        if not await self.exists_async(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return await client.indices.put_mapping(index=index, body=mappings)

    def get_settings(self, index: str) -> dict[str, Any]:
        if not self.exists(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return self.client.indices.get_settings(index=index)

    async def get_settings_async(self, index: str) -> dict[str, Any]:
        client = await self.get_async_client()
        if not await self.exists_async(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return await client.indices.get_settings(index=index)

    def refresh(self, index: str) -> dict[str, Any]:
        if not self.exists(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return self.client.indices.refresh(index=index)

    async def refresh_async(self, index: str) -> dict[str, Any]:
        client = await self.get_async_client()
        if not await self.exists_async(index):
            raise IndexNotFoundError(f"Index '{index}' not found")
        return await client.indices.refresh(index=index)

    def list_indices(self) -> list[str]:
        return list(self.client.cat.indices(format="json"))

    async def list_indices_async(self) -> list[str]:
        client = await self.get_async_client()
        return list(await client.cat.indices(format="json"))
