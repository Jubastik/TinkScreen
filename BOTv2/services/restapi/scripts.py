async def get_headers(tg_id: int = None) -> dict:
    headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json", "access_token": "no"}
    return headers
