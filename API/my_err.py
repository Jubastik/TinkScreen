"""
Коды ошибок
Первые 2 цифры - место ошибки
Вторые 2 цифры - номер ошибки

Описание первых 2 цифр:
3х значные - HTTP код ошибки
10: Ошибка валидации
11: Ошибки пользователя
"""


class APIError(Exception):
    def __init__(self, status_code: int, err_id: int, msg: str = None):
        self.msg = msg
        if msg is None:
            self.msg = readable_code[status_code]
        self.status_code = status_code
        self.err_id = err_id


readable_code = {
    1101: "Пользователь с данным tg_id уже существует",
    1102: "Пользователь не найден",
}

INTERNAL_SERVER_ERROR = 500

VALIDATION_ERROR = 1000
INVALID_ROOT_TOKEN = 1001
IN_DEVELOPMENT = 1002

TG_ID_OCCUPIED = 1101
USER_NOT_FOUND = 1102
