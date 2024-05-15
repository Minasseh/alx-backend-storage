#!/usr/bin/env python3
"""  Writing strings to Redis """
import redis
import uuid
from typing import Union, Callable
from functools import wraps


@staticmethod
def count_calls(method: Callable) -> Callable:

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self.calls_counter[key] = self.calls_counter.get(key, 0) + 1

        return method(self, *args, **kwargs)

    return wrapper

class Cache:
    def __init__(self):
        """  An instance of the Redis client as a private variable
        named _redis (using redis.Redis()) and flush the
        instance using flushdb """
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.calls_counter = {}

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """  A store method that takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid), store the
        input data in Redis using the random key and return the key. """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str, fn: Callable = None) -> Union[str, int, bytes, None]:
        """ A method that take a key string argument and an optional
        Callable argument named fn. This callable will be used to convert
        the data back to the desired format. """
        data = self._redis.get(key)

        if data is None:
            return None
        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """ Get data from Redis and convert to str """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """ Get data from Redis and convert to int """
        return self.get(key, int)
