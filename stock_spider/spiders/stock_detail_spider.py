import scrapy
import time
import json
import datetime
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

        endTs = int(round(time.time() * 1000))
        beginTs = endTs - 1000 * 3600 * 24 * 200

        today = datetime.datetime.now().strftime("%Y%m%d")
        daysAgo = (datetime.datetime.now() - datetime.timedelta(days=120)).strftime("%Y%m%d")


        # with open("stock_list.log") as f:
        #     for line in f.readlines():
        #         start_urls.append("https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}&_={}".format(line, beginTs, endTs, endTs))

        stock_id_list = query_all_stockid()
        print('The query urls limit 10 is ', stock_id_list[:10])
        for line in stock_id_list[:2]:
            stock_code = '0' + line[2:]
            start_urls.append("http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
                              .format(stock_code, daysAgo, today))
            # start_urls.append("https://xueqiu.com/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}&_={}".format(line, beginTs, endTs, endTs))

        '''
        SZ399006 
        
        SZ399001
        SH000001 
        '''

        for url in start_urls:
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    def parse(self, response):
        pass
        # resp = json.loads(response.body)
        # insert_tail_data(data)
        # insert_single_detail(data)
        # print(data)

        # with open("data/" + resp['stock']['symbol'], 'wb') as f:
        #     print(response.body)

