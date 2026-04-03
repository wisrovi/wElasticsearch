import ssl
from typing import Optional, Union
from elasticsearch import Elasticsearch, AsyncElasticsearch
from elasticsearch.helpers import bulk, async_bulk

from wElasticsearch.exceptions import ConnectionError as WConnectionError


class ConnectionManager:
    def __init__(
        self,
        hosts: Union[str, list[str]] = "http://localhost:9200",
        verify_certs: bool = True,
        ca_certs: Optional[str] = None,
        client_cert: Optional[str] = None,
        client_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[tuple[str, str]] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_on_timeout: bool = True,
        use_async: bool = False,
    ):
        self.hosts = hosts
        self.verify_certs = verify_certs
        self.ca_certs = ca_certs
        self.client_cert = client_cert
        self.client_key = client_key
        self.username = username
        self.password = password
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_on_timeout = retry_on_timeout
        self.use_async = use_async
        self._sync_client: Optional[Elasticsearch] = None
        self._async_client: Optional[AsyncElasticsearch] = None

    def _build_ssl_context(self) -> Optional[ssl.SSLContext]:
        if not self.verify_certs:
            return None
        context = ssl.create_default_context(cafile=self.ca_certs)
        if self.client_cert and self.client_key:
            context.load_cert_chain(self.client_cert, self.client_key)
        return context

    def _get_client_params(self) -> dict:
        params = {
            "hosts": self.hosts,
            "verify_certs": self.verify_certs,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_on_timeout": self.retry_on_timeout,
        }
        if self.ca_certs or (self.client_cert and self.client_key):
            params["ssl_context"] = self._build_ssl_context()
        if self.username and self.password:
            params["basic_auth"] = (self.username, self.password)
        elif self.api_key:
            params["api_key"] = self.api_key
        return params

    def get_sync_client(self) -> Elasticsearch:
        if self._sync_client is None:
            try:
                params = self._get_client_params()
                self._sync_client = Elasticsearch(**params)
                self._sync_client.info()
            except Exception as e:
                raise WConnectionError(f"Failed to connect to Elasticsearch: {e}")
        return self._sync_client

    async def get_async_client(self) -> AsyncElasticsearch:
        if self._async_client is None:
            try:
                params = self._get_client_params()
                params["use_async"] = True
                self._async_client = AsyncElasticsearch(**params)
                await self._async_client.info()
            except Exception as e:
                raise WConnectionError(f"Failed to connect to Elasticsearch: {e}")
        return self._async_client

    def close(self):
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None
        if self._async_client:
            import asyncio

            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self._async_client.close())
            else:
                loop.run_until_complete(self._async_client.close())
            self._async_client = None

    async def close_async(self):
        if self._async_client:
            await self._async_client.close()
            self._async_client = None
