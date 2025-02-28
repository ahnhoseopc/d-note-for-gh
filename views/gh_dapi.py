import utils.api as api

from pydantic import BaseModel
import asyncio

import streamlit as st

# Pydantic 모델
class GenerateRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-pro"

# Streamlit UI
def streamlit_ui():
    st.title("LLM API Service")
    
    # API 문서 링크
    st.markdown("""
    ## API Documentation
    - Generate Text: `POST /api/generate`
    - List Models: `GET /api/models`
    """)
    
    # API 테스트 인터페이스
    st.header("Test API")
    
    # 모델 선택
    models = asyncio.run(api.get_models()) 
    # loop = asyncio.get_event_loop()
    # models = loop.run_until_complete(api.get_models())
    
    model = st.selectbox("Select Model", models["models"])
    
    # 프롬프트 입력
    prompt = st.text_area("Enter prompt:")
    
    if st.button("Generate"):
        with st.spinner("Generating..."):
            try:
                # request = GenerateRequest(prompt=prompt, model_name=model)
                response = asyncio.run(api.generate(prompt, model))

                st.success("Generation successful!")
                st.text_area("Response:", value=response, height=200)
                # st.text_area("Response:", value=response["text"], height=200)
            except Exception as e:
                st.error(f"Error: in [streamlit_ui()] - {str(e)}")

    # API 사용 예시
    st.header("API Usage Examples")
    st.code("""
    # Python example using requests
    import requests

    response = requests.post(
        "http://localhost:8501/api/generate",
        json={
            "prompt": "Your prompt here",
            "model_name": "gemini-pro"
        }
    )
    """)


if __name__ == "__page__":
    streamlit_ui()
