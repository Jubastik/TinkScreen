from settings import settings as s

BASE_URL = f"{s().API_HOST}:{s().API_PORT}/api"
URL_USER = f"{BASE_URL}/user"
CHECK_URL = f"{BASE_URL}/check/"
GET_CHECKS_URL = f"{BASE_URL}/check/my"