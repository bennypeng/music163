# -*- coding:utf-8 -*-
import pymongo
import settings
from commons.helper import Helper

client = pymongo.MongoClient(settings.MONGO_CONFIG['music']['host'])
db = client[settings.MONGO_CONFIG['music']['db']]
print('使用方式：https://music.163.com/playlist?id=歌单ID')
print('-'*92)
print('|%-20s\t|%-50s\t|%-6s|' % ('歌单ID', '歌单名', '总播放量'))
print('-'*92)
for i in db['playlists'].find().sort([("play_count", -1)]).limit(100):
    number = Helper.chinese(i['name'])
    print('|{0:<20}\t|{1:{wd}}\t|{2:<10}|'.format(i['id'], i['name'], i['play_count'], wd=50-number))
print('-'*92)



