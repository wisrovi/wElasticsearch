from pydantic import BaseModel
from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    client = WElasticsearch(**ES_CONFIG)

    orders = [{"id": i, "user_id": i, "amount": float(i * 10)} for i in range(1, 6)]
    for o in orders:
        client.insert("orders", o, id=str(o["id"]))

    result = client.search(
        "orders",
        {
            "query": {"match_all": {}},
            "size": 0,
            "aggs": {"total_amount": {"sum": {"field": "amount"}}},
        },
    )
    print(f"Total amount: {result['aggregations']['total_amount']['value']}")

    count_result = client.search("orders", {"query": {"match_all": {}}, "size": 0})
    print(f"Order count: {count_result['hits']['total']['value']}")

    client.close()


if __name__ == "__main__":
    main()
