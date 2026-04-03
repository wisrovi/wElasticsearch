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

    for i in range(1, 21):
        user = User(id=i, name=f"User{i}", email=f"user{i}@example.com")
        client.insert("users", user.model_dump(), id=str(i))

    page1 = client.search("users", {"query": {"match_all": {}}, "from": 0, "size": 5})
    print(f"Page 1: {page1['hits']['total']['value']} docs")

    page2 = client.search("users", {"query": {"match_all": {}}, "from": 5, "size": 5})
    print(f"Page 2: {page2['hits']['total']['value']} docs")

    client.close()


if __name__ == "__main__":
    main()
