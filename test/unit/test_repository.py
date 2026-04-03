import pytest
from pydantic import BaseModel


class TestRepository:
    def test_import(self):
        from wElasticsearch.core.repository import Repository

        assert Repository is not None

    def test_model_validation(self):
        from wElasticsearch.core.repository import Repository

        class User(BaseModel):
            id: int
            name: str

        repo = Repository(User)
        assert repo.model == User
