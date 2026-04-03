from pydantic import BaseModel
from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


class Product(BaseModel):
    id: int
    name: str
    price: float


def main():
    client = WElasticsearch(**ES_CONFIG)

    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 29.99},
        {"id": 3, "name": "Keyboard", "price": 89.99},
    ]
    for p in products:
        client.insert("products", p, id=str(p["id"]))

    avg_result = client.search(
        "products",
        {
            "query": {"match_all": {}},
            "size": 0,
            "aggs": {"avg_price": {"avg": {"field": "price"}}},
        },
    )
    avg_price = avg_result["aggregations"]["avg_price"]["value"]

    above_avg = client.search(
        "products", {"query": {"range": {"price": {"gt": avg_price}}}}
    )
    print(
        f"Products above average ({avg_price:.2f}): {above_avg['hits']['total']['value']}"
    )

    client.close()


if __name__ == "__main__":
    main()
