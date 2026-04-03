from typing import Any, Optional


class QueryBuilder:
    def __init__(self):
        self._query: dict[str, Any] = {}

    def match_all(self) -> "QueryBuilder":
        self._query = {"query": {"match_all": {}}}
        return self

    def match_none(self) -> "QueryBuilder":
        self._query = {"query": {"match_none": {}}}
        return self

    def term(self, field: str, value: Any) -> "QueryBuilder":
        if "query" not in self._query:
            self._query["query"] = {"bool": {"must": []}}
        if "bool" not in self._query["query"]:
            self._query["query"] = {"bool": {"must": []}}
        self._query["query"]["bool"]["must"].append({"term": {field: value}})
        return self

    def terms(self, field: str, values: list[Any]) -> "QueryBuilder":
        if "query" not in self._query:
            self._query["query"] = {"bool": {"must": []}}
        self._query["query"]["bool"]["must"].append({"terms": {field: values}})
        return self

    def match(self, field: str, value: str, operator: str = "or") -> "QueryBuilder":
        if "query" not in self._query:
            self._query["query"] = {"bool": {"must": []}}
        self._query["query"]["bool"]["must"].append(
            {"match": {field: {"query": value, "operator": operator}}}
        )
        return self

    def multi_match(
        self, query: str, fields: list[str], operator: str = "or"
    ) -> "QueryBuilder":
        self._query["query"] = {
            "multi_match": {"query": query, "fields": fields, "operator": operator}
        }
        return self

    def range(
        self,
        field: str,
        gte: Optional[Any] = None,
        lte: Optional[Any] = None,
        gt: Optional[Any] = None,
        lt: Optional[Any] = None,
    ) -> "QueryBuilder":
        if "query" not in self._query:
            self._query["query"] = {"bool": {"must": []}}
        range_params: dict[str, Any] = {}
        if gte is not None:
            range_params["gte"] = gte
        if lte is not None:
            range_params["lte"] = lte
        if gt is not None:
            range_params["gt"] = gt
        if lt is not None:
            range_params["lt"] = lt
        self._query["query"]["bool"]["must"].append({"range": {field: range_params}})
        return self

    def bool(self) -> "QueryBuilder":
        self._query.setdefault("query", {}).setdefault("bool", {})
        return self

    def must(self, query: dict[str, Any]) -> "QueryBuilder":
        self._query.setdefault("query", {}).setdefault("bool", {}).setdefault(
            "must", []
        ).append(query)
        return self

    def must_not(self, query: dict[str, Any]) -> "QueryBuilder":
        self._query.setdefault("query", {}).setdefault("bool", {}).setdefault(
            "must_not", []
        ).append(query)
        return self

    def should(self, query: dict[str, Any]) -> "QueryBuilder":
        self._query.setdefault("query", {}).setdefault("bool", {}).setdefault(
            "should", []
        ).append(query)
        return self

    def filter(self, query: dict[str, Any]) -> "QueryBuilder":
        self._query.setdefault("query", {}).setdefault("bool", {}).setdefault(
            "filter", []
        ).append(query)
        return self

    def exists(self, field: str) -> "QueryBuilder":
        return self.must({"exists": {"field": field}})

    def missing(self, field: str) -> "QueryBuilder":
        return self.must_not({"exists": {"field": field}})

    def wildcard(self, field: str, value: str) -> "QueryBuilder":
        return self.must({"wildcard": {field: {"value": value}}})

    def prefix(self, field: str, value: str) -> "QueryBuilder":
        return self.must({"prefix": {field: {"value": value}}})

    def query_string(
        self, query: str, fields: Optional[list[str]] = None
    ) -> "QueryBuilder":
        q = {"query_string": {"query": query}}
        if fields:
            q["query_string"]["fields"] = fields
        return self.must(q)

    def nested(self, path: str, query: dict[str, Any]) -> "QueryBuilder":
        return self.must({"nested": {"path": path, "query": query}})

    def script(self, script: dict[str, Any]) -> "QueryBuilder":
        return self.must({"script": script})

    def from_size(self, from_: int = 0, size: int = 10) -> "QueryBuilder":
        self._query["from"] = from_
        self._query["size"] = size
        return self

    def sort(self, field: str, order: str = "asc") -> "QueryBuilder":
        self._query.setdefault("sort", []).append({field: {"order": order}})
        return self

    def source(
        self, includes: Optional[list[str]] = None, excludes: Optional[list[str]] = None
    ) -> "QueryBuilder":
        self._query["_source"] = {}
        if includes:
            self._query["_source"]["includes"] = includes
        if excludes:
            self._query["_source"]["excludes"] = excludes
        return self

    def highlight(
        self,
        fields: list[str],
        pre_tags: Optional[list[str]] = None,
        post_tags: Optional[list[str]] = None,
    ) -> "QueryBuilder":
        self._query["highlight"] = {"fields": {f: {} for f in fields}}
        if pre_tags:
            self._query["highlight"]["pre_tags"] = pre_tags
        if post_tags:
            self._query["highlight"]["post_tags"] = post_tags
        return self

    def aggregations(self, aggs: dict[str, Any]) -> "QueryBuilder":
        self._query["aggs"] = aggs
        return self

    def post_filter(self, query: dict[str, Any]) -> "QueryBuilder":
        self._query["post_filter"] = query
        return self

    def build(self) -> dict[str, Any]:
        return self._query

    def to_dict(self) -> dict[str, Any]:
        return self._query.copy()

    @classmethod
    def from_dict(cls, query: dict[str, Any]) -> "QueryBuilder":
        builder = cls()
        builder._query = query.copy()
        return builder
