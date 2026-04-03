class WElasticsearchError(Exception):
    pass


class ConnectionError(WElasticsearchError):
    pass


class DocumentNotFoundError(WElasticsearchError):
    pass


class IndexNotFoundError(WElasticsearchError):
    pass


class ValidationError(WElasticsearchError):
    pass


class BulkOperationError(WElasticsearchError):
    pass
