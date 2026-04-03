import pytest
from wElasticsearch.core.connection import ConnectionManager


class TestConnectionManager:
    def test_import(self):
        from wElasticsearch.core.connection import ConnectionManager

        assert ConnectionManager is not None
