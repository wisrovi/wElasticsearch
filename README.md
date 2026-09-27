<p align="center">
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

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

---

## 👤 Autor & Afiliación Oficial

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Cargo:** Principal AI Engineer & Applied AI Solutions Architect | Scientific Researcher
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com)
* 🌐 **Portal Oficial:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)


