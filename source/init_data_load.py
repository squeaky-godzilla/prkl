import json, sys
from pymongo import MongoClient as mongo

source_file = sys.argv[1]
try:
    purge = sys.argv[2]
except:
    purge = "nope"

def connectMongoDB(ip,port):
    client = mongo(ip,port)
    dbase = client.prkl
    return dbase

def insertSong(json,dbase):
    songs = dbase.songs
    song_id = songs.insert_one(json)

def importData(json_file, dbase):
    json_obj = open(json_file,"r")
    print "[PRKL import] loading file %s" % (str(json_file))
    for line in json_obj:
        # json_list.append(json.loads(line))
        insertSong(json.loads(line), dbase)
    print "[PRKL import] collection now has total %i records" % (prkl_dbase.songs.count())

prkl_dbase = connectMongoDB('100.0.10.10',27017)
if purge.lower() == "purge":
    try:
        print "[PRKL purge] purging songs collection"
        prkl_dbase.songs.drop()
    except:
        pass
importData(source_file,prkl_dbase)
