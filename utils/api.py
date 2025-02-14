import requests
import httpx

FASTAPI_HOST = "localhost"
FASTAPI_PORT = 8000
API_BASEURL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}"

def is_fastapi_running():
    """FastAPI 서버 실행 여부를 API를 통해 확인"""
    url = f"{API_BASEURL}/health"
    headers = {"Content-Type": "application/json"}
    try:
        with httpx.AsyncClient() as client:
            response = client.get(url, headers=headers)
        # response = requests.get(f"{API_BASEURL}/health")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# async def generate(request):
#     return generate(request.prompt, request.model)

async def generate(prompt, model):
    url = f"{API_BASEURL}/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "model_name": model
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        #response.json
    # response = requests.post(url, json=data, headers=headers)
    return response.json()

async def get_models():
    url = f"{API_BASEURL}/api/models"
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    #response = requests.get(url, headers=headers)
    return response.json()

# 응답 출력
# print("Status Code:", response.status_code)
# print("Response JSON:", response.json())
