import utils.api as api

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import uvicorn
import streamlit as st

FASTAPI_PORT = 8000

print(f"gh_dapi.__name__: {__name__}")

# FastAPI 앱 설정
if "app" not in st.session_state:
    st.session_state["app"] = None

app = FastAPI()

# FastAPI 서버 실행 함수
def run_fastapi():
    if st.session_state.app is None:
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        )

        st.session_state.app = app

    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=FASTAPI_PORT)

from fastapi import HTTPException
from pydantic import BaseModel
import asyncio
import google.genai as ggenai
import google.auth

import streamlit as st
import os
if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = st.secrets.GCP_CREDENTIALS;

# Pydantic 모델
class GenerateRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-pro"

def get_genai_models():
    try:
        client = ggenai.Client(api_key="AIzaSyBTlisr9BRJO0pluf0W2qJkQ7ZGhfeowac")
        models = client.models.list()

        return [model.name for model in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

# FastAPI 라우트
@api.app.post("/api/generate")
async def generate_text(request: GenerateRequest):
    project = "dk-medical-solutions"
    try:
        models = get_genai_models()
        if request.model_name in models:
            # credentials,project = google.auth.default()
            # client = ggenai.Client(vertexai=True, project=project, location="us-central1", credentials=credentials)
            client = ggenai.Client(api_key="AIzaSyBTlisr9BRJO0pluf0W2qJkQ7ZGhfeowac")
            response = client.models.generate_content(model=request.model_name, contents=request.prompt)
            # ggenai.configure(api_key="AIzaSyBTlisr9BRJO0pluf0W2qJkQ7ZGhfeowac")
            # ggenai.configure(credentials=credentials)
            # model = ggenai.GenerativeModel('gemini-pro')
            # response = model.generate_content(request.prompt)
            return {"text": response.text}
        return {"text": "Model not supported"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{request}: {project} | {str(e)}")

@api.app.get("/api/models")
async def list_models():
    return {"models": get_genai_models()}

@api.app.get("/health")
async def health_check():
    return {"status": "running"}