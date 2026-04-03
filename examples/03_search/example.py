from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


def main():
    client = WElasticsearch(**ES_CONFIG)
    results = client.search("users", {"query": {"match_all": {}}})
    print(f"Found {results['hits']['total']['value']} documents")
    client.close()


if __name__ == "__main__":
    main()
