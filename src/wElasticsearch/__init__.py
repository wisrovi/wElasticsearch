__version__ = "1.0.0"

from wElasticsearch.core.repository import WElasticsearch
from wElasticsearch.core.index import IndexManager
from wElasticsearch.builders.query_builder import QueryBuilder
from wElasticsearch.exceptions import (
    WElasticsearchError,
    ConnectionError,
    DocumentNotFoundError,
    IndexNotFoundError,
    ValidationError,
    BulkOperationError,
)

__all__ = [
    "__version__",
    "WElasticsearch",
    "IndexManager",
    "QueryBuilder",
    "WElasticsearchError",
    "ConnectionError",
    "DocumentNotFoundError",
    "IndexNotFoundError",
    "ValidationError",
    "BulkOperationError",
]
