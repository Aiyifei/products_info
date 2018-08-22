# -*- coding: utf-8 -*-
import scrapy
from ..items import parse_jd, parse_tianmao
from scrapy_redis.spiders import RedisSpider
import re
from threading import Timer

reg_page_num = re.compile(r'>    共(.*?)页，到第<', re.S)


# class JdSpider(scrapy.Spider):
class JdSpider(RedisSpider):
    name = 'jd'

    # start_urls = ['https://search.jd.com/Search?keyword=iphone&page={}'.format(i) for i in range(0, 202, 2)]
    # start_urls = ['http://httpbin.org/ip']        # 测试代理ip是否生效

    def parse(self, response):

        # 进行天猫页面数据的分页，先拿出总共有多少页
        tianmao_first_url = 'https://list.tmall.com/search_product.htm?q=iphone'

        yield scrapy.Request(tianmao_first_url, callback=self.parse_tianmao, dont_filter=True)

        # 页数固定,没有进一步处理。
        for page_url in ['https://search.jd.com/Search?keyword=iphone&page={}'.format(i) for i in range(0, 20, 2)]:
            print(page_url)
            yield scrapy.Request(page_url, callback=self.parse_list, dont_filter=True)

    # 获取天猫的页数，处理分页。
    def parse_tianmao(self, response):
        print(response.url)

        try:
            page_num = reg_page_num.findall(response.text)[0]
            print('page_num', page_num)
            for page_url in [
                'https://list.tmall.com/search_product.htm?type=pc&q=iphone&totalPage=' + page_num + '&jumpto={}'.format(
                        i) for i in range(1, int(page_num))]:
                print('page_url', page_url)
                yield scrapy.Request(page_url, callback=self.parse_list, dont_filter=True)
        except Exception as e:
            print(e)

    def parse_list(self, response):

        # 京东页面的解析
        if "search.jd.com" in response.url:
            print('search.jd.com =>', len(response.css('.gl-warp.clearfix .gl-item')))
            product_list = response.css('.gl-warp.clearfix .gl-item')

            if product_list:
                for product in product_list:
                    jd_item = parse_jd(product)

                    # print(jd_item)
                    yield jd_item

        # 天猫页面的解析
        elif "list.tmall.com" in response.url:
            product_list = response.css(".product")
            print(len(product_list))
            for product in product_list:
                print(product)
                tianmao_item = parse_tianmao(product)

                yield tianmao_item
