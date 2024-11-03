from pymongo import MongoClient

import logging

# Set pymongo logger to WARNING level to suppress DEBUG and INFO logs
logging.getLogger("pymongo").setLevel(logging.WARNING)


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://nhan:852124@cluster0.qmwjy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["rpgs"]


def add_character(character_dict):
    db["character"].insert_one(character_dict)


def get_character_by_id(cid):
    return db["character"].find({"id": cid})


def insert_or_update_character_by_id(cid, new_char_dict):
    new_values = {"$set": new_char_dict}
    return db["character"].update_one({"id": cid}, new_values, upsert=True)


db = get_database()
