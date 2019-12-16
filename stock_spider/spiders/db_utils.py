import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["stock_spider"]

TABLE_NAME = 'stock_detail'

# def insert_all_stockid(stock_list):
#     if len(stock_list) > 0:
#         print(stock_list[:10])
#         mylist = [{'id': stock_id} for stock_id in stock_list]
#         mydb["stock_list"].insert_many(mylist)
#
#
# def insert_single_detail(data):
#     print("insert single data", data)
#     mydb[TABLE_NAME].insert_one(data)
#
# def insert_tail_data(data):
#     print("Appending the last day data", len(data['chartlist']), 'end date is ', data['chartlist'][-1])
#     stock_query = {'stock_id': data['stock_id']}
#     newvalues = {"$set": {"chartlist": data['chartlist']}}
#     mydb[TABLE_NAME].update_one(stock_query, newvalues)
#
# def query_all_stockid():
#     res = []
#     for stock_id in mydb["stock_list"].find():
#         res.append(stock_id['id'])
#     return res