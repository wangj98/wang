# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import re
from dangdang.items import DangdangItem


class HappSpider(scrapy.Spider):
    name = 'happ'
    # allowed_domains = ['http://category.dangdang.com/cid4001001-srsort_sale_amt_desc.html']
    start_urls = ['http://category.dangdang.com/cid4001001.html']
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'http://category.dangdang.com/cid4001001.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    }
    # def start_requests(self):
    def parse(self, response):
        for atype in range(0, 3):
            item = DangdangItem()
            item['atype'] = atype
            item = DangdangItem(atype=atype)
            cid = "-cid400252"+str(atype)+".html"
            base_url = "http://category.dangdang.com/pg1" + cid
            yield scrapy.Request(url=base_url, callback=self.parse_url, headers=self.header, meta={'item': item})

    def parse_url(self, response):
        html = Selector(response)
        id = html.xpath("//ul[@class= 'bigimg cloth_shoplist']/li/@id").extract()
        next_link = html.xpath("//*[@id='12810']/div[3]/div[2]/div/ul/li/a[@title='下一页']/@href").extract_first()
        start_url = 'http://product.dangdang.com/'
        next_start_url = 'http://category.dangdang.com'
        item = response.meta['item']
        atype= item['atype']
        item = DangdangItem(atype=atype)

        for aid in id:
            item['aid'] = int(aid)
            item = DangdangItem(aid=aid, atype=atype)
            item_url = start_url + aid + '.html'
            yield scrapy.Request(url=item_url, callback=self.parse_item, headers=self.header, meta={'item': item})
        if next_link != '':
            next_url = next_start_url + next_link
            yield scrapy.Request(url=next_url, callback=self.parse_url,headers=self.header, meta={'item': item})




    def parse_item(self, response):
        item_html = Selector(response)
        item = DangdangItem()
        item = response.meta['item']

        shop_name = item_html.xpath("//*[@id='service-more']/div[2]/p[1]/span/span[2]/a/text()").extract_first()
        item['shop_name'] = shop_name

        item_name = ','.join(item_html.xpath("//*[@id='product_info']/div[1]/h1/text()").extract()).replace(' ', '').replace('\r\n', '')
        item['item_name'] = item_name

        item_price = ','.join(item_html.xpath("//*[@id='dd-price']/text()").extract()).replace(' ', '').replace(',', '')
        item['item_price'] = item_price

        item_from = ','.join(item_html.xpath("//*[@id='shop-geo-name']/text()").extract()).replace(' 至', '')
        item['item_from'] = item_from

        image_url = item_html.xpath("//*[@id='main-img-slider']/li/a/@data-imghref").extract()
        item['image_url'] = image_url

        image_list = ','.join(image_url)
        item['image_list'] = image_list

        yield item







