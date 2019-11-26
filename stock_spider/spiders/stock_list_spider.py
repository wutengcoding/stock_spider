import sys
from os.path import dirname, abspath
base_dir = dirname(abspath(__file__))
sys.path.append(base_dir)

import scrapy
from db_utils import *

class StockListSpider(scrapy.Spider):
    name = "stock_list"
    allowed_domains = ["eastmoney.com"]
    start_urls = [
        "http://quote.eastmoney.com/stock_list.html"
    ]

    def parse(self, response):
        filename = "stock_list.log"

        # with open(filename, 'w') as f:
        #     for sel in response.xpath("//div/div[contains(@class, 'quotebody')]/div/ul/li"):
        #         name = sel.xpath("a/text()").extract()[0]
        #         link = sel.xpath('a/@href').extract()[0]
        #         stock_code = name.strip(")").split("(")[1]
        #         # if stock_code[0] != '5':
        #         if stock_code[:3] == "300":
        #             # print(link.strip('.html').split('/')[-1])
        #             f.write(link.strip('.html').split('/')[-1] + '\n')

        stock_list = []
        for sel in response.xpath("//div/div[contains(@class, 'quotebody')]/div/ul/li"):
            name = sel.xpath("a/text()").extract()[0]
            link = sel.xpath('a/@href').extract()[0]
            stock_code = name.strip(")").split("(")[1]
            # if stock_code[0] != '5':
            if stock_code[:3] == "300":
                # print(link.strip('.html').split('/')[-1])
                stock_list.append(link.strip('.html').split('/')[-1])

        insert_all_stockid(stock_list)

        query_all_stockid()