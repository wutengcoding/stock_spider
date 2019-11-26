import scrapy
import time
import json
from db_utils import *


class StockListSpider(scrapy.Spider):
    name = "stock_detail"
    allowed_domains = ["xueqiu.com"]


    def start_requests(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        cookies = {
            'xq_a_token':'f225dc6f48faedd78b6fd2ce39b645eb69a49278'
        }

        start_urls = []

        # endTs = int(round(time.time() * 1000)) - 1000 * 3600 * 24 * 1
        # beginTs = endTs - 1000 * 3600 * 24 * 100

        endTs = int(round(time.time() * 1000))
        beginTs = endTs - 1000 * 3600 * 24 * 79
        print(beginTs, endTs)

        # with open("stock_list.log") as f:
        #     for line in f.readlines():
        #         start_urls.append("https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}&_={}".format(line, beginTs, endTs, endTs))

        stock_id_list = query_all_stockid()
        print('The query urls limit 10 is ', stock_id_list[:10])
        for line in stock_id_list[:2]:
            start_urls.append("https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}&_={}".format(line, beginTs, endTs, endTs))

        '''
        SZ399006 
        
        SZ399001
        SH000001 
        '''

        for url in start_urls:
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    def parse(self, response):
        resp = json.loads(response.body)
        data = {'stock_id': resp['stock']['symbol'], 'chartlist': resp['chartlist']}
        insert_tail_data(data)
        # insert_single_detail(data)
        # print(data)

        # with open("data/" + resp['stock']['symbol'], 'wb') as f:
        #     print(response.body)

