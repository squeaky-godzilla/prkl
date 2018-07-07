from __future__ import print_function
import sys
import json
import re
from pymongo import MongoClient as mongo
from pymongo import TEXT
from bson.json_util import dumps
from flask import request, jsonify, Flask


be_hostname = "192.168.10.10"
be_port = 27017

app = Flask(__name__)


def connect_mongo(ip, port):
    client = mongo(ip, port)
    dbase = client.prkl
    return dbase


def format_output(output):
    result = {}
    try:
        for item in output:
            result[item["_id"]["$oid"]] = item
            result[item["_id"]["$oid"]].pop("_id")
    except:
        result = output
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
    collection.create_index([('artist', TEXT),('title', TEXT)])
    search_regex = re.compile(search_string, re.IGNORECASE)
    output = json.loads(dumps(collection.find({ "$or": [{ "title": search_regex },{ "artist": search_regex }]})))
    result = format_output(output)
    return result


def add_song_rating(id, rating, rating_collection):
    print("rating function call, parameters id:%s rating:%f" % (id,rating), file=sys.stdout)
    if 1 <= rating <= 5:
        print("adding rating to %s" % (id), file=sys.stdout)
        rating_collection.insert_one({"song_id": id, "song_rating": rating})
    else:
        print ("invalid rating", file=sys.stderr)

def get_song_rating(id, rating_collection):
    # print(dumps(rating_collection.find({})), file=sys.stdout)
    try:
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
    except:
        result = 'song_id=%s not found' % (id)
    return result


@app.route('/songs/', methods=['GET'])
def route_get_all():
    songs_db = connect_mongo(be_hostname, be_port)
    return jsonify(get_all(songs_db.songs))

@app.route('/songs/avg/difficulty/', methods=['GET'])
def route_get_diff_above():
    songs_db = connect_mongo(be_hostname, be_port)
    difficulty = request.args.get('diff',default = 0, type = int)
    return jsonify(get_diff_above(songs_db.songs, difficulty))

@app.route('/songs/search/', methods=['GET'])
def route_song_search():
    try:
        search = request.args.get('string', default = '')
    except:
        pass
    songs_db = connect_mongo(be_hostname, be_port)
    return jsonify(song_search(songs_db.songs, search))

@app.route('/songs/rating', methods = ['POST'])
def route_add_song_rating():
    songs_db = connect_mongo(be_hostname, be_port)
    song_id = request.form['song_id']
    rating = float(request.form['rating'])
    add_song_rating(song_id, rating, songs_db.ratings)
    return "rating=%s added to song_id=%s\n" % (rating, song_id)

@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
def route_get_song_rating(song_id):
    songs_db = connect_mongo(be_hostname, be_port)
    return jsonify(get_song_rating(song_id,songs_db.ratings))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
