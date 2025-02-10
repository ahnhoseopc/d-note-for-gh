from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import uvicorn

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
    uvicorn.run(app, host="0.0.0.0", port=8000)

# from threading import Thread
# # 메인 실행
# if __name__ == "__main__":
#     # FastAPI 서버를 별도 스레드로 실행
#     api_thread = Thread(target=api.run_fastapi, daemon=True)
#     api_thread.start()
    
#     # Streamlit UI 실행
#     # streamlit_ui()