import scrapy
from ..items import HistoryDetailItem
from db_utils import *
import datetime


class HistoryItemSpider(scrapy.Spider):
    name = "history_stock"
    allowed_domains = ["quotes.money.163.com"]
    start_urls = ['http://quotes.money.163.com/stock']

    def parse(self, response):
        today = datetime.datetime.now().strftime("%Y%m%d")
        daysAgo = (datetime.datetime.now() - datetime.timedelta(days=120)).strftime("%Y%m%d")

        #stock_id_list = query_all_stockid()
        stock_id_list = []
        with open('/Users/wuteng/myspace/stock_spider/stock_list.log') as f:
            stock_id_list = [line.strip() for line in f.readlines()]
        print('The query urls limit 10 is ', stock_id_list[:10])
        stock_urls = []
        for line in stock_id_list[:3]:
            stock_code = '1' + line[2:]
            stock_urls.append("http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(stock_code, daysAgo, today))
        print("the query urls is ", stock_urls)

        for url in stock_urls:
            yield HistoryDetailItem(file_urls=[url])
