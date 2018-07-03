import json, sys
from pymongo import MongoClient as mongo

be_hostname = "localhost"
be_port = 27017

def connectMongoDB(ip,port):
    client = mongo(ip,port)
    dbase = client.prkl
    return dbase

def getAll(collection):
    cursor = collection.find({})
    result = {}
    for document in cursor:
        result[document.get('_id')]=document
    return result

songs_db = connectMongoDB(be_address,be_port)
print getAll(songs_db.songs)
