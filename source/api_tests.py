import sys

base_url = sys.argv[1]

tested_endpoints = {

"/songs":{"methods":["GET"]},
"/songs/avg/difficulty/":{"methods":["GET"],"variables":{"difficulty":"int"}},
"/songs/search/":{"methods":["GET"],"variables":{"string":"string"}},
"/songs/rating":{"methods":["POST"],"variables":{"song_id":"string","rating":"float"}},
"/songs/avg/rating":{"methods":["GET"],"variables":{"song_id":"string"}},

}
