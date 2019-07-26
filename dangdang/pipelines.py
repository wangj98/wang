# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import codecs
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

from scrapy.pipelines.images import ImagesPipeline
import os
from dangdang.settings import IMAGES_STORE as images_store
from dangdang.items import DangdangItem
from scrapy.utils.project import get_project_settings
import re
import random
from scrapy.exceptions import DropItem


class DangdangPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)


    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item


    def _conditional_insert(self, tx, item ):
        sql = """insert into happs(aid,shop_name, item_name, item_price, item_from, image_list) values(%s,%s, %s,%s, %s, %s)"""
        params = (item['aid'],item['shop_name'], item['item_name'], item['item_price'], item['item_from'], item['image_list'])

        tx.execute(sql, params)


class DangdangImagePipeline(ImagesPipeline):

    img_store = get_project_settings().get('IMAGES_STORE')
    tt=dict()

    def get_media_requests(self, item, info):
        self.tt=item
        print(1)
        for image_urll in item['image_url']:
            yield scrapy.Request(url=image_urll, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        apath = "./" + str(item['atype'])
        img_name = (item['item_name']).replace('/', '_').replace('|', '')
        img_name = img_name+'_'+str(random.randint(0, 1000))
        path = apath+'/'+img_name+'.jpg'
        return path

    def item_completed(self, results, item, info):
    #     print('success !!!! ')
        img_path = [x['path'] for ok, x in results if ok]
        if not img_path:
            raise DropItem('Item contains no images')
        item['img_paths'] = img_path
        return item