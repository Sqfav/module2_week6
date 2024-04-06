import asyncio
from functools import wraps


class Cache:
    def __init__(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(kwargs.items()))
            if key not in self.data:
                self.data[key] = func(*args, **kwargs)
            return self.data[key]
        return wrapper

    def invalidate(self, func):
        keys_to_delete = [key for key in self.data.keys() if key[0] == func.__name__]
        for key in keys_to_delete:
            del self.data[key]


cache = Cache()


@cache
def slow_function(arg):
    return arg


class MyClass:
    @cache
    def method(self, arg):
        return arg


@cache
async def async_func(arg):
    await asyncio.sleep(1)
    return arg
