#!/usr/bin/env python3
"""A function that changes all topics of a school document
based on the name """
import pymongo


def update_topics(mongo_collection, name, topics):
    """function that changes all topics of a school document based on the name
    mongo_collection will be the pymongo collection object
    name (string) will be the school name to update
    topics (list of strings) will be the list of
    topics approached in the school"""
    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
