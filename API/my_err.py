"""
Коды ошибок
Первые 2 цифры - место ошибки
Вторые 2 цифры - номер ошибки

Описание первых 2 цифр:
3х значные - HTTP код ошибки
10: Ошибка валидации
"""


class APIError(Exception):
    def __init__(self, status_code: int, err_id: int, msg: str):
        self.msg = msg
        self.status_code = status_code
        self.err_id = err_id


INTERNAL_SERVER_ERROR = 500

VALIDATION_ERROR = 1000
INVALID_ROOT_TOKEN = 1001
IN_DEVELOPMENT = 1002

