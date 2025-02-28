import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

import streamlit as st

import os
if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = st.secrets.GCP_CREDENTIALS;

import google.auth
def get_access_token():
    """
    Retrieves an access token using Google default credentials.

    Returns:
        str: The access token.
    """
    credentials, project = google.auth.default()
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token

def init_genai(project="dk-medical-solutions"):
    vertexai.init(project=project, location="us-central1")

init_genai()

SI = """답변시 정확한 진단은 의사에게 확인하라는 내용은 제외하고 표시해줘.""" 
# """답을 질문내용, 응답내용을 포함하는 json 포맷으로 해.답변시 정확한 진단은 의사에게 확인하라는 내용은 응답내용에서 제외하고 별도의 json 필드 "주의" 라는 필드에 표시하도록 해."""
MODEL={
    "gemini-flash":"gemini-2.0-flash-exp",
    "gemini-pro":"gemini-1.5-pro-002", 
    "medlm":"medlm-large-1.5@001"
    }

model = {"gemini-flash":None, "gemini-pro":None, "medlm":None}

def get_model(model_name, si=SI):
    global model
    if model_name not in model.keys():
        model_name = list(model.keys())[0]

    if model[model_name] is None:
        model[model_name] = GenerativeModel( MODEL[model_name], system_instruction=[si] )

    return model[model_name]

def generate(prompts, model_name):
    model = get_model(model_name=model_name)
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
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
]

if __name__ == "__main__":
    prompt = """
    입력된 데이터의 "present illness" 와 "plan"을 확인하여 "operation name"을 추정하라.
    추정된 "operation name"을 참조하여 "protocols of doctor"의 "code" 또는 "code name"과 대응하는 것을 찾아서 해당하는 "protocol"을 찾아라.
    응답으로 "present illness" 와 "plan", "operation name"과 "code", "code name", "protocol"을 제시하라.
    """

    data = """{
        "patient": {
            "patient id": "1135806 ",
            "date of admission": "20250123",
            "sex": "M",
            "age": "64"
        },
        "clinical staff": {
            "department": "NS",
            "doctor in charge": "002702",
            "physician assistant": null,
            "nurse": null,
            "anesthesiologist": null,
            "method of anesthesia": null
        },
        "subjective": {
            "chief complaints": "LBP with rt. buttock/thigh/leg pain",
            "pain": "1$6^0$^0$^0^1^",
            "onset": "for 4-5 months",
            "present illness": "\uc77c\uc0c1\uc0dd\ud65c \ubd88\uac00\ub2a5\ud560 \uc815\ub3c4\ub85c LBP with rt. buttock/thigh/leg pain \uc2ec\ud558\uc5ec \uc218\uc220\uc704\ud574 \uc785\uc6d0\ud568",
            "obsteric gpal": null,
            "menstrual history": null,
            "past medical history": "^0",
            "admission-operation history": null,
            "social history": null,
            "family history": "1$0$^"
        },
        "objective": {
            "review of systems": null,
            "other review of systems": null
        },
        "assessment": {
            "impression": "1. \uc2e0\uacbd\ubfcc\ub9ac\ubcd1\uc99d\uc744 \ub3d9\ubc18\ud55c \uc694\ucd94 \ubc0f \uae30\ud0c0 \ucd94\uac04\ud310\uc7a5\uc560<G55.1*>",
            "diagnosis": [
                null
            ]
        },
        "plan": {
            "operation name": null,
            "plan": "L4-5, rt, discectomy",
            "discharge plan": null,
            "educational plan": "\uc9c8\ud658\uc0c1\ud0dc, \uce58\ub8cc\uacc4\ud68d, \uce58\ub8cc\uc5d0 \ub530\ub978 \uc608\uc0c1\ud6a8\uacfc \ubc0f \uc704\ud5d8\uc5d0 \ub300\ud574 \uad50\uc721\ud568."
        },
        "report date": "20250123",
        "report time": "11:41:49",
        "protocols of doctor": [
            {
                "code": "A01                 ",
                "code_name": "Lumbar",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position\r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. Small laminotomy with discectomy ( L )\r\n5. Decompressive laminotomy ( L )\r\n(Unilateral laminotomy for bilateral decompression)\r\n5. Decompressive foraminotomy ( L )\r\n1) adhesion, severe\r\n2) inflammation, severe\r\n6. Bleeding control, irrigation\r\n7. Hemovac 100cc\r\n8. Suture\r\n}\r\n"
            },
            {
                "code": "A02                 ",
                "code_name": "PLIF",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position\r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. L PLIF \r\n1) Lt. laminotomy for bilateral decompression \r\n: adhesion & inflmmmation, severe\r\n2) facetectomy/ discectomy\r\n3) Cage interbody insertion \r\n: transversely lying \r\n: autologous bone + allograft + DBM\r\n6. Percutaneous screw fixation (6.5mm X 45mm)\r\n7. Bleeding control, irrigation\r\n8. Hemovac 100cc\r\n9. Suture\r\n}\r\n"
            },
            {
                "code": "A11                 ",
                "code_name": "Cervical",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position with slightly flexed neck\r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. Small laminotomy\r\n5. Discectomy ( C )\r\n1) ruptured disc (+)\r\n2) adhesion, severe\r\n5. Decompressive foraminotomy ( C )\r\n5. Decompressive laminotomy ( C )\r\n(unilateral laminotomy with bilateral decompression)\r\n5. Decompressive hemilaminectomy with contralateal sublaminoplasty \r\nwith total flacectomy ( C )\r\n1) adhesion, severe\r\n2) inflammation, severe\r\n6. Bleeding control, irrigation\r\n7. Hemovac 100cc\r\n8. Suture\r\n}\r\n"
            },
            {
                "code": "A21                 ",
                "code_name": "Thoracic",
                "protocol": "}\r\n1. General anesthesia\r\n2. Prone position \r\n3. Clean drapping with fluid collecting bag\r\n4. Small skin incision\r\n5. Decompressive laminotomy\r\n5. Removal of OLF ( T ) through translaminar approach\r\n1) adhesion, severe\r\n2) inflammation, severe\r\n6. Bleeding control, irrigation\r\n7. Hemovac 100cc\r\n8. Suture\r\n}\r\n"
            },
            {
                "code": "A31                 ",
                "code_name": "VP",
                "protocol": "}\r\n1. Prone position\r\n2. Local anesthesia\r\n3. Clean drapping\r\n4. Small skin incision\r\n5. L2 VP\r\n6. Suture\r\n}\r\n"
            },
            {
                "code": "A32                 ",
                "code_name": "Irrigation",
                "protocol": "}\r\n1. Prone position\r\n2. Local anesthesia\r\n3. Clean drapping\r\n4. I & D\r\n5. Hemovac 100cc\r\n6. Suture\r\n}\r\n"
            },
            {
                "code": "A41                 ",
                "code_name": "NAVI",
                "protocol": "}\r\n1. Prone position\r\n2. Local anesthesia\r\n3. Catheter insertion into epidural space though trans-sacral hiatus (with NAVI)\r\n4. Position of catheter checked with C-ram radiography and dye\r\n5. Epidural neuroplasty was performed under the C-arm\r\n6. Several drugs apply\r\n7. Suture and dressing\r\n}\r\n"
            }
        ]
    }
    """

    responses = generate([prompt, data])
    for response in responses:
        print(dir(response)) # candidates, from_dict, to_dict, prompt_feedback, usage_metadata, text
        print(response.text, end="\t\t")
