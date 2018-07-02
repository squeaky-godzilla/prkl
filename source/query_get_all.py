import json, sys

json_file = sys.argv[1]

def testQuery(json_file):
    json_obj = open(json_file,"r")
    json_list = []
    for line in json_obj:
        json_list.append(json.loads(line))
    return json_list

print testQuery(json_file)
