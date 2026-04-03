FAQ
===

Frequently Asked Questions about wElasticsearch.

General
-------

What is wElasticsearch?
~~~~~~~~~~~~~~~~~~~~~~~

wElasticsearch is a Python ORM library for Elasticsearch that provides Pydantic-based document modeling, index management, and search operations.

What Python versions are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wElasticsearch supports Python 3.9 and later.

Connection
----------

How do I connect to Elasticsearch?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wElasticsearch import WElasticsearch

    es = WElasticsearch(
        hosts=["http://localhost:9200"],
        basic_auth=("elastic", "password")
    )

How do I connect to Elastic Cloud?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    es = WElasticsearch(
        cloud_id="cluster-name:xxxx",
        basic_auth=("elastic", "password")
    )

Documents
---------

Do I need to define Pydantic models?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using Pydantic models provides type validation, auto-completion, and easy serialization, but direct dictionaries are also supported.

How do I handle nested documents?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define nested structures in your Pydantic model:

.. code-block:: python

    from pydantic import BaseModel
    from typing import List

    class Author(BaseModel):
        name: str
        email: str

    class Article(BaseModel):
        title: str
        authors: List[Author]

Errors
------

What exceptions does wElasticsearch raise?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``WElasticsearchError`` - Base exception
- ``ConnectionError`` - Connection failures
- ``DocumentNotFoundError`` - Document not found
- ``IndexNotFoundError`` - Index not found
- ``ValidationError`` - Data validation errors
- ``BulkOperationError`` - Bulk operation failures