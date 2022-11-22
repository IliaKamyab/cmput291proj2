from pymongo import MongoClient
import json
import re



def load(file, port):
    port = int(port)
    client = MongoClient('localhost', port)
    f = open(file)  

    db = client["291db"]
    db.dblp.drop()
    dblp = db["dblp"]
    for line in f:
        dblp.insert_one(json.loads(line))
    f.close()
    return db


#db.dblp.find({"or": [{"year":2013},{"year":2014}]})
  
def random():
    keywords = input("Enter keywords: ").split(" ")
    int_list = []

    for keyword in keywords:
        if keyword.isdigit():
            int_list.append(int(keyword))



    lst = keywords
    db = load('dblp-ref-10.json', 27017)
    dblp = db["dblp"]

    a = db.dblp.find({"$or":[{"abstract":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"title":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"authors":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"venue":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"year":{"$in":int_list}}]},{"references":0,"n_citation":0,"references":0,"authors":0,"abstract":0,"_id":0})
                            




