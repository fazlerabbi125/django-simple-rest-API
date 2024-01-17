from enum import Enum
from typing import Any, Optional

def success_response(message: str, data: Any = None):
    return {
        "success": True,
        "message": message,
        "result": data,
    }


def failure_response(message: str, errors: Optional[dict[str, list[str]]] = None):
    return {
        "success": False,
        "message": message,
        "errors": errors,
    }


class USER_ROLES(Enum):
    ADMIN = "admin"
    MEMBER = "member"
