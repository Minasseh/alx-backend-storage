#!/usr/bin/env python3
"""  Writing strings to Redis """
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ Store the history of inputs and outputs for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapper function """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper

def count_calls(method: Callable) -> Callable:

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper

class Cache:
    def __init__(self):
        """  An instance of the Redis client as a private variable
        named _redis (using redis.Redis()) and flush the
        instance using flushdb """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
