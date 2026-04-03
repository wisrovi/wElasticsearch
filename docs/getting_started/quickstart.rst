Quickstart
===========

This guide will help you get started with wElasticsearch quickly.

Basic Usage
-----------

.. code-block:: python

    from wElasticsearch import WElasticsearch

    es = WElasticsearch(
        hosts=["http://localhost:9200"],
        basic_auth=("elastic", "your-password")
    )

    result = es.search(index="my-index", query={"match_all": {}})
    print(result)

Index Documents
---------------

.. code-block:: python

    from pydantic import BaseModel

    class Document(BaseModel):
        title: str
        content: str
        author: str

    doc = Document(title="My Document", content="Hello World", author="John")
    es.index(index="my-index", document=doc)

Search Documents
-----------------

.. code-block:: python

    results = es.search(
        index="my-index",
        query={"match": {"title": "Document"}}
    )

    for hit in results["hits"]["hits"]:
        print(hit["_source"])

Using IndexManager
------------------

.. code-block:: python

    from wElasticsearch import IndexManager

    im = IndexManager(hosts=["http://localhost:9200"])

    im.create_index(
        index="my-index",
        mappings={"properties": {"title": {"type": "text"}}},
        settings={"number_of_shards": 1}
    )