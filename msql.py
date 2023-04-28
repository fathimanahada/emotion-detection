from pymongo import MongoClient
 

client = MongoClient("mongodb+srv://fathimanahada06:fnhd_681@cluster0.clnokkg.mongodb.net/?retryWrites=true&w=majority")
#db
db= client.get_database('testdb')
#collection
records = db.test_records
records.count_documents({})

# new_data = {
#     "name":"efd",
#     "age":"21",
#     "branch" : "cse"
# }
records.update_one({"name": "abcd"},
                   {'$set':{'name':'nahada','branch':'mech'}})

#records.delete_many({"name:nimitha"})
#delet.delete_count()
#records.insert_one(new_data)
# results=records.find({})
# for result in results:
#      print(result)