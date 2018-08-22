# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.item import Item
import pymongo


class ProductsInfoPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    DB_URI = 'mongodb://localhost:27017'
    # DB_NAME = 'crawler'    # 生产库
    DB_NAME = 'test'        # 测试库

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]
        # self.db.authenticate(name='zytong', password='crawler2018')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        collection = self.db['products_info']
        if isinstance(item, Item):
            post = dict(item)
        else:
            post = item
        collection.update({'p_id': post['p_id']}, post, True)

        return item
