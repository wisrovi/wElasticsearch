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


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    client = WElasticsearch(**ES_CONFIG)

    user = User(id=1, name="John", email="john@example.com")
    order = {"id": 1, "user_id": 1, "amount": 100.0, "user_name": "John"}

    client.insert("users", user.model_dump(), id="1")
    client.insert("orders", order, id="1")

    results = client.search("orders", {"query": {"match": {"user_name": "John"}}})
    print(f"Join-style search: {results['hits']['total']['value']} results")

    client.close()


if __name__ == "__main__":
    main()
