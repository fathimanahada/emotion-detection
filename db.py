from pymongo import MongoClient
 
client = MongoClient("mongodb+srv://fathimanahada06:fnhd_681@cluster0.clnokkg.mongodb.net/?retryWrites=true&w=majority")
#db
db = client.get_database('emotion')
#collection
records = db.collection

# def add_data(name, time, dominant_emotion):
#     document = {
#         "Name": name,
#         "Time": time,
#         "Dominant_emotion": dominant_emotion
#     }
#     return records.insert_one(document)
records.delete_many({})
