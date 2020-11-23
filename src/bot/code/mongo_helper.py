#!usr/bin/env python3
import os
from pymongo import MongoClient

username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]


def connect():
    client = MongoClient('mongo:27017', username=username, password=password, authSource='admin')
    db = client.squawky
    return db