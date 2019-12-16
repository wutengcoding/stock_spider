# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse, parse_qs
import pandas as pd
import json
import pymongo



class MyFilePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        params = parse_qs(urlparse(request.url).query)
        print(params)
        return params['code'][0][1:] + ".csv"
        # return join(basename(dirname(path)),basename(path))

class MongoPipeline(object):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["stock_spider"]

    def process_item(self, item, spider):
        filepath = spider.settings.get('FILES_STORE') +"\\" + item['files'][0]['path']
        filename = item['files'][0]['path'].split(".")[0]
        data = pd.read_csv(filepath, encoding="gbk")
        data_json = json.loads(data.to_json(orient="records"))
        self.mydb[filename].insert_many(data_json)