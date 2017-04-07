# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class NjuptPipeline(object):
    def __init__(self):
        self.file = open('njupt.txt', mode='w')
    def process_item(self, item, spider):
        self.file.write(item['news_title'])
        self.file.write("\n")
        self.file.write(item['news_date'])
        self.file.write("\n")
        self.file.write(item['news_url'])
        self.file.write("\n")
        return item

    from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
class NjuptPipeline(object):
    #数据库参数
    def __init__(self):
        dbargs = dict(
             host = '127.0.0.1',
             db = 'lirui',          #数据库
             user = 'zhanglirui',    #用户名
             passwd = 'zlr1998',    #密码
             cursorclass = pymysql.cursors.DictCursor,
             charset = 'utf8',
            # use_unicode = True
            )
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbargs)

    '''
    The default pipeline invoke function
    '''
    def process_item(self, item,spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item
    #插入的表，此表需要事先建好
    def insert_into_table(self,conn,item):
            conn.execute('insert into my(title, date,link) values(%s,%s,%s)', (
                item['title'][0],
                item['date'][0],
                item['link'][0])
                )
