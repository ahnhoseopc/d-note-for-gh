import json
import toml
from pathlib import Path

# -----------------------------------------------------------------------
# DB Query Collection
# -----------------------------------------------------------------------
QUERY_CONFIG_TOML = "dbquery.toml"

def save_query(query_name, query):
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        config_data["database"][query_name] = query

    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config_data, f)

def save_query_list(query_list): # NEW FUNCTION TO PERSIST THE QUERY LIST
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
    config_data["queries"] = query_list  #Store the list itself
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config_data, f)

def get_query(query_name):
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        return config_data["database"][query_name]

def get_query_list(): # MODIFY TO RETRIEVE THE LIST DIRECTLY
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        return list( config_data.get("database").keys() )  # Return empty list if not found

# -----------------------------------------------------------------------
# Chat History Json
# -----------------------------------------------------------------------
def get_chat_filename(user_id, chat_id):
    return ".".join([user_id + "_" + chat_id, "json"])

def save_chat_history(user_id, chat_id, messages):
    Path(".history").mkdir(parents=True, exist_ok=True)
    chat_file = Path(".history", get_chat_filename(user_id, chat_id))
    with open(chat_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(messages))

def delete_chat_history(user_id, chat_id):
    chat_file = Path(".history", get_chat_filename(user_id, chat_id))
    chat_file.unlink(missing_ok=False)

MAX_CHAT_FILES = 10

def get_chat_list(user_id):
    chat_path = Path(".history")
    chat_files = list(chat_path.glob(f"{user_id}_*.json"))
    chat_files_sorted = sorted(chat_files, key=lambda f: f.stat().st_mtime, reverse=True)

    chat_list = []
    for file in chat_files[:MAX_CHAT_FILES]:
        with open(file, "r", encoding="utf-8") as f:
            chat_string = f.read()
        chat = json.loads(chat_string)
        
        chat_list.append({"chat_name":chat["chat_name"], "chat_id":file.stem.removeprefix(user_id+ "_"), "user_id":user_id})
    return chat_list

def get_chat_content(user_id, chat_name):
    chat_path = Path(".history", get_chat_filename(user_id, chat_name))
    if chat_path.exists():
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_string = f.read()
        chat = json.loads(chat_string)
        return chat
    else:
        return None
