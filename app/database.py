from pymongo import MongoClient

MONGO_URL = "mongodb+srv://harshitd891:LHw8hTmYbljcf9Bc@cluster0.2edjw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URL)
db = client.Cluster0

def get_db():
    return db