from pymongo import MongoClient
import json



def load(file, port):
    client = MongoClient('localhost', port)
    f = open(file)  
    db = client["291db"]
    dblp = db["dblp"]
    for line in f:
        dblp.insert_one(json.loads(line))
    f.close()

    


load('dblp-ref-10.json', 27017)
