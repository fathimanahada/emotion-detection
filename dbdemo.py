from pymongo import MongoClient

 
client = MongoClient("mongodb+srv://fathimanahada06:fnhd_681@cluster0.clnokkg.mongodb.net/?retryWrites=true&w=majority")
 #db
db = client.get_database('emotion')
#collection
records = db.collection
records.delete_one({"name":"Nahada1.png (93.93%)"})
#delet.delete_count()
# records.insert_one(new_data)
# results=records.find({})
# for result in results:
#       print(result)
print(records.deleted_count)