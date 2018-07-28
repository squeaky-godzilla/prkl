from __future__ import print_function
import os
import sys
import json
import re
from datetime import datetime
from pymongo import MongoClient as mongo
from pymongo import TEXT
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, jsonify, Flask, abort


sys.path.insert(0, './snippets')
from checks import format_chk


def logger(message):
    print("[PRKL API log] %s\n" % (message), file=sys.stdout)


#mongoDB song collection format

record_format = {
                    "artist": "unicode",
                    "title": "unicode",
                    "difficulty": "float",
                    "level": "int",
                    "released": '%Y-%m-%d'
                }

# date_format = '%Y-%m-%d'

def logger(message):
    timestamp = datetime.now()
    print("[PRKL API log] %s -- %s\n" % (timestamp, message), file=sys.stdout)

#settings variables
BE_HOSTNAME = "localhost"
BE_PORT = 27017

#arguments input
try:
    BE_HOSTNAME, BE_PORT = sys.argv[1].split(':')
    BE_PORT = int(BE_PORT)
except:
    pass


def connect_mongo(ip, port):
    client = mongo(ip, port)
    dbase = client.prkl
    return dbase

# simplifies the output of mongo queries,
# putting object id: song record as key value pair
def format_output(output):
    result = {}
    try:
        for item in output:
            result[item["_id"]["$oid"]] = item
            result[item["_id"]["$oid"]].pop("_id")
    except Exception, err:
        logger(str(err))
        result = output
    return result


def insert_song(song_dictionary, dbase):
    songs_db = dbase.songs
    songs_db.insert_one(song_dictionary)


def import_data(json_file, dbase):
    json_obj = open(json_file, "r")
    logger("[PRKL import] loading file %s ... testing for format defects" % (str(json_file)))
    for line in json_obj:
        bad_keys = format_chk(json.loads(line), record_format, record_format["released"])
        if len(bad_keys) > 0:
            logger("invalid song import file .. aborting")
            abort(400)
        else:
            pass
    json_obj.close()
    json_obj = open(json_file, "r")
    for idx, line in enumerate(json_obj):
        try:
            print(line)
            insert_song(json.loads(line), dbase)
        except Exception, err:
            logger("[PRKL import] line %i: %s" % (idx,str(err)))
    json_obj.close()
    return ("[PRKL import] collection now has total %i records\n"
            % (dbase.songs.count()))


def get_all(collection, per_page, offset, prev_page, next_page):
    result = jsonify({
                        'result': format_output(json.loads(
                            dumps(collection.find({}).
                            skip(offset).limit(per_page)))),
                        'prev_page': prev_page, 'next_page': next_page})
    return result


def get_level_above(collection, level):
    if type(level).__name__ != "int":
        logger("invalid level input ... aborting")
        abort(400)
    else:
        avg_difficulty_output = json.loads(dumps(collection.aggregate([
                        {"$group": {"_id": "null", "avg_difficulty":
                                    {"$avg": "$difficulty"}
                                    }}])))
        avg_difficulty = {}
        avg_difficulty['avg_difficulty'] = \
            avg_difficulty_output[0]['avg_difficulty']
        output = json.loads(dumps(collection.find({"level":  {"$gt": level}})))
        result = format_output(output)
        return [result, avg_difficulty]


def song_search(collection, search_string):
    collection.create_index([('artist', TEXT), ('title', TEXT)])
    search_regex = re.compile(search_string, re.IGNORECASE)
    output = json.loads(dumps(collection.find(
                {"$or": [
                    {"title": search_regex},
                    {"artist": search_regex}]})))
    result = format_output(output)
    return result


def add_song_rating(id, rating, rating_collection, song_collection):
    logger("rating function call, parameters id:%s rating:%f\n" % (id, rating))
    try:
        id_search = song_collection.find({"_id": ObjectId(id)})
    except Exception, err:
        logger(err)
        id_search = None
        abort(400)
    print(dumps(id_search), file=sys.stdout)
    if id_search != None:
        if 1 <= rating <= 5:
            result = "adding rating to %s\n" % (id)
            rating_collection.insert_one({"song_id": id, "song_rating": rating})
        else:
            logger("invalid rating")
            abort(400)
    else:
        result = "id: %s does not exist in the song database\n" % (id)
    return result

