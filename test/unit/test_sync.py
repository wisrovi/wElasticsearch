import pytest
from wElasticsearch.core.index import IndexManager


class TestIndexManager:
    def test_import(self):
        from wElasticsearch.core.index import IndexManager

        assert IndexManager is not None

    def test_create_index(self):
        from wElasticsearch.core.index import IndexManager

        manager = IndexManager(client=None, index_name="test")
        assert manager.index_name == "test"
