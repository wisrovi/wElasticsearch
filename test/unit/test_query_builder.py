import pytest
from wElasticsearch.builders.query_builder import QueryBuilder


class TestQueryBuilder:
    def test_match_all(self):
        qb = QueryBuilder()
        result = qb.match_all().build()
        assert "match_all" in result

    def test_match(self):
        qb = QueryBuilder()
        result = qb.match("field", "value").build()
        assert "match" in result

    def test_term(self):
        qb = QueryBuilder()
        result = qb.term("field", "value").build()
        assert "term" in result

    def test_range(self):
        qb = QueryBuilder()
        result = qb.range("field", gte=1, lte=10).build()
        assert "range" in result
