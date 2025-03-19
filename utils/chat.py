import logging
import utils.base as base
import utils.config as config
import utils.chatgen as chatgen
import utils.qna as qna
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
    logging.debug("entered")
    summary_title = qna.generate(messages)
    return summary_title

def delete_history(user_id, chat_group, chat_id):
    config.delete_chat_history(f"{chat_group}_{user_id}", chat_id)
    return

def save_history(user_id, chat_group, chat_id, chat_name, messages):
    conversation = {"user_id": user_id, "chat_group":chat_group, "chat_name": chat_name, "messages": messages}

    config.save_chat_history(f"CHAT_{user_id}", chat_id, conversation)
    return chat_name

def get_chat_list(user_id, chat_group):
    chat_list = config.get_chat_list(f"{chat_group}_{user_id}")
    return chat_list

def get_chat_messages(user_id, chat_group, chat_id):
    conversation = config.get_chat_content(f"{chat_group}_{user_id}", chat_id)
    if conversation is None:
        return [], ""
    else:
        return conversation["messages"], conversation["chat_name"]
