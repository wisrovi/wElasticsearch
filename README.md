# wElasticsearch

**Elasticsearch ORM library with Pydantic support - type-safe document operations**

High-level Python library providing a clean, type-safe interface for Elasticsearch operations using Pydantic models for document schema definition.

## Key Features

- **Pydantic Integration** - Define document schema using Pydantic v2 models
- **Index Management** - Create, delete, and manage indices
- **Document Operations** - Insert, get, update, delete documents
- **Bulk Operations** - Efficient bulk insert/update
- **Type Safety** - Full type hints and Pydantic validation
- **Query Builder** - Safe query construction
- **Mapping Support** - Define custom mappings for indices
- **CLI Tool** - Command-line interface for common operations
- **Code Quality** - Pylint compatible, comprehensive type hints

## Technical Stack

- **Python**: 3.9+
- **Key Libraries**: elasticsearch>=8.0.0, pydantic>=2.0.0
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Code Quality**: black, mypy, ruff

## Installation & Setup

```bash
pip install wElasticsearch
```

Development installation:
```bash
pip install -e ".[dev]"
```

## Architecture & Workflow

```
wElasticsearch/
├── src/wElasticsearch/     # Main library package
│   ├── core/              # Core Elasticsearch operations
│   ├── builders/          # Query builder
│   ├── exceptions/       # Custom exceptions
│   ├── types/            # Type definitions
│   └── cli/              # CLI tool
├── examples/              # Usage examples (12+ folders)
├── test/                  # Test suite
│   ├── unit/            # Unit tests
│   └── integration/    # Integration tests
├── docs/                  # Sphinx documentation
├── stress_test/          # Performance testing
├── docker/               # Docker configurations
├── pyproject.toml        # Project config
└── README.md
```

**Workflow**: Define Pydantic model → Configure Elasticsearch connection → Initialize WElasticsearch → Create index → Perform document operations

## Configuration

**Environment Variables**:
- `ELASTICSEARCH_HOSTS` - Comma-separated list of hosts
- `ELASTICSEARCH_API_KEY` - API key for authentication

**Configuration Files**:
- `pyproject.toml` - Project metadata and dependencies
- `setup.py` - Package configuration

## Usage

```python
from pydantic import BaseModel
from wElasticsearch import WElasticsearch

ES_CONFIG = {
    "hosts": ["http://localhost:9200"],
}

class User(BaseModel):
    id: int
    name: str
    email: str

client = WElasticsearch(**ES_CONFIG)
client.insert("users", {"id": 1, "name": "John", "email": "john@example.com"}, id="1")
results = client.search("users", {"query": {"match_all": {}}})
print(results)
client.close()
```

## Author

- **William Rodríguez** - [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/wisrovi/)