Search
======

This tutorial covers search operations in wElasticsearch.

Basic Search
------------

.. code-block:: python

    from wElasticsearch import WElasticsearch

    es = WElasticsearch(hosts=["http://localhost:9200"])

    results = es.search(
        index="articles",
        query={"match": {"title": "Elasticsearch"}}
    )

    for hit in results["hits"]["hits"]:
        print(hit["_source"])

Bool Query
----------

.. code-block:: python

    results = es.search(
        index="articles",
        query={
            "bool": {
                "must": [
                    {"match": {"title": "search"}}
                ],
                "filter": [
                    {"term": {"status": "published"}}
                ]
            }
        }
    )

Aggregations
------------

.. code-block:: python

    results = es.search(
        index="articles",
        aggs={
            "tags": {
                "terms": {"field": "tags.keyword"}
            }
        },
        size=0
    )

    print(results["aggregations"]["tags"])

Pagination
----------

.. code-block:: python

    results = es.search(
        index="articles",
        from_=0,
        size=10,
        query={"match_all": {}}
    )