Bulk Operations
================

This tutorial covers bulk operations in wElasticsearch.

Bulk Indexing
-------------

.. code-block:: python

    from wElasticsearch import WElasticsearch

    es = WElasticsearch(hosts=["http://localhost:9200"])

    documents = [
        {"index": {"_index": "articles", "_id": "1"}},
        {"title": "Article 1", "content": "Content 1"},
        {"index": {"_index": "articles", "_id": "2"}},
        {"title": "Article 2", "content": "Content 2"},
    ]

    es.bulk(operations=documents)

Bulk Update and Delete
----------------------

.. code-block:: python

    operations = [
        {"update": {"_index": "articles", "_id": "1"}},
        {"doc": {"title": "Updated Title"}},
        {"delete": {"_index": "articles", "_id": "2"}},
    ]

    es.bulk(operations=operations)

Using Bulk with Pydantic Models
--------------------------------

.. code-block:: python

    from pydantic import BaseModel

    class Article(BaseModel):
        title: str
        content: str

    articles = [
        Article(title=f"Article {i}", content=f"Content {i}")
        for i in range(100)
    ]

    operations = []
    for i, article in enumerate(articles):
        operations.append({"index": {"_index": "articles", "_id": str(i)}})
        operations.append(article.model_dump())

    es.bulk(operations=operations)