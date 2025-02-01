import utils.base as base
import utils.config as config
import utils.genai as genai
import datetime

def generate_conversation_id(user_id):
    time_string = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    rand_string = base.get_random_string(4)

    return "_".join([time_string, rand_string])

# Streamed response emulator
def generate_content(message, previous_messages=[]):
    model = "medlm"
    responses = genai.generate( previous_messages + [message] , model)

    for response in responses:
        yield response.text

def summarize_content(messages):
    model = "medlm"
    summary_prompt = """
                    이전 메시지를 사용자의 질문과 응답내용을 요약하시오.
                    사용자의 의도에 따라 여러 개의 주제가 있으면 주제별로 요약하시오. 
                    이전 메시지에 Summary 정보가 있으면 이후 메시지와 주제 단위에서 통합하여 요약하시오.
                    """
    summarize_message = {"role": "user", "parts": [{"text": summary_prompt}]}
    responses = genai.generate( messages + [summarize_message] , model)

    summary_text = ""
    for response in responses:
        summary_text += response.text

    return summary_text

def summarize_title(messages):
    model = "medlm"
    summary_prompt = """
                    메시지에 저장된 사용자의 첫 3개의 질문을 요약하여 5단어 이내로 제목을 작성하시오.
                    제목은 영어로 표시하고 특수문자는 포함하지 마시오.
                    """
    summarize_message = {"role": "user", "parts": [{"text": summary_prompt}]}
    responses = genai.generate( messages + [summarize_message] , model)

    summary_title = ""
    for response in responses:
        summary_title += response.text

    return summary_title

def save_history(user_id, conversation_id, messages):
    conversation_name = summarize_title(messages)
    conversation = {"conversation_name": conversation_name, "messages": messages}

    config.save_chat_history(user_id, conversation_id, conversation)
    return conversation_name

def get_history(user_id, conversation_id):
    conversation = config.get_chat_history(user_id, conversation_id)
    return conversation.messages, conversation.conversation_name
