import pytest
from wElasticsearch.types.mappings import MappingBuilder


class TestMappings:
    def test_text_field(self):
        mb = MappingBuilder()
        result = mb.text("title").build()
        assert "text" in result

    def test_keyword_field(self):
        mb = MappingBuilder()
        result = mb.keyword("status").build()
        assert "keyword" in result

    def test_integer_field(self):
        mb = MappingBuilder()
        result = mb.integer("age").build()
        assert "integer" in result

    def test_date_field(self):
        mb = MappingBuilder()
        result = mb.date("created_at").build()
        assert "date" in result
