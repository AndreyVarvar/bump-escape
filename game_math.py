import settings as stt


def clamp(n, min_n, max_n):
    if n < min_n:
        return min_n

    if n > max_n:
        return max_n

    return n
