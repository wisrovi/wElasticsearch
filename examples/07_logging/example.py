import logging
from pydantic import BaseModel
from wElasticsearch import WElasticsearch

logging.basicConfig(level=logging.DEBUG)

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


class User(BaseModel):
    id: int
    name: str
    email: str


def main():
    client = WElasticsearch(**ES_CONFIG, log_level=logging.DEBUG)

    user = User(id=1, name="LoggedUser", email="logged@example.com")
    client.insert("users", user.model_dump(), id="1")
    print("Logged operation completed")

    client.close()


if __name__ == "__main__":
    main()
