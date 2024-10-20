from pymongo import MongoClient

try:
    conn = MongoClient("mongodb+srv://blpamritesh:oo8HCnX92eCTUbNY@mongotest.stuir.mongodb.net/")
    db = conn.notes
    docs = db.notes.find({})
    for doc in docs:
        print(doc)
except Exception as e:
    print(f"Error: {e}")