def get_song_rating(id, rating_collection):
    # print(dumps(rating_collection.find({})), file=sys.stdout)
    try:
        avg_rating_output = json.loads(dumps(rating_collection.aggregate([
                        {"$match": {"song_id": id}},
                        {"$group":
                            {"_id": "null", "avg_rating":
                                {"$avg": "$song_rating"}}}
                        ])))[0]["avg_rating"]
        max_rating_output = json.loads(dumps(rating_collection.aggregate([
                        {"$match": {"song_id": id}},
                        {"$group":
                            {"_id": "null", "max_rating":
                                {"$max": "$song_rating"}}}
                        ])))[0]["max_rating"]
        min_rating_output = json.loads(dumps(rating_collection.aggregate([
                        {"$match": {"song_id": id}},
                        {"$group":
                            {"_id": "null", "min_rating":
                                {"$min": "$song_rating"}}}
                        ])))[0]["min_rating"]
        result = {id: {"avg": avg_rating_output, "max": max_rating_output, "min": min_rating_output}}
    except Exception, err:
        logger(err)
        abort(400)


UPLOAD_FOLDER = "./upload/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app = Flask(__name__)
app.config['DEFAULT_RENDERERS'] = [
'flask.ext.api.renderers.JSONRenderer'
]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logger("MongoDB host set to: %s:%s" % (BE_HOSTNAME, BE_PORT))


@app.route('/songs/load/', methods=['POST'])
def route_songs_load():
    songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
    load_file = request.files['myfile']
    load_file.save(os.path.join(UPLOAD_FOLDER,"upload.json"))
    try:
        return import_data(os.path.join(UPLOAD_FOLDER,"upload.json"),songs_db), 201
    except:
        abort(500)

@app.route('/songs/purge/', methods=['POST'])
def route_purge():
    try:
        songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
        songs_db.songs.drop()
        songs_db.ratings.drop()
        logger("all songs & ratings purged")
        return "all songs & ratings purged\n", 201
    except:
        abort(500)


@app.route('/songs/avg/difficulty/', methods=['GET'])
def route_get_diff_above():
    try:
        songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
        level = request.args.get('level', default = 0)
        logger("level: %s, %s" % (str(level),type(level).__name__))
        level = int(level)
        if type(level).__name__ != "int":
            raise Exception("level param is not a valid integer")
    except Exception, err:
        logger(err)
        abort(400)
    try:
        return jsonify(get_level_above(songs_db.songs, level)), 200
    except Exception, err:
        logger(err)
        abort(500)


@app.route('/songs/search', methods=['GET'])
def route_song_search():
    try:
        search = request.args.get('message', default = '')
    except:
        pass
    try:
        songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
        return jsonify(song_search(songs_db.songs, search)), 200
    except:
        abort(500)


@app.route('/songs/', methods=['GET'])
def route_allsongs_paginated():
    try:
        per_page = int(request.args.get('per_page', default='0'))
        offset = int(request.args.get('offset', default='0'))
    except Exception, err:
        logger(err)
        abort(400)
    next_page = "%s?per_page=%s&offset=%s" % (request.base_url,str(per_page), str(offset + per_page))
    prev_page = "%s?per_page=%s&offset=%s" % (request.base_url,str(per_page), str(offset - per_page))
    try:
        songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
        return get_all(songs_db.songs, per_page, offset, prev_page, next_page), 200
    except Exception, err:
        logger(err)
        abort(500)


@app.route('/songs/rating', methods=['POST'])
def route_add_song_rating():
    try:
        song_id = request.form['song_id']
        rating = int(request.form['rating'])
    except Exception, err:
        logger(err)
        abort(400)
    songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
    return add_song_rating(song_id, rating, songs_db.ratings, songs_db.songs), 201


@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
def route_get_song_rating(song_id):
    try:
        songs_db = connect_mongo(BE_HOSTNAME, BE_PORT)
        return jsonify(get_song_rating(song_id, songs_db.ratings))
    except Exception, err:
        logger(err)
        abort(400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
