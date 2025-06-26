from pymongo import MongoClient

client = None
db = None

def init_db(uri, dbname):
    global client, db
    client = MongoClient(uri)
    db = client[dbname]

def get_db():
    return db
