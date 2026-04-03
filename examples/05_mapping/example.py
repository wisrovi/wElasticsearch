from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


def main():
    client = WElasticsearch(**ES_CONFIG)
    mappings = {
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "text", "analyzer": "standard"},
            "email": {"type": "keyword"},
            "created_at": {"type": "date"},
        }
    }
    client.create_index("users_new", mappings=mappings)
    print("Index with mapping created")
    client.close()


if __name__ == "__main__":
    main()
