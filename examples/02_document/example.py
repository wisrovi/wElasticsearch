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
    user = User(id=1, name="John", email="john@example.com")
    client.insert("users", user.model_dump(), id="1")
    print("Document inserted")
    client.close()


if __name__ == "__main__":
    main()
