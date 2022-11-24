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
  
