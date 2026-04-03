"""
Comprehensive test suite for wElasticsearch library.
"""

import pytest


class TestWElasticsearchImport:
    """Test basic imports."""

    def test_import_main_class(self):
        from wElasticsearch import WElasticsearch

        assert WElasticsearch is not None

    def test_import_index_manager(self):
        from wElasticsearch import IndexManager

        assert IndexManager is not None

    def test_import_query_builder(self):
        from wElasticsearch import QueryBuilder

        assert QueryBuilder is not None

    def test_version(self):
        import wElasticsearch

        assert wElasticsearch.__version__ == "1.0.0"


class TestExceptions:
    """Test exception hierarchy."""

    def test_welasticsearch_error(self):
        from wElasticsearch import WElasticsearchError

        with pytest.raises(WElasticsearchError):
            raise WElasticsearchError("test")

    def test_connection_error(self):
        from wElasticsearch import ConnectionError

        with pytest.raises(ConnectionError):
            raise ConnectionError("test")

    def test_query_error(self):
        from wElasticsearch import QueryError

        with pytest.raises(QueryError):
            raise QueryError("test")

    def test_validation_error(self):
        from wElasticsearch import ValidationError

        with pytest.raises(ValidationError):
            raise ValidationError("test")

    def test_hierarchy(self):
        from wElasticsearch import WElasticsearchError, ConnectionError

        assert issubclass(ConnectionError, WElasticsearchError)


class TestQueryBuilder:
    """Test QueryBuilder for Elasticsearch queries."""

    def test_fluent_api(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder("users")
        assert qb is not None

    def test_match_query(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder("users").match("name", "John")
        query, _ = qb.build()
        assert "match" in query

    def test_term_query(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder("users").term("status", "active")
        query, _ = qb.build()
        assert "term" in query

    def test_range_query(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder("users").range("age", gte=18)
        query, _ = qb.build()
        assert "range" in query

    def test_bool_query(self):
        from wElasticsearch import QueryBuilder

        qb = (
            QueryBuilder("users")
            .must("status", "active")
            .must_not("deleted", True)
            .should("verified", True)
        )
        query, _ = qb.build()
        assert "bool" in query

    def test_pagination(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder("users").from_(0).size(10)
        query, _ = qb.build()
        assert "from" in query
        assert "size" in query

    def test_sort(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder("users").sort("name", order="asc")
        query, _ = qb.build()
        assert "sort" in query


class TestIndexManager:
    """Test IndexManager functionality."""

    def test_init(self):
        from wElasticsearch import IndexManager

        im = IndexManager(hosts=["localhost:9200"])
        assert im is not None

    def test_create_index_params(self):
        from wElasticsearch import IndexManager

        im = IndexManager(hosts=["localhost:9200"])

        settings = {"number_of_shards": 3, "number_of_replicas": 1}
        mappings = {
            "properties": {"name": {"type": "text"}, "age": {"type": "integer"}}
        }

        result = im._build_create_params("test_index", settings, mappings)
        assert "index" in result
        assert "settings" in result
        assert "mappings" in result
