Documents
=========

This tutorial covers document operations in wElasticsearch.

Setup
-----

.. code-block:: python

    from wElasticsearch import WElasticsearch

    es = WElasticsearch(hosts=["http://localhost:9200"])

Index a Document
----------------

.. code-block:: python

    from pydantic import BaseModel

    class Article(BaseModel):
        title: str
        content: str
        tags: list[str]
        published_at: str

    article = Article(
        title="Introduction to Elasticsearch",
        content="Elasticsearch is a distributed search engine...",
        tags=["elasticsearch", "search"],
        published_at="2024-01-01"
    )

    es.index(index="articles", document=article)

Get a Document
--------------

.. code-block:: python

    doc = es.get(index="articles", id="doc-id")
    print(doc["_source"])

Update a Document
-----------------

.. code-block:: python

    es.update(
        index="articles",
        id="doc-id",
        doc={"title": "Updated Title"}
    )

Delete a Document
-----------------

.. code-block:: python

    es.delete(index="articles", id="doc-id")