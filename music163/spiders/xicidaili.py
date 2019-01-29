# -*- coding: utf-8 -*-
import scrapy
import pymongo
import requests
from ..settings import MONGO_CONFIG
from ..items import ProxiesItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from twisted.internet.error import ConnectionRefusedError


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com', 'httpbin.org']
    base_url = 'https://www.xicidaili.com'
    ip_test_url = 'http://httpbin.org/ip'
    pages = 2  # 爬取的页数
    type_list = ['nn', 'nt', 'wt']  # 高匿/普通/国内http

    custom_settings = {
        'ITEM_PIPELINES': {
            'music163.pipelines.ProxiesPipeline': 301,
        }
    }

    #  预处理失效代理
    def __init__(self):
        self.logger.info('=================recheck proxy start=================')
        client = pymongo.MongoClient(host=MONGO_CONFIG['proxy']['host'])
        db = client[MONGO_CONFIG['proxy']['db']]
        proxy_list = db['proxies'].find()
        for data in proxy_list:
            try:
                response = requests.get(self.ip_test_url, proxies={'http': data['proxy']}, timeout=5)
                self.logger.info('test proxy %s ok.' % (data['proxy']))
            except Exception as e:
                db['proxies'].remove(data)
                self.logger.info('invalid proxy %s, remove it.' % (data['proxy']))
        self.logger.info('=================recheck proxy end=================')

    def start_requests(self):
        for page in range(1, self.pages + 1):
            for itype in self.type_list:
                url = self.base_url + '/' + itype + '/' + str(page)
                yield scrapy.Request(url, callback=self.parse_proxy)

    def parse_proxy(self, response):
        ip_port_list = response.xpath('//*[@id="ip_list"]/tr/td[2]/text()|//td[3]/text()|//td[6]/text()').extract()
        ip_list = ip_port_list[::3]
        port_list = ip_port_list[1::3]
        # protocol_type_list = ip_port_list[2::3]
        for i in range(0, len(ip_list)-1):
            # protocol_type = protocol_type_list[i]
            # ip_for_test = str.lower(protocol_type) + '://' + ip_list[i] + ':' + port_list[i]
            # 暂不考虑https，全部按照http处理
            ip_for_test = 'http://' + ip_list[i] + ':' + port_list[i]
            yield scrapy.Request(
                self.ip_test_url,
                callback=self.parse,
                errback=lambda failure: self.parse_error(failure, ext={'proxy': ip_for_test}),
                meta={'proxy': ip_for_test, 'download_timeout': 5},
                dont_filter=True)

    def parse(self, response):
        if response.status == 200:
            proxy = response.meta['proxy']
            self.logger.info('Url: %s, Proxy: %s, Status code: %s.'
                             % (self.ip_test_url, proxy, str(response.status)))
            item = ProxiesItem()
            for field in item.fields:
                try:
                    item[field] = eval(field)
                except Exception as e:
                    print('field not defined')
            yield item

    def parse_error(self, failure, ext):
        request = failure.request
        if failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error('Url: %s, Proxy: %s timeout.'
                              % (request.url, ext['proxy']))
        elif failure.check(ConnectionRefusedError):
            self.logger.error('Url: %s, Proxy: %s connection refused.'
                              % (request.url, ext['proxy']))
        elif failure.check(HttpError):
            response = failure.value.response
            self.logger.error('Url: %s, Proxy: %s, Status code: %s.'
                              % (request.url, response.meta['proxy'], str(response.status)))
        else:
            self.logger.error('Url: %s, Proxy: %s unknow error.' % (request.url, ext['proxy']))
