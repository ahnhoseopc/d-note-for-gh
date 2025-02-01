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
def get_chat_filename(user_id, chat_name):
    return ".".join([user_id + "_" + chat_name, "json"])

def save_chat_history(user_id, chat_name, messages):
    Path(".history").mkdir(parents=True, exist_ok=True)
    config_path = Path(".history", get_chat_filename(user_id, chat_name))
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(messages))

def get_chat_history(user_id, chat_name):
    config_path = Path(".history", get_chat_filename(user_id, chat_name))
    with open(config_path, "r", encoding="utf-8") as f:
        messages_string = f.read()
    messages = json.loads(messages_string)
    return messages
