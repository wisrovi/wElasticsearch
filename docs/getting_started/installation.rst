Installation
============

Requirements
------------

* Python 3.9+
* Elasticsearch cluster (self-hosted or cloud)

Install via pip
---------------

.. code-block:: bash

    pip install wElasticsearch

Install with development dependencies
-------------------------------------

.. code-block:: bash

    pip install wElasticsearch[dev]

Install from source
-------------------

.. code-block:: bash

    git clone https://github.com/wisrovi/wElasticsearch.git
    cd wElasticsearch
    pip install -e .

Dependencies
~~~~~~~~~~~~

Required dependencies:

* ``elasticsearch>=8.0.0`` - Official Elasticsearch Python client
* ``pydantic>=2.0.0`` - Data validation and settings management

Optional dependencies:

* ``pytest`` - Testing framework
* ``pytest-cov>=4.0.0`` - Coverage plugin
* ``pytest-asyncio`` - Async test support
* ``black`` - Code formatter
* ``mypy`` - Type checker
* ``ruff`` - Linter