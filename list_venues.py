def list_venues(db) -> None:
    venue_count = input("Provide the number of top venues to search for: ")
    is_valid_number = False
    while not is_valid_number:
        try:
            venue_count = int(venue_count)
            assert venue_count > 0
            is_valid_number = True
        except:
            venue_count = input("Not a positive integer. Try again: ")

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
         {"$limit":int(venue_count)}
        
    
    ])

    for venue in top_venues:
        print("Venue:",venue["_id"], "| Number of articles in venue:", venue["count"], "| Number of references:", venue["ref_count"])
