import re
import os


def load(file, port):
    # port = int(port)
    # client = MongoClient('localhost', port)
    # f = open(file)  

    # db = client["291db"]
    # db.dblp.drop()
    # dblp = db["dblp"]
    # for line in f:
    #     dblp.insert_one(json.loads(line))
    # f.close()
    # client.close()
    os.system("mongoimport --port "+ port +" --db 291db --collection dblp --drop --file " + file + " --batchSize 100 --numInsertionWorkers 10")

#db.dblp.find({"or": [{"year":2013},{"year":2014}]})
  
def random():
    '''
    keywords = input("Enter keywords: ").split(" ")
    int_list = []

    for keyword in keywords:
        if keyword.isdigit():
            int_list.append(int(keyword))



    lst = keywords
    '''
    db = load('dblp-ref-10.json', 27017)
    dblp = db["dblp"]
    '''
    a = db.dblp.find({"$or":[{"abstract":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"title":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"authors":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"venue":{"$in":[re.compile(x,re.IGNORECASE) for x in lst]}},
                            {"year":{"$in":int_list}}]},{"references":0,"n_citation":0,"references":0,"authors":0,"abstract":0,"_id":0})
                    
    '''
    venues = db.dblp.aggregate([{"$group": {"_id":{"venue":"$venue"},"count":{"$sum": 1}}},{"$group": {"_id":"$_id.venue"}}])
    test = db.dblp.aggregate([{"$lookup":{
            "from": "dblp",
            "let": {"venue":"$venue", "id":"$id"},
            "pipeline": [
                {"$match":
                    {"$expr":
                    { "$and":
                        [
                           { "$eq": [ "$venue", "$$venue"] }
                        ]
                    }
                    }
                },
                {"$project": {"venue":1,"id":1,"_id":0}}
            ],
            "as":"articles"
            }
    },
    
    {"$group": {"_id":{"venue":"$venue","articles":"$articles.id"}, "count":{"$sum": 1}}},
    {"$unwind":"$references"},
    {"$lookup":{
            "from": "dblp",
            "let": {"venue":"$articles.venue", "id":"$id","references":"$references","ids":"$_id.articles.id"},
            "pipeline": [
                
                {"$match":
                {"$expr":
                    {"$and":
                        [  
                           #{"$in":["$$id","$$ids"]}
                           {"$setEquals":[["$$id"],"$$ids"]}
                        ]
                    }
                    
                    }
                },
                {"$project": {"title":1,"_id":0}}
            ],
            "as":"references"
            }
    }
    

    ])
    db.dblp.update_many(
        { "references": {"$exists":False}},
        { "$set": { "references": [] } },
        
        upsert = False
        )
    
    test1 = db.dblp.aggregate(
        [
        
        {"$group": {"_id":"$venue", "ids": {"$push":"$id"}, "count":{"$sum": 1}}},
        {"$unwind": "$ids"},
        {"$lookup": {
            "from": "dblp",
            "let": {"id":"$ids","referecnes":"$references"},
            "pipeline": [
                
                {"$match":
                {"$expr":
                    {"$and":
                        [  
                           {"$in":["$$id","$references"]}
                          
                        ]
                    }
                    
                    }
                },
                #{"$count": "ref_count"},
                {"$project": {"title":1,"_id":0}},
            ],
            "as":"references"

        }},
        {"$unwind": "$references"},
        {"$group":{"_id":{"name":"$_id","count":"$count", "ref":"$references"}}},
        {"$project": {"title":"$_id.name","count":"$_id.count","references":"$_id.ref","_id":0}},
        {"$group":{"_id":"$title","count":{"$first":"$count"},"ref_count":{"$push":"$references"}}},
        {"$project": {"_id":1,"count":1,
                 "refCount": { "$size": "$ref_count" } }
        },
         {"$group":{"_id":"$_id","count":{"$first":"$count"},"ref_count":{"$sum":"$refCount"}}},
         {"$sort":{"ref_count":-1}},
         {"$limit":1}
        #{"$unwind":"$ref_count"},
        #{"$unwind":"$ref_count"},
       
        
        
         
         
    ])
    
    for a in test1:
        print(a)

        

    '''
    for venue in venues:
        venue_name = venue["_id"]
        venue_article_ids =[] 
        #c = db.dblp.find({"venue":venue_name})
        c = db.dblp.aggregate([{"$match":{"venue":venue_name}},{"$project":{}}])
        for d in c:
            #venue_article_ids.append(d["id"])
            print(d)

        #count = db.dblp.count_documents({"references": {"$in":[re.compile(x) for x in venue_article_ids]}})
        #print("reference count", count)
        #venue["reference_count"] = count
    '''
    
    
    for b in venues:
        #print(b)
        pass

    

        
        #c = db.dblp.aggregate([{"$match": {"venue":venue}}])
        
def top_n_venues(db):
    
    
    n = input("Enter the top number of venues: ")

    db.dblp.update_many(
        { "references": {"$exists":False}},
        { "$set": { "references": [] } },
        
        upsert = False
        )

    top_venues = db.dblp.aggregate(
        [
        
        {"$group": {"_id":"$venue", "ids": {"$push":"$id"}, "count":{"$sum": 1}}},
        {"$unwind": "$ids"},
        {"$lookup": {
            "from": "dblp",
            "let": {"id":"$ids","referecnes":"$references"},
            "pipeline": [
                
                {"$match":
                {"$expr":
                    {"$and":
                        [  
                           {"$in":["$$id","$references"]}
                          
                        ]
                    }
                    
                    }
                },
                #{"$count": "ref_count"},
                {"$project": {"title":1,"_id":0}},
            ],
            "as":"references"

        }},
        {"$unwind": "$references"},
        {"$group":{"_id":{"name":"$_id","count":"$count", "ref":"$references"}}},
        {"$project": {"title":"$_id.name","count":"$_id.count","references":"$_id.ref","_id":0}},
        {"$group":{"_id":"$title","count":{"$first":"$count"},"ref_count":{"$push":"$references"}}},
        {"$project": {"_id":1,"count":1,
                 "refCount": { "$size": "$ref_count" } }
        },
         {"$group":{"_id":"$_id","count":{"$first":"$count"},"ref_count":{"$sum":"$refCount"}}},
         {"$sort":{"ref_count":-1}},
         {"$limit":int(n)}
        
    
    ])

    for venue in top_venues:
        print("Venue:",venue["_id"], "| Number of articles in venue:", venue["count"], "| Number of references:", venue["ref_count"])
    

    




