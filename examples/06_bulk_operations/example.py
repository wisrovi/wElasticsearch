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
        {"id": i, "name": f"BulkUser{i}", "email": f"bulk{i}@example.com"}
        for i in range(1, 11)
    ]
    client.bulk_index("users", users)
    print(f"Bulk indexed {len(users)} documents")

    client.close()


if __name__ == "__main__":
    main()
