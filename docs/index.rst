wElasticsearch Documentation
============================

|Version| |License| |Python|

wElasticsearch is a Python library that provides a high-level interface for Elasticsearch operations.
It simplifies working with Elasticsearch clusters, indices, and documents.

.. |Version| image:: https://img.shields.io/pypi/v/wElasticsearch.svg
   :target: https://pypi.org/project/wElasticsearch/
   :alt: PyPI Version

.. |License| image:: https://img.shields.io/pypi/l/wElasticsearch.svg
   :target: https://pypi.org/project/wElasticsearch/
   :alt: License

.. |Python| image:: https://img.shields.io/pypi/pyversions/wElasticsearch.svg
   :target: https://pypi.org/project/wElasticsearch/
   :alt: Python Versions

Quick Start
-----------

.. code-block:: bash

   pip install wElasticsearch

.. code-block:: python

   from wElasticsearch import Elasticsearch

   es = Elasticsearch(hosts=["http://localhost:9200"])
   result = es.search(index="my-index", body={"query": {"match_all": {}}})

Key Capabilities
----------------

- **Document Operations** - Index, update, and delete documents
- **Search API** - Full-text search with aggregations
- **Index Management** - Create and manage indices
- **Bulk Operations** - Efficient bulk importing
- **Type Safety** - Pydantic models for documents

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started/index
   api_reference/index
   tutorials/index
   faq
   glossary

.. toctree::
   :maxdepth: 1
   :caption: Additional

   License <license>
   bibliography

.. toctree::
   :maxdepth: 1
   :caption: External Links

   GitHub <https://github.com/wisrovi/wElasticsearch>
   PyPI <https://pypi.org/project/wElasticsearch/>
   LinkedIn <https://www.linkedin.com/in/william-steve-rodriguez-villamizar>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`