import pytest


class TestWElasticsearchImport:
    def test_import(self):
        from wElasticsearch import WElasticsearch

        assert WElasticsearch is not None

    def test_version(self):
        import wElasticsearch

        assert wElasticsearch.__version__ == "1.0.0"


class TestQueryBuilder:
    def test_import(self):
        from wElasticsearch import QueryBuilder

        qb = QueryBuilder()
        assert qb is not None


class TestExceptions:
    def test_import(self):
        from wElasticsearch import WElasticsearchError

        with pytest.raises(WElasticsearchError):
            raise WElasticsearchError("test")
