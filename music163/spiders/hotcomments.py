# -*- coding: utf-8 -*-
import json
import scrapy
from ..settings import DEFAULT_REQUEST_HEADERS
from ..items import HotcommentsItem


class HotcommentsSpider(scrapy.Spider):
    name = 'hotcomments'
    allowed_domains = ['163.com']
    base_url = 'https://music.163.com'
    # ids = ['1001', '1002', '1003',
    #        '2001', '2002', '2003',
    #        '4001', '4002', '4003',
    #        '6001', '6002', '6003',
    #        '7001', '7002', '7003']
    # initials = range(65, 91)  # A-Z
    # initials = [i for i in range(65, 91)]+[0]

    ids = ['1001']
    initials = ['67']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'music163.middlewares.RandomUserAgentMiddleware': 1,
            'music163.middlewares.ProxyMiddleware': 100,
        },
        'ITEM_PIPELINES': {
            'music163.pipelines.HotCommentsPipeline': 300,
        }
    }

    def start_requests(self):
        for id in self.ids:
            for initial in self.initials:
                url = '{url}/discover/artist/cat?id={id}&initial={initial}' . format(url=self.base_url, id=id, initial=initial)
                yield scrapy.Request(url, callback=self.parse_index)

    def parse_index(self, response):
        artists = response.xpath('//ul[@id="m-artist-box"]/li[@class="sml"]//a[1]/@href').extract()
        # print(artists)
        # artists = ['/artist?id=2116']
        for artist in artists:
            artist_url = self.base_url + '/artist' + '/album?' + artist[8:]
            yield scrapy.Request(artist_url, callback=self.parse_artist_pre)

    def parse_artist_pre(self, response):
        album_url_list = [response.request.url]
        in_show_albums_pages = response.xpath('//div[@class="u-page"]/a[@class="zpgi"]/@href').extract()
        last_item = in_show_albums_pages[-1:]   # 最后一页
        if last_item:
            temp = last_item[0].split('&')
            if len(temp) == 3:
                album_id = temp[0][17:]
                limit = temp[1][6:]
                total = temp[2][7:]
                for offset in range(int(limit), int(total)+1, int(limit)):
                    album_url = self.base_url + '/artist/album?id=%s&limit=%s&offset=%s' % (album_id, limit, offset)
                    album_url_list.append(album_url)
        # print(album_url_list)
        for album_url in album_url_list:
            yield scrapy.Request(album_url, callback=self.parse_artist)

    def parse_artist(self, response):
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        # albums = ['/album?id=74268947']
        # print('--------'+DEFAULT_REQUEST_HEADERS['User-Agent'])
        for album in albums:
            album_id = album[10:]
            album_url = self.base_url + album
            # print(album_url)
            yield scrapy.Request(album_url, meta={'aid': album_id}, callback=self.parse_album)

    def parse_album(self, response):
        album_id = response.meta['aid']
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        # musics = ['/song?id=1323302905']
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music
            # print(music_url)
            yield scrapy.Request(music_url, meta={'mid': music_id, 'aid': album_id}, callback=self.parse_music)

    def parse_music(self, response):
        album_id = response.meta['aid']
        music_id = response.meta['mid']
        music_name = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        artist_name = response.xpath('//div[@class="cnt"]/p[1]/span/@title').extract_first()
        album_name = response.xpath('//div[@class="cnt"]/p[2]/a/text()').extract_first()
        comment_url = self.base_url + '/weapi/v1/resource/comments/R_SO_4_' + str(music_id) + '?csrf_token='

        data = {
            'params': '/MXYWKSmiJzW37IBmps4IAKiX0voA7sh2IOMSKg5ERFlyNP3uewADoUMbfrW4ZT3hsRfcMl6uP1JOKalQKcw0oA+jOhT' +
                      'hetW8VlazrEuKJxZqtmgh/EHhj/qCSP39OL26D6lk0mPOBRnO7yhDYULx/7N03YjNsnX/hW47TWzoGZHD/oMs90criGr' +
                      'aEVCa4zO',
            'encSecKey': '0fcb505142abdba2ff75456772bb1d78a68c74333e5b85a11e1ca1f79ccd51c226eb00ed348ea59fa8c2ace5f' +
                         '38c791104dae2d620f9ceb181f556b4841c75795f3204eceb5a31c2490d11aa2a85f316832fb11414706d27ca' +
                         'e2c18215c702652baf5404858a4e0807216f2860668669fdd449dec0327d378242b0bf819d3a4a'
        }
        DEFAULT_REQUEST_HEADERS['Referer'] = self.base_url + 'song?id=' + str(music_id)
        DEFAULT_REQUEST_HEADERS['Origin'] = 'https://music.163.com'
        DEFAULT_REQUEST_HEADERS['Accept'] = '*/*'

        yield scrapy.FormRequest(
            comment_url,
            meta={'mid': music_id, 'aid': album_id, 'music': music_name, 'artist': artist_name, 'album': album_name},
            callback=self.parse_comment,
            formdata=data
        )

    def parse_comment(self, response):
        music_id = response.meta['mid']
        album_id = response.meta['aid']
        music_name = response.meta['music']
        artist_name = response.meta['artist']
        result = json.loads(response.text)
        comments = []

        # print(result)
        self.logger.info('%s[%s]' % (artist_name, music_name))
        if 'hotComments' in result.keys():
            for comment in result.get('hotComments'):
                hotcomment = comment['content']
                hotcomment_author = comment['user']['nickname']
                hotcomment_avatar = comment['user']['avatarUrl']
                hotcomment_like = comment['likedCount']
                data = {
                    'nickname': hotcomment_author,
                    'avatar': hotcomment_avatar,
                    'like': hotcomment_like,
                    'comment': hotcomment
                }
                comments.append(data)
            # print(comments)
            item = HotcommentsItem()
            for field in item.fields:
                try:
                    item[field] = eval(field)
                except NameError:
                    print('Field is not defined', field)
            yield item

    def parse(self, response):
        pass
