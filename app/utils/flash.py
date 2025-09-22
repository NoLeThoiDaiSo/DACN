from starlette.requests import Request

FLASH_KEY = "_flash"

def set_flash(request: Request, message: str, category: str = "info") -> None:
    request.session[FLASH_KEY] = {"message": message, "category": category}

def pop_flash(request: Request):
    return request.session.pop(FLASH_KEY, None)
