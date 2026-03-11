import string

# 0-9, a-z, A-Z (62 total characters)
CHARSET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(id_num):
    """
    Converts a base10 integer (Database ID) into a base62 string.
    """
    if id_num == 0:
        return CHARSET[0]
    
    arr = []
    base = len(CHARSET)
    while id_num:
        id_num, rem = divmod(id_num, base)
        arr.append(CHARSET[rem])
    
    arr.reverse()
    return ''.join(arr)