import utils.base as base
import utils.config as config
import utils.chatgen as chatgen
import datetime

def generate_chat_id(user_id):
    time_string = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    rand_string = base.get_random_string(4)

    return "_".join([time_string, rand_string])

# Streamed response emulator
def generate_content(message, previous_messages=[]):
    response = chatgen.generate(message)
    return response

def summarize_title(messages):
    model = "gemini-flash"
    summary_prompt = """
                    메시지에 저장된 사용자의 첫 3개의 질문을 요약하여 5단어 이내로 제목을 작성하시오.
                    제목은 영어로 표시하고 특수문자는 포함하지 마시오.

                    """
    summary_target = ""
    for i, message in enumerate(messages):
        summary_target = f"message {i}. {message}\n"

    summary_title = chatgen.generate(summary_prompt + summary_target)
    return summary_title

def delete_history(user_id, chat_id, chat_group="CHAT"):
    config.delete_chat_history(f"{chat_group}_{user_id}", chat_id)
    return

def save_history(user_id, chat_id, chat_name, messages, chat_group="CHAT"):
    conversation = {"user_id": user_id, "chat_group":chat_group, "chat_name": chat_name, "messages": messages}

    config.save_chat_history(f"CHAT_{user_id}", chat_id, conversation)
    return chat_name

def get_chat_list(user_id, chat_group="CHAT00"):
    chat_list = config.get_chat_list(f"{chat_group}_{user_id}")
    return chat_list

def get_chat_messages(user_id, chat_id, chat_group="CHAT00"):
    conversation = config.get_chat_content(f"{chat_group}_{user_id}", chat_id)
    if conversation is None:
        return [], ""
    else:
        return conversation["messages"], conversation["chat_name"]
