import scrapy
import time
import json


class StockListSpider(scrapy.Spider):
    name = "stock_detail"
    allowed_domains = ["xueqiu.com"]


    def start_requests(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        cookies = {
            'xq_a_token':'84f0424d3a6b572dacb4b96523ba04f140b1f254'
        }

        start_urls = []

        # beginTs = "1478620800000"
        # endTs = "1510126200000"
        endTs = int(round(time.time() * 1000))
        beginTs = endTs - 1000 * 3600 * 24 * 100

        # with open("stock_list.log") as f:
        #     for line in f.readlines():
        #         start_urls.append("https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}&_={}".format(line, beginTs, endTs, endTs))
        start_urls.append(
            "https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}&_={}".format(
                "SZ300002", beginTs, endTs, endTs))
        '''
        SZ399006 
        
        SZ399001
        SH000001 
        '''

        for url in start_urls:
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    def parse(self, response):
        resp = json.loads(response.body)
        with open("data/" + resp['stock']['symbol'], 'wb') as f:
            f.write(response.body)

