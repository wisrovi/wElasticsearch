from pydantic import BaseModel
from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


class User(BaseModel):
    id: int
    name: str
    email: str


def main():
    client = WElasticsearch(**ES_CONFIG)

    users = [
        {"id": 1, "name": "John", "email": "john@example.com"},
        {"id": 2, "name": "Jane", "email": "jane@example.com"},
    ]
    for u in users:
        client.insert("users", u, id=str(u["id"]))

    subquery = client.search(
        "users",
        {
            "query": {"match_all": {}},
            "size": 0,
            "aggs": {"max_id": {"max": {"field": "id"}}},
        },
    )
    max_id = subquery["aggregations"]["max_id"]["value"]
    print(f"Max ID from subquery: {max_id}")

    client.close()


if __name__ == "__main__":
    main()
