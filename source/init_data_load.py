import json, sys
from pymongo import MongoClient as mongo


source_file = sys.argv[1]

be_hostname, be_port = sys.argv[2].split(':')



def connect_mongo(ip,port):
    print "[PRKL import] connecting to %s:%i" % (ip,port)
    client = mongo(ip,port)
    dbase = client.prkl
    return dbase

def insert_song(json,dbase):
    songs = dbase.songs
    song_id = songs.insert_one(json)

def import_data(json_file, dbase):
    json_obj = open(json_file,"r")
    print "[PRKL import] loading file %s" % (str(json_file))
    for line in json_obj:
        # json_list.append(json.loads(line))
        insert_song(json.loads(line), dbase)
    print "[PRKL import] collection now has total %i records" % (prkl_dbase.songs.count())

prkl_dbase = connect_mongo(be_hostname,int(be_port))
print "[PRKL purge] purging songs collection"
prkl_dbase.songs.drop()
import_data(source_file,prkl_dbase)
