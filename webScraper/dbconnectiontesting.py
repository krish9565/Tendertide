from pymongo import *
try:
    client=MongoClient("mongodb://localhost:27017")
    client.admin.command("ping")
    MongoClient("mongodb://localhost:27017/")
    db=client['newDB2']
    collection=db['users']
    print("connected")
except:
    print("Not connnected")

