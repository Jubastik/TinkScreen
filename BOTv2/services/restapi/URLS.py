from settings import settings as s

BASE_URL = f"{s().API_HOST}:{s().API_PORT}/api"
URL_USER = f"{BASE_URL}/user"