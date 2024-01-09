from typing import Any, Optional


def success_response(message: str, data: Any = None) -> dict:
    return {
        "success": True,
        "message": message,
        "result": data,
    }


def failure_response(
    message: str, errors: Optional[dict[str, list[str]]] = None
) -> dict:
    return {
        "success": False,
        "message": message,
        "errors": errors,
    }
