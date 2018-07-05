import json
import sys
from pymongo import MongoClient as mongo
from bson.json_util import dumps


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


def get_diff_above(collection,diff_threshold):      #mongo query to dict should have a function!
    avg_difficulty_output = json.loads(dumps(collection.aggregate([{"$group": {"_id": "null","avg_difficulty": { "$avg": "$difficulty" }}}])))
    avg_difficulty = {}
    avg_difficulty['avg_difficulty'] = avg_difficulty_output[0]['avg_difficulty']
    output = json.loads(dumps(collection.find( { "difficulty":  {"$gt" : diff_threshold}  } )))
    result = {}
    for item in output:
        result[item["_id"]["$oid"]] = item
        result[item["_id"]["$oid"]].pop("_id")
    return result, avg_difficulty



songs_db = connect_mongo(be_hostname, be_port)

# print get_all(songs_db.songs)

print get_diff_above(songs_db.songs,10)
