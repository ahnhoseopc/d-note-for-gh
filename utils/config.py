import json
import toml
from pathlib import Path

# -----------------------------------------------------------------------
# DB Query Collection
# -----------------------------------------------------------------------
QUERY_CONFIG_TOML = "dma_query.toml"

def save_query(query_name, query):
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        config_data["database"][query_name] = query

    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config_data, f)

def delete_query(query_name):
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        if query_name in config_data["database"]:
            del config_data["database"][query_name]

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
        if query_name not in config_data["database"]:
            return None
        return config_data["database"][query_name]

def get_query_list(): # MODIFY TO RETRIEVE THE LIST DIRECTLY
    config_path = Path(".streamlit", QUERY_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        return list( config_data.get("database").keys() )  # Return empty list if not found

# -----------------------------------------------------------------------
# Chat History Json
# -----------------------------------------------------------------------
def get_chat_filename(prefix, chat_id):
    return ".".join([prefix + "_" + chat_id, "json"])

def save_chat_history(prefix, chat_id, messages):
    Path(".history").mkdir(parents=True, exist_ok=True)
    chat_file = Path(".history", get_chat_filename(prefix, chat_id))
    with open(chat_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(messages))

def delete_chat_history(prefix, chat_id):
    chat_file = Path(".history", get_chat_filename(prefix, chat_id))
    chat_file.unlink(missing_ok=True)

MAX_CHAT_FILES = 10

def get_chat_list(prefix):
    chat_path = Path(".history")
    chat_files = list(chat_path.glob(f"{prefix}_*.json"))
    chat_files_sorted = sorted(chat_files, key=lambda f: f.stat().st_mtime, reverse=True)

    chat_list = []
    for file in chat_files_sorted[:MAX_CHAT_FILES]:
        with open(file, "r", encoding="utf-8") as f:
            chat_string = f.read()
        chat = json.loads(chat_string)
        
        chat_list.append({"chat_name":chat["chat_name"], "chat_id":file.stem.removeprefix(prefix+ "_"), "prefix":prefix})
    return chat_list

def get_chat_content(prefix, chat_name):
    chat_path = Path(".history", get_chat_filename(prefix, chat_name))
    if chat_path.exists():
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_string = f.read()
        chat = json.loads(chat_string)
        return chat
    else:
        return None

DMA_CONFIG_TOML = "dma.toml"
def get_option(key):
    config_path = Path(".streamlit", DMA_CONFIG_TOML)
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)

        keys = key.split(".")
        if keys[0] in config_data and keys[1] in config_data[keys[0]]:
            option_value = config_data[keys[0]][keys[1]]
            return option_value

    return None
