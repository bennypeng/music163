# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotcommentsItem(scrapy.Item):
    table_name = 'hotcomments'
    album_id = scrapy.Field()
    music_id = scrapy.Field()
    artist_name = scrapy.Field()
    music_name = scrapy.Field()
    comments = scrapy.Field()


class ProxiesItem(scrapy.Item):
    table_name = 'proxies'
    proxy = scrapy.Field()

