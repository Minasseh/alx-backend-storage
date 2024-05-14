#!/usr/bin/env python3
""" Python function that lists all documents in a collection """
import pymongo


def list_all(mongo_collection):
    """ Lists all documents in a collection
    Return an empty list if no document in the collection """

    if mongo_collection.count_documents({}) == 0:
        return []
    return list(mongo_collection.find())
