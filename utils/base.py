import random
import string
import logging
 
def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    #result_str = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*?") for i in range(length))
    return result_str

import json

def is_json_format(data):
    try:
        json.loads(data)
        return True
    except (ValueError, TypeError) as ex:
        logging.error("json error", ex)
        return False

import re

def is_rtf_format(data):
    """
    문자열이 RTF 형식인지 확인하는 함수.
    """
    # RTF는 항상 '{\rtf'로 시작
    return bool(re.match(r'^{\\rtf', data.strip()))

from urllib.parse import unquote

def decode_rtf(rtf_text):
    # Remove RTF formatting and extract relevant text
    rtf_cleaned = re.sub(r"{\\.*?}", "", rtf_text)  # Remove RTF metadata
    rtf_cleaned = re.sub(r"\\[a-z]+[0-9]* ?", "", rtf_cleaned)  # Remove RTF control words
    rtf_cleaned = rtf_cleaned.replace("\\'", "%")  # Replace RTF hex marker with URL encoding
    decoded_text = bytes(rtf_cleaned, "latin1").decode("cp949", errors="ignore")  # Decode with Korean charset
    decoded_text = unquote(decoded_text, encoding='euc-kr')
    return decoded_text

def ifnull(value1, value2):
    """
    Returns default_value if value is None, otherwise returns value.
    """
    try:
        return value2 if value1 is None else value1
    except Exception:
        return None
    
def make_short(sentense):
    return sentense[:16] + "..." if len(sentense) > 16 else sentense