#!usr/bin/env python3
import os
from pymongo import MongoClient

username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]


def connect():
    client = MongoClient('mongo:27017', username=username, password=password, authSource='admin')
    db = client.squawky
    return db


def write_dictionary_to_mongodb(dictionary):
    db = connect()
    old_dictionary = db.squawky.find_one({})
    if old_dictionary is not None:
        # TODO delete old dictionary
        pass
    db.squawky.insert_one(dictionary)


def get_dictionary_from_mongodb(author, server):
    db = connect()
    dictionary = db.squawky.find_one({})
    return dictionary

