from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from pydantic import BaseModel
import google.auth
import google.genai as ggenai
import nest_asyncio
import uvicorn
import os

import streamlit as st

FASTAPI_PORT = 8000

print(f"gh_dapi.__name__: {__name__}")

# FastAPI 앱 설정
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# FastAPI 서버 실행 함수
def run_fastapi():
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=FASTAPI_PORT)

# Pydantic 모델
class GenerateRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-pro"

if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = st.secrets.GCP_CREDENTIALS;

def get_genai_models():
    try:
        client = ggenai.Client(api_key="AIzaSyBTlisr9BRJO0pluf0W2qJkQ7ZGhfeowac")
        models = client.models.list()

        return [model.name for model in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

# FastAPI 라우트
@app.post("/api/generate")
async def generate_text(request: GenerateRequest):
    project = "dk-medical-solutions"
    try:
        models = get_genai_models()
        if request.model_name in models:
            # client = ggenai.Client(api_key="AIzaSyBTlisr9BRJO0pluf0W2qJkQ7ZGhfeowac")
            # response = client.models.generate_content(model=request.model_name, contents=request.prompt)

            # ggenai.configure(api_key="AIzaSyBTlisr9BRJO0pluf0W2qJkQ7ZGhfeowac")
            credentials,project = google.auth.default()
            ggenai.configure(credentials=credentials)
            client = ggenai.Client(vertexai=True, project=project, location="us-central1", credentials=credentials)
            response = client.models.generate_content(model=request.model_name, contents=request.prompt)

            # model = ggenai.GenerativeModel('gemini-pro')
            # response = model.generate_content(request.prompt)
            return {"text": response.text}
        return {"text": "Model not supported"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{request}: {project} | {str(e)}")

@app.get("/api/models")
async def list_models():
    return {"models": get_genai_models()}

@app.get("/health")
async def health_check():
    return {"status": "running"}
