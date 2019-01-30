# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotcommentsItem(scrapy.Item):
    table_name = 'hotcomments'
    album_id = scrapy.Field()         # 专辑id
    music_id = scrapy.Field()         # 音乐id
    artist_name = scrapy.Field()      # 艺术家名
    music_name = scrapy.Field()       # 音乐名
    comments = scrapy.Field()         # 评论


class ProxiesItem(scrapy.Item):
    table_name = 'proxies'
    proxy = scrapy.Field()            # 代理


class PlaylistsItem(scrapy.Item):
    table_name = 'playlists'
    id = scrapy.Field()               # 歌单id
    name = scrapy.Field()             # 歌单名
    tags = scrapy.Field()              # 所属标签
    play_count = scrapy.Field()       # 播放量
    collect_count = scrapy.Field()    # 收藏量
    transmit_count = scrapy.Field()   # 转发量

