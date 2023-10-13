import json
import re
from datetime import datetime

from core.entities import LogItemCreateDTO


def get_operation(service_name: str):
    if service_name == "create-service":
        return "create"
    elif service_name == "update-service":
        return "update"
    elif service_name == "delete-service":
        return "delete"
    elif service_name == "read-service":
        return "read"
    else:
        raise ValueError(f"Invalid service name: {service_name}")


def create_log_item(
    operation: str, doc_id: str | None = None, doc_type: str | None = None
) -> LogItemCreateDTO:
    log_item = LogItemCreateDTO(
        operation=operation,
        document_id=doc_id if doc_id is not None else "000",
        document_type=doc_type if doc_type is not None else "Cédula",
        created_at=datetime.now(),
    )

    return log_item


def get_doc_id_and_doc_type(raw_body: str | None) -> tuple[str | None, str | None]:
    if raw_body is None:
        return None, None

    try:
        body = json.loads(raw_body)
        doc_id = body.get("document_id", None)
        doc_type = body.get("document_type", None)
    except json.JSONDecodeError:
        doc_id = None
        doc_type = None

    return doc_id, doc_type


# valid detail uri: /:id
def get_detail_uri(uri: str):
    match = re.match(r"/(\w+)/?$", uri)

    if match:
        return match.group(1)

    return None
