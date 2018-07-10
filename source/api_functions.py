from __future__ import print_function
import os
import sys
import json
import re
from pymongo import MongoClient as mongo
from pymongo import TEXT
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, jsonify, Flask, redirect, url_for, abort
from werkzeug import secure_filename



try:
    be_hostname = sys.argv[1]
except:
    be_hostname = "192.168.10.100"
be_port = 27017


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

def insert_song(json,dbase):
    songs = dbase.songs
    song_id = songs.insert_one(json)

def import_data(json_file, dbase):
    json_obj = open(json_file,"r")
    print ("[PRKL import] loading file %s" % (str(json_file)))
    for line in json_obj:
        insert_song(json.loads(line), dbase)
    return ("[PRKL import] collection now has total %i records\n" % (dbase.songs.count()))


def get_all(collection):
    output = json.loads(dumps(collection.find({})))
    result = format_output(output)
    return result


def get_level_above(collection, level):
    avg_difficulty_output = json.loads(dumps(collection.aggregate([
                    {"$group": {"_id": "null","avg_difficulty": { "$avg": "$difficulty" }}}])))
    avg_difficulty = {}
    avg_difficulty['avg_difficulty'] = avg_difficulty_output[0]['avg_difficulty']
    output = json.loads(dumps(collection.find( { "level":  {"$gt" : level}  } )))
    result = format_output(output)
    return [result, avg_difficulty]


def song_search(collection, search_string):
    collection.create_index([('artist', TEXT),('title', TEXT)])
    search_regex = re.compile(search_string, re.IGNORECASE)
    output = json.loads(dumps(collection.find({ "$or": [{ "title": search_regex },{ "artist": search_regex }]})))
    result = format_output(output)
    return result


def add_song_rating(id, rating, rating_collection, song_collection):
    print("rating function call, parameters id:%s rating:%f\n" % (id,rating), file=sys.stdout)
    try:
        id_search = song_collection.find({"_id": ObjectId(id) })
    except:
        result = "invalid MongoDB id"
        id_search = []
    print(dumps(id_search), file=sys.stdout)
    if id_search:
        if 1 <= rating <= 5:
            result = "adding rating to %s\n" % (id)
            rating_collection.insert_one({"song_id": id, "song_rating": rating})
        else:
            result = "invalid rating"
    else:
        result = "id: %s does not exist in the song database\n" % (id)
    return result

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

UPLOAD_FOLDER = "./upload/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app = Flask(__name__)
app.config['DEFAULT_RENDERERS'] = [
'flask.ext.api.renderers.JSONRenderer'
]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/songs/load/', methods=['POST'])
def route_songs_load():
    songs_db = connect_mongo(be_hostname, be_port)
    load_file = request.files['myfile']
    load_file.save(os.path.join(UPLOAD_FOLDER,"upload.json"))
    return import_data(os.path.join(UPLOAD_FOLDER,"upload.json"),songs_db), 201

@app.route('/songs/purge/', methods=['POST'])
def route_purge():
    songs_db = connect_mongo(be_hostname, be_port)
    songs_db.songs.drop()
    songs_db.ratings.drop()
    return "[PRKL] songs & ratings purged\n", 201


@app.route('/songs/', methods=['GET'])
def route_get_all():
    songs_db = connect_mongo(be_hostname, be_port)
    result = get_all(songs_db.songs)
    return jsonify(get_all(songs_db.songs)), 201

@app.route('/songs/avg/difficulty/', methods=['GET'])
def route_get_diff_above():
    songs_db = connect_mongo(be_hostname, be_port)
    level = request.args.get('level',default = 0, type = int)
    return jsonify(get_level_above(songs_db.songs, level)), 201

@app.route('/songs/search/', methods=['GET'])
def route_song_search():
    try:
        search = request.args.get('string', default = '')
    except:
        pass
    songs_db = connect_mongo(be_hostname, be_port)
    return jsonify(song_search(songs_db.songs, search)),201

@app.route('/songs/rating', methods = ['POST'])
def route_add_song_rating():
    songs_db = connect_mongo(be_hostname, be_port)
    song_id = request.form['song_id']
    rating = float(request.form['rating'])
    return add_song_rating(song_id, rating, songs_db.ratings, songs_db.songs), 201

@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
def route_get_song_rating(song_id):
    songs_db = connect_mongo(be_hostname, be_port)
    return jsonify(get_song_rating(song_id,songs_db.ratings)), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
