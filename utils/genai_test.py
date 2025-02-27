import logging
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import os

if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ".streamlit/gcp_credentials_dk_dnote_ghmh.json";

def generate():
    vertexai.init(
        project="dkportal",
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com"
    )
    model = GenerativeModel(
        "medlm-large-1.5@001",
    )
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        logging.info(response.text, end="")

text1 = """local에서 산전 진찰 받으시던분으로 오늘 아침 설사 있어 진료 받던중 질 출혈 있어 타병원 방문하여 자궁 문이 다 열렸다고 하여 태아 치료 위해 전원 되어 옴 5:00pm 경 bethamethasone은 맞고 옴, 분만실 도착시 산모 맥박 120회 정도 됨
이런 환자에게 어떤 진료를 제공하여야 하는가"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

generate()