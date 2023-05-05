async def get_headers() -> dict:
    headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json", "access_token": "no"}
    return headers


async def get_params() -> dict:
    params = {"id_type": "student_tg"}
    return params
