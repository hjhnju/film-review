#!/bin/env python
#coding:utf8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

# Standard Python library imports
 
# 3rd party modules
import pymongo

from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

from items import MovieItem,RateItem
 
 
class MongoDBPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        connection = pymongo.Connection(self.server, self.port)
        self.db = connection[settings['MONGODB_DB']]
        #collections
        self.base = self.db[settings['MONGODB_COL_BASE']]
        self.rate = self.db[settings['MONGODB_COL_RATE']]
        self.base.ensure_index('mid',uniqe=True)
        self.base.ensure_index('year')
        self.rate.ensure_index('mid',uniqe=True)
        self.rate.ensure_index('rate_douban')
        self.rate.ensure_index('vote_douban')
 
    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if field in ('title'):
                continue
            if not data:
                err_msg += 'Missing %s of field from %s\n' % (field, item['mid'])
        if err_msg:
            #raise DropItem(err_msg)
            log.msg(err_msg, level=log.WARNING)
    
        values = {}
        for field, data in item.items():
            if data:
                values[field] = data

        if isinstance(item, MovieItem):
            log.msg('A MovieItem updated: %s' % item['mid'])
            self.base.update({'mid':item['mid']},{'$set':dict(values)}, upsert=True)
        elif isinstance(item, RateItem):
            log.msg('A RateItem updated: %s' % item['mid'])
            self.rate.update({'mid':item['mid']},{'$set':dict(values)}, upsert=True)
        log.msg('Item written to MongoDB database', level=log.INFO, spider=spider)
        return item

