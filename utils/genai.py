import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

model = None

def init_genai(project="dk-medical-solutions"):
    vertexai.init(project=project, location="us-central1")

init_genai()

def get_model_gemini_2_0_flash_exp(si):
    global model
    if model is None:
        model = GenerativeModel(
            "gemini-2.0-flash-exp",
            system_instruction=[si]
        )
    return model

def get_model_gemini_1_5_pro_002(si):
    global model
    if model is None:
        model = GenerativeModel(
            "gemini-1.5-pro-002",
            system_instruction=[si]
        )
    return model

def get_model_medlm_large(si):
    global model
    if model is None:
        model = GenerativeModel(
            "medlm-large-1.5@001",
            system_instruction=[si]
        )
    return model

SI = """답을 질문내용, 응답내용을 포함하는 json 포맷으로 해.답변시 정확한 진단은 의사에게 확인하라는 내용은 응답내용에서 제외하고 별도의 json 필드 "주의" 라는 필드에 표시하도록 해."""
MODEL="medlm"
def get_model(si=SI, model_name=MODEL):
    if model_name == "medlm":
        return get_model_medlm_large(si)
    elif model_name == "gemini-1.5-pro-002":
        return get_model_gemini_1_5_pro_002(si)
    else:
        return get_model_gemini_2_0_flash_exp(si)

def generate(prompts):
    model = get_model()
    responses = model.generate_content(
        prompts,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    return responses

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

if __name__ == "__main__":
    responses = generate(["""신장질병 종류가 얼마나 되는가."""])
    for response in responses:
        print(dir(response))
        print(response.text, end="\n\n")
