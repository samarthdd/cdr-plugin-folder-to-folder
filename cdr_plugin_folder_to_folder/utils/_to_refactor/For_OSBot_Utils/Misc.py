import re


def is_regex_full_match(pattern, target, flags=0):
    try:
        match = re.fullmatch(pattern, target, flags=flags)
        if match:
            return True
    except:
        pass
    return False

def is_regex_match(pattern, target, flags=0):
    try:
        match = re.match(pattern, target, flags=flags)
        if match:
            return True
    except:
        pass
    return False