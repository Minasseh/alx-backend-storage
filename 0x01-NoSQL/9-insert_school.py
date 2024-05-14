#!/usr/bin/env python3
"""A function that inserts a new document in a collection based on kwargs """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a collection based on kwargs and
    Returns the new _id """
    for key, value in kwargs.items():
        result = mongo_collection.insert_many([{key: "value"}])
    return result.inserted_ids
