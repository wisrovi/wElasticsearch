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

    client.update(
        "users",
        "1",
        {"doc": {"name": "John Updated", "email": "john.updated@example.com"}},
    )
    print("Document updated in transaction")

    result = client.get("users", "1")
    print(f"Updated doc: {result['_source']}")

    client.close()


if __name__ == "__main__":
    main()
