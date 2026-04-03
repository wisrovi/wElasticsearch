import os
import tempfile
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

    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
    temp_file.write("Temp data\n")
    temp_file.close()

    user = User(id=1, name="TempUser", email="temp@example.com")
    client.insert("users", user.model_dump(), id="1")
    results = client.search("users", {"query": {"match_all": {}}})
    print(f"Users: {results['hits']['total']['value']}")

    os.unlink(temp_file.name)
    client.close()


if __name__ == "__main__":
    main()
