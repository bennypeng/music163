# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import PlaylistsItem


class PlaylistsSpider(scrapy.Spider):
    name = 'playlists'
    allowed_domains = ['music.163.com']
    base_url = 'https://music.163.com'

    unit_convert = {'万': '10000', '亿': '100000000'}

    custom_settings = {
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'music163.middlewares.ProxyMiddleware': 100,
        # },
        'ITEM_PIPELINES': {
            'music163.pipelines.PlaylistsPipeline': 300,
        }
    }

    def start_requests(self):
        url = self.base_url + '/discover/playlist'
        yield scrapy.Request(url, callback=self.parse_cat)

    def parse_cat(self, response):
        cat_list = response.xpath('//div[@id="cateListBox"]//div[@class="bd"]//dl[@class="f-cb"]/dd/a[@class="s-fc1 "]/@href').extract()
        # cat_list = ['/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD']
        for cat in cat_list:
            cat_url = self.base_url + cat
            # print(cat_url)
            yield scrapy.Request(cat_url, callback=self.parse_page_pre)

    def parse_page_pre(self, response):
        playlist_url_list = []
        in_show_albums_pages = response.xpath('//div[@class="u-page"]/a[@class="zpgi"]/@href').extract()
        last_item = in_show_albums_pages[-1:]  # 最后一页
        if last_item:
            temp = last_item[0].split('&')
            if len(temp) == 4:
                cat = temp[1][4:]
                limit = temp[2][6:]
                total = temp[3][7:]
                for offset in range(0, int(total) + 1, int(limit)):
                    playlist_url = self.base_url + '/discover/playlist/?cat=%s&limit=%s&offset=%s' % (cat, limit, offset)
                    playlist_url_list.append(playlist_url)
        # print(playlist_url_list)
        # playlist_url_list = ['https://music.163.com/discover/playlist/?order=hot&cat=华语&limit=35&offset=0']
        for playlist_url in playlist_url_list:
            yield scrapy.Request(playlist_url, callback=self.parse_page)

    def parse_page(self, response):
        playlist_url_list = response.xpath('//ul[@id="m-pl-container"]//a[@class="msk"]/@href').extract()

        # playlist_url_list = ['/playlist?id=988690134']

        for k, url in enumerate(playlist_url_list):
            playlist_id = url[13:]
            playlist_url = self.base_url + url
            yield scrapy.Request(playlist_url, callback=self.parse_playlist, meta={'playlist_id': playlist_id})

    def parse_playlist(self, response):
        id = response.meta['playlist_id']
        name = response.xpath('//div[@id="m-playlist"]//div[@class="cnt"]//div[contains(@class,"tit")]/h2/text()').extract_first()
        collect_data = response.xpath('//div[@id="content-operation"]/a[3]/i/text()').extract_first()
        transmit_data = response.xpath('//div[@id="content-operation"]/a[4]/i/text()').extract_first()
        play_count = response.xpath('//strong[@id="play-count"]/text()').extract_first()
        tags = response.xpath('//div[@id="m-playlist"]//div[@class="cntc"]//a[@class="u-tag"]/i/text()').extract()

        collect_count = re.findall(r'\d+', collect_data)
        transmit_count = re.findall(r'\d+', transmit_data)
        collect_count = int(collect_count[0]) if collect_count else 0
        transmit_count = int(transmit_count[0]) if transmit_count else 0
        play_count = int(play_count) if play_count else 0

        # 单位转换
        for key in self.unit_convert:
            if key in collect_data:
                num = int(self.unit_convert[key])
                collect_count *= num

            if key in transmit_data:
                num = int(self.unit_convert[key])
                transmit_count *= num

        self.logger.info('%s\t%s\t%s\t%s\t%s\t%s' % (id, name, tags, collect_count, transmit_count, play_count))

        item = PlaylistsItem()
        for field in item.fields:
            try:
                item[field] = eval(field)
            except NameError:
                print('Field is not defined', field)
        yield item
