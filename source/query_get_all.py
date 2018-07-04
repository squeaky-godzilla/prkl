import json
import sys
from pymongo import MongoClient as mongo

be_hostname = "100.0.10.10"
be_port = 27017


def connect_mongo(ip, port):
    client = mongo(ip, port)
    dbase = client.prkl
    return dbase


def get_all(collection):
    cursor = collection.find({})
    result = {}
    for document in cursor:
        result[document.get('_id')] = document
    return result


def get_diff_above(collection,diff_threshold):
    cursor = collection.find( { "difficulty": "{ $gt: diff_threshold }" } )
    result = {}
    for document in cursor:
        result[document.get('_id')] = document
    return result



songs_db = connect_mongo(be_hostname, be_port)

# print get_all(songs_db.songs)

print get_diff_above(songs_db.songs,10)
