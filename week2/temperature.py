def is_vormir_safe(threshold, a, b, c):
    if threshold < a and threshold < b:
        return True
    if threshold < a and threshold < c:
        return True
    if threshold < b and threshold < c:
        return True
    else:
        return False
