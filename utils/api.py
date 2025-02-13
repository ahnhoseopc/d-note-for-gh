import requests

FASTAPI_HOST = "localhost"
FASTAPI_PORT = 8000

def is_fastapi_running():
    """FastAPI 서버 실행 여부를 API를 통해 확인"""
    try:
        response = requests.get(f"http://{FASTAPI_HOST}:{FASTAPI_PORT}/health")
        return response.status_code == 200
    except requests.ConnectionError:
        return False
