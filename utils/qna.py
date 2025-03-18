import utils.base as base
import utils.config as config
import utils.genai as genai
import datetime

def generate_chat_id(user_id):
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
                    사용자의 의도에 따라 여러 개의 주제가 있으면 주제별로 요약하되 
                    각 주제는 markdown 형식으로 제6단계의 header로 표시하시오.
                    이전 메시지에 Summary 정보가 있으면 이후 메시지와 주제 단위에서 통합하여 요약하시오.
                    최대한 폰트 크기를 작게 하시오.
                    500자 이내로 요약하시오.
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

def delete_history(user_id, chat_id):
    config.delete_chat_history(user_id, chat_id)
    return

def save_history(user_id, chat_id, chat_name, messages):
    conversation = {"chat_name": chat_name, "messages": messages}

    config.save_chat_history(user_id, chat_id, conversation)
    return chat_name

def get_chat_list(user_id):
    chat_list = config.get_chat_list(user_id)
    return chat_list

def get_chat_messages(user_id, chat_id):
    conversation = config.get_chat_content(user_id, chat_id)
    if conversation is None:
        return [], ""
    else:
        return conversation["messages"], conversation["chat_name"]
