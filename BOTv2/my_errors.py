class ApiError(Exception):
    def __init__(self, error_code: int):
        self.error_code = error_code


TOKEN_ERROR = 100  # Error while getting a token from the API
USER_ERROR = 101  # Error while getting a user from the API
USER_EXISTS = 102  # User already exists in the API