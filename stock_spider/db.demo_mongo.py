import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["stock_spider"]
mycol2 = mydb["stock_detail"]

for x in mycol2.find():
  print(x['chartlist'][-1])