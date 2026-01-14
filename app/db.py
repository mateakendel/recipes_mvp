from pymongo import MongoClient
import time

uri = "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0"

for _ in range(30):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        break
    except Exception:
        time.sleep(1)
else:
    raise RuntimeError("MongoDB replica set not available")

db = client["recepti_db"]
users = db.users
recipes = db.recipes
