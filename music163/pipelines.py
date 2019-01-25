# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class Music163Pipeline(object):
    def process_item(self, item, spider):
        return item


class HotCommentsPipeline(object):

    def __init__(self, mongo_host, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        mongo_config = crawler.settings.get('MONGO_CONFIG')
        return cls(
            mongo_host=mongo_config['music']['host'],
            mongo_db=mongo_config['music']['db']
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({'music_id': item.get('music_id')}, {'$set': dict(item)}, True)
        return item


class ProxiesPipeline(object):

    def __init__(self, mongo_host, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        mongo_config = crawler.settings.get('MONGO_CONFIG')
        return cls(
            mongo_host=mongo_config['proxy']['host'],
            mongo_db=mongo_config['proxy']['db']
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({'proxy': item.get('proxy')}, {'$set': dict(item)}, True)
        return item
