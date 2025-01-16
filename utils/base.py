import random
import string

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    #result_str = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*?") for i in range(length))
    return result_str
