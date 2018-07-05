import json
import sys
from pymongo import MongoClient as mongo
from pymongo import TEXT
from bson.json_util import dumps


be_hostname = "192.168.10.10"
be_port = 27017


def connect_mongo(ip, port):
    client = mongo(ip, port)
    dbase = client.prkl
    return dbase

def format_output(output):
    result = {}
    for item in output:
        result[item["_id"]["$oid"]] = item
        result[item["_id"]["$oid"]].pop("_id")
    return result

def get_all(collection):
    output = json.loads(dumps(collection.find({})))
    result = format_output(output)
    return result


def get_diff_above(collection, diff_threshold):
    avg_difficulty_output = json.loads(dumps(collection.aggregate([
                    {"$group": {"_id": "null","avg_difficulty": { "$avg": "$difficulty" }}}])))
    avg_difficulty = {}
    avg_difficulty['avg_difficulty'] = avg_difficulty_output[0]['avg_difficulty']
    output = json.loads(dumps(collection.find( { "difficulty":  {"$gt" : diff_threshold}  } )))
    result = format_output(output)
    return [result, avg_difficulty]


def song_search(collection, search_string):
    collection.create_index([('artist', TEXT),('title', TEXT)], default_language='english')
    output = json.loads(dumps(collection.find( { "$text": { "$search": search_string } } )))
    result = format_output(output)
    return result


def add_song_rating(id, rating, rating_collection):
    if 1 <= rating <= 5:
        rating_collection.insert_one({"song_id": id, "song_rating": rating})
    else:
        pass

def get_song_rating(id, rating_collection):
    avg_rating_output = json.loads(dumps(rating_collection.aggregate([
                    { "$match": {"song_id": id}},
                    {"$group": {"_id": "null","avg_rating": { "$avg": "$song_rating" }}}
                    ])))[0]["avg_rating"]
    max_rating_output = json.loads(dumps(rating_collection.aggregate([
                    { "$match": {"song_id": id}},
                    {"$group": {"_id": "null","max_rating": { "$max": "$song_rating" }}}
                    ])))[0]["max_rating"]
    min_rating_output = json.loads(dumps(rating_collection.aggregate([
                    { "$match": {"song_id": id}},
                    {"$group": {"_id": "null","min_rating": { "$min": "$song_rating" }}}
                    ])))[0]["min_rating"]
    result = {id: {"avg":avg_rating_output,"max":max_rating_output,"min":min_rating_output}}
    return result


songs_db = connect_mongo(be_hostname, be_port)

print get_all(songs_db.songs)

print 100*"="

print get_diff_above(songs_db.songs,10)

print 100*"="

print song_search(songs_db.songs,"Bouzoukia")

print 100*"="

for i in range(4):
    add_song_rating("5b3d5c279dc6d67f73633f4e",i+1,songs_db.ratings)

print get_song_rating("5b3d5c279dc6d67f73633f4e", songs_db.ratings)
