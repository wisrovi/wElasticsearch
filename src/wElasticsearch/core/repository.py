from typing import Any, Optional, Type, TypeVar, Generic, Callable
from pydantic import BaseModel

from wElasticsearch.core.connection import ConnectionManager
from wElasticsearch.core.index import IndexManager
from wElasticsearch.builders.query_builder import QueryBuilder
from wElasticsearch.types.mappings import (
    model_to_mapping,
    get_model_id,
    document_to_dict,
)
from wElasticsearch.exceptions import (
    WElasticsearchError,
    DocumentNotFoundError,
    IndexNotFoundError,
    BulkOperationError,
    ValidationError,
)

T = TypeVar("T", bound=BaseModel)


class WElasticsearch:
    def __init__(
        self,
        hosts: str = "http://localhost:9200",
        **kwargs,
    ):
        self._connection = ConnectionManager(hosts=hosts, **kwargs)
        self._index_manager = IndexManager(self._connection)

    @property
    def connection(self) -> ConnectionManager:
        return self._connection

    @property
    def index(self) -> IndexManager:
        return self._index_manager

    @property
    def client(self):
        return self._connection.get_sync_client()

    def get_async_client(self):
        return self._connection.get_async_client()

    def index_document(
        self,
        index: str,
        document: BaseModel,
        id: Optional[str] = None,
        routing: Optional[str] = None,
        refresh: Optional[bool] = None,
    ) -> dict[str, Any]:
        doc_id = id or get_model_id(document)
        body = document.model_dump()
        return self.client.index(
            index=index,
            id=doc_id,
            document=body,
            routing=routing,
            refresh=refresh,
        )

    async def index_document_async(
        self,
        index: str,
        document: BaseModel,
        id: Optional[str] = None,
        routing: Optional[str] = None,
        refresh: Optional[bool] = None,
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        doc_id = id or get_model_id(document)
        body = document.model_dump()
        return await client.index(
            index=index,
            id=doc_id,
            document=body,
            routing=routing,
            refresh=refresh,
        )

    def get_document(
        self,
        index: str,
        id: str,
        routing: Optional[str] = None,
    ) -> dict[str, Any]:
        try:
            return self.client.get(index=index, id=id, routing=routing)
        except Exception as e:
            if "not_found" in str(e).lower():
                raise DocumentNotFoundError(
                    f"Document with id '{id}' not found in index '{index}'"
                )
            raise

    async def get_document_async(
        self,
        index: str,
        id: str,
        routing: Optional[str] = None,
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        try:
            return await client.get(index=index, id=id, routing=routing)
        except Exception as e:
            if "not_found" in str(e).lower():
                raise DocumentNotFoundError(
                    f"Document with id '{id}' not found in index '{index}'"
                )
            raise

    def get_document_as(
        self,
        index: str,
        id: str,
        model: Type[T],
        routing: Optional[str] = None,
    ) -> T:
        result = self.get_document(index, id, routing)
        return model(**result["_source"])

    async def get_document_as_async(
        self,
        index: str,
        id: str,
        model: Type[T],
        routing: Optional[str] = None,
    ) -> T:
        result = await self.get_document_async(index, id, routing)
        return model(**result["_source"])

    def delete_document(
        self,
        index: str,
        id: str,
        routing: Optional[str] = None,
        refresh: Optional[bool] = None,
    ) -> dict[str, Any]:
        try:
            return self.client.delete(
                index=index, id=id, routing=routing, refresh=refresh
            )
        except Exception as e:
            if "not_found" in str(e).lower():
                raise DocumentNotFoundError(
                    f"Document with id '{id}' not found in index '{index}'"
                )
            raise

    async def delete_document_async(
        self,
        index: str,
        id: str,
        routing: Optional[str] = None,
        refresh: Optional[bool] = None,
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        try:
            return await client.delete(
                index=index, id=id, routing=routing, refresh=refresh
            )
        except Exception as e:
            if "not_found" in str(e).lower():
                raise DocumentNotFoundError(
                    f"Document with id '{id}' not found in index '{index}'"
                )
            raise

    def update_document(
        self,
        index: str,
        id: str,
        doc: dict[str, Any],
        routing: Optional[str] = None,
        refresh: Optional[bool] = None,
        upsert: bool = False,
    ) -> dict[str, Any]:
        return self.client.update(
            index=index,
            id=id,
            document={"doc": doc, "upsert": doc} if upsert else doc,
            routing=routing,
            refresh=refresh,
        )

    async def update_document_async(
        self,
        index: str,
        id: str,
        doc: dict[str, Any],
        routing: Optional[str] = None,
        refresh: Optional[bool] = None,
        upsert: bool = False,
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        return await client.update(
            index=index,
            id=id,
            document={"doc": doc, "upsert": doc} if upsert else doc,
            routing=routing,
            refresh=refresh,
        )

    def search(
        self,
        index: str,
        query: Optional[dict[str, Any]] = None,
        from_: int = 0,
        size: int = 10,
        routing: Optional[str] = None,
    ) -> dict[str, Any]:
        return self.client.search(
            index=index,
            query=query,
            from_=from_,
            size=size,
            routing=routing,
        )

    async def search_async(
        self,
        index: str,
        query: Optional[dict[str, Any]] = None,
        from_: int = 0,
        size: int = 10,
        routing: Optional[str] = None,
    ) -> dict[str, Any]:
        client = await self.get_async_client()
        return await client.search(
            index=index,
            query=query,
            from_=from_,
            size=size,
            routing=routing,
        )

    def search_as(
        self,
        index: str,
        model: Type[T],
        query: Optional[dict[str, Any]] = None,
        from_: int = 0,
        size: int = 10,
        routing: Optional[str] = None,
    ) -> list[T]:
        result = self.search(index, query, from_, size, routing)
        return [model(**hit["_source"]) for hit in result["hits"]["hits"]]

    async def search_as_async(
        self,
        index: str,
        model: Type[T],
        query: Optional[dict[str, Any]] = None,
        from_: int = 0,
        size: int = 10,
        routing: Optional[str] = None,
    ) -> list[T]:
        result = await self.search_async(index, query, from_, size, routing)
        return [model(**hit["_source"]) for hit in result["hits"]["hits"]]

    def count(
        self,
        index: str,
        query: Optional[dict[str, Any]] = None,
        routing: Optional[str] = None,
    ) -> int:
        return self.client.count(index=index, query=query, routing=routing)["count"]

    async def count_async(
        self,
        index: str,
        query: Optional[dict[str, Any]] = None,
        routing: Optional[str] = None,
    ) -> int:
        client = await self.get_async_client()
        result = await client.count(index=index, query=query, routing=routing)
        return result["count"]

    def bulk(
        self,
        operations: list[dict[str, Any]],
        raise_on_error: bool = True,
        raise_on_exception: bool = True,
    ) -> dict[str, Any]:
        try:
            success, failed = bulk(
                self.client,
                operations,
                raise_on_error=raise_on_error,
                raise_on_exception=raise_on_exception,
            )
            return {
                "success": success,
                "failed": failed,
                "errors": failed if raise_on_error else [],
            }
        except Exception as e:
            raise BulkOperationError(f"Bulk operation failed: {e}")

    async def bulk_async(
        self,
        operations: list[dict[str, Any]],
        raise_on_error: bool = True,
        raise_on_exception: bool = True,
    ) -> dict[str, Any]:
        from elasticsearch.helpers import async_bulk

        client = await self.get_async_client()
        try:
            success, failed = await async_bulk(
                client,
                operations,
                raise_on_error=raise_on_error,
                raise_on_exception=raise_on_exception,
            )
            return {
                "success": success,
                "failed": failed,
                "errors": failed if raise_on_error else [],
            }
        except Exception as e:
            raise BulkOperationError(f"Bulk operation failed: {e}")

    def bulk_index(
        self,
        index: str,
        documents: list[BaseModel],
        id_field: str = "id",
    ) -> dict[str, Any]:
        operations = []
        for doc in documents:
            doc_data = document_to_dict(doc, id_field)
            operations.append(
                {
                    "_index": index,
                    "_id": doc_data.get("_id"),
                    "_source": doc_data["_source"],
                }
            )
        return self.bulk(operations)

    async def bulk_index_async(
        self,
        index: str,
        documents: list[BaseModel],
        id_field: str = "id",
    ) -> dict[str, Any]:
        operations = []
        for doc in documents:
            doc_data = document_to_dict(doc, id_field)
            operations.append(
                {
                    "_index": index,
                    "_id": doc_data.get("_id"),
                    "_source": doc_data["_source"],
                }
            )
        return await self.bulk_async(operations)

    def create_model_index(
        self,
        index: str,
        model: Type[BaseModel],
        settings: Optional[dict[str, Any]] = None,
        aliases: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        mappings = model_to_mapping(model, index)
        return self.index.create_index(index, mappings, settings, aliases)

    async def create_model_index_async(
        self,
        index: str,
        model: Type[BaseModel],
        settings: Optional[dict[str, Any]] = None,
        aliases: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        mappings = model_to_mapping(model, index)
        return await self.index.create_index_async(index, mappings, settings, aliases)

    def scroll(
        self,
        index: str,
        query: Optional[dict[str, Any]] = None,
        scroll: str = "5m",
        size: int = 1000,
    ) -> list[dict[str, Any]]:
        response = self.client.search(
            index=index, query=query, size=size, scroll=scroll
        )
        scroll_id = response["_scroll_id"]
        hits = list(response["hits"]["hits"])
        while response["hits"]["hits"]:
            response = self.client.scroll(scroll_id=scroll_id, scroll=scroll)
            hits.extend(response["hits"]["hits"])
        return hits

    async def scroll_async(
        self,
        index: str,
        query: Optional[dict[str, Any]] = None,
        scroll: str = "5m",
        size: int = 1000,
    ) -> list[dict[str, Any]]:
        client = await self.get_async_client()
        response = await client.search(
            index=index, query=query, size=size, scroll=scroll
        )
        scroll_id = response["_scroll_id"]
        hits = list(response["hits"]["hits"])
        while response["hits"]["hits"]:
            response = await client.scroll(scroll_id=scroll_id, scroll=scroll)
            hits.extend(response["hits"]["hits"])
        return hits

    def close(self):
        self._connection.close()

    async def close_async(self):
        await self._connection.close_async()
