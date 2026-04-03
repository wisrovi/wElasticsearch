from pydantic import BaseModel
from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
    "verify_certs": False,
}


class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


def main():
    client = WElasticsearch(**ES_CONFIG)

    employees = [
        {"id": 1, "name": "Alice", "department": "IT", "salary": 70000},
        {"id": 2, "name": "Bob", "department": "IT", "salary": 75000},
        {"id": 3, "name": "Charlie", "department": "HR", "salary": 65000},
    ]
    for emp in employees:
        client.insert("employees", emp, id=str(emp["id"]))

    result = client.search(
        "employees",
        {
            "query": {"match_all": {}},
            "size": 3,
            "sort": [{"salary": {"order": "desc"}}],
        },
    )
    print(f"Window function (sorted): {len(result['hits']['hits'])} employees")

    client.close()


if __name__ == "__main__":
    main()
