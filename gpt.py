import pymongo

conn = pymongo.MongoClient()
db= conn.get_database('testdb')
coll = db.testcollection

def add_data(name ,time,dominant_emotion):
    document = {
        "NAME":name,
        'TIME':time,
        'DOMINANT_EMOTION':dominant_emotion
    }
    return coll.insert_one(document)

