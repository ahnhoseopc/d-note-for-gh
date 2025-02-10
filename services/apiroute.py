import utils.api as api

from fastapi import HTTPException
from pydantic import BaseModel
import google.generativeai as ggenai
import google.auth

# Pydantic 모델
class GenerateRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-pro"

# FastAPI 라우트
@api.app.post("/api/generate")
async def generate_text(request: GenerateRequest):
    try:
        if request.model_name == "gemini-pro":
            # ggenai.configure(api_key="your_api_key")
            credentials, = google.auth.default()
            ggenai.configure(credentials=credentials)
            model = ggenai.GenerativeModel('gemini-pro')
            response = model.generate_content(request.prompt)
            return {"text": response.text}
        return {"text": "Model not supported"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.app.get("/api/models")
async def list_models():
    return {"models": ["gemini-pro", "flash", "medllm"]}
