from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import uvicorn

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

server = None
# FastAPI 서버 실행 함수
def run_fastapi():
    global server

    nest_asyncio.apply()

    server = uvicorn.Server(app, host="0.0.0.0", port=8000)
    server.start()
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    return server

# from threading import Thread
# # 메인 실행
# if __name__ == "__main__":
#     # FastAPI 서버를 별도 스레드로 실행
#     api_thread = Thread(target=api.run_fastapi, daemon=True)
#     api_thread.start()
    
#     # Streamlit UI 실행
#     # streamlit_ui()

import uvicorn
import asyncio

async def app(scope, receive, send):
    # your FastAPI app logic here
    pass

async def run_uvicorn(shutdown_event):
    server = uvicorn.Server(app=app, port=8000)
    await server.start()
    await shutdown_event.wait()
    await server.shutdown()

if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    asyncio.run(run_uvicorn(shutdown_event))
    # set the event to trigger shutdown
    shutdown_event.set()