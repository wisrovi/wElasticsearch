from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from datetime import datetime


PYDANTIC_TO_ES = {
    str: "text",
    int: "long",
    float: "double",
    bool: "boolean",
    datetime: "date",
    "datetime": "date",
}


def model_to_mapping(
    model: Type[BaseModel], index_name: Optional[str] = None
) -> dict[str, Any]:
    properties = {}
    for field_name, field_info in model.model_fields.items():
        field_type = field_info.annotation
        es_type = "object"
        if field_type in PYDANTIC_TO_ES:
            es_type = PYDANTIC_TO_ES[field_type]
        elif hasattr(field_type, "__origin__"):
            if field_type.__origin__ is list:
                if hasattr(field_type, "__args__") and field_type.__args__:
                    inner_type = field_type.__args__[0]
                    if inner_type in PYDANTIC_TO_ES:
                        es_type = PYDANTIC_TO_ES[inner_type]
                    else:
                        es_type = "nested"
                else:
                    es_type = "text"
            elif field_type.__origin__ is dict:
                es_type = "object"
        elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
            es_type = "nested"

        field_config: dict[str, Any] = {"type": es_type}
        if field_info.default is not None and field_info.default != Field:
            if hasattr(field_info.default, "description"):
                field_config["doc_values"] = True
        if field_info.description:
            field_config["fields"] = {"keyword": {"type": "keyword"}}
        if field_info.json_schema_extra and "index" in field_info.json_schema_extra:
            if not field_info.json_schema_extra["index"]:
                field_config["index"] = False

        properties[field_name] = field_config

    mapping = {"properties": properties}
    if index_name:
        mapping["index"] = index_name
    return mapping


def get_model_id(document: BaseModel, id_field: str = "id") -> Optional[str]:
    if hasattr(document, id_field):
        return str(getattr(document, id_field))
    return None


def document_to_dict(document: BaseModel, id_field: str = "id") -> dict[str, Any]:
    doc_dict = document.model_dump()
    if id_field in doc_dict:
        doc_id = doc_dict.pop(id_field)
        return {"_id": doc_id, "_source": doc_dict}
    return {"_source": doc_dict}
