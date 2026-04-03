from pydantic import BaseModel
from wElasticsearch import WElasticsearch, IndexManager

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
    im = IndexManager(client)
    im.create_index(
        "users",
        mappings={
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "text"},
                "email": {"type": "keyword"},
            }
        },
    )
    print("Index created: users")
    client.close()


if __name__ == "__main__":
    main()
