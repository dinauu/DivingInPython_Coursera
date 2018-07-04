import functools
import json


def to_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result)

    return wrapper
