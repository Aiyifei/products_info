# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
import pytz
tz = pytz.timezone('Asia/Shanghai')


reg_p_title = re.compile(r'</font>(.*?)</em>', re.S)
reg_p_title_em = re.compile(r'<em>(.*?)</em>', re.S)

keyword = 'iphone'
# headers = {
#     'referer': 'https://search.jd.com/Search?keyword=keyword'
# }


class ProductsInfoItem(scrapy.Item):
    p_id = scrapy.Field()
    p_detail_url = scrapy.Field()
    p_price = scrapy.Field()
    p_name = scrapy.Field()
    p_title = scrapy.Field()
    p_paipai_url = scrapy.Field()
    p_comments = scrapy.Field()
    p_type = scrapy.Field()
    update_time = scrapy.Field()


def parse_jd(product):
    jd_item = ProductsInfoItem()

    p_id = product.css('li::attr(data-sku)').extract_first()
    p_detail_url = 'https:' + product.css('.p-img a::attr(href)').extract_first()
    p_price = product.css('.p-price strong i::text').extract_first()
    p_name = product.css('.p-name.p-name-type-2 a em font::text').extract_first()
    p_title_1 = product.css('.p-name.p-name-type-2 a em').extract_first()
    print('p_title_1 =>', p_title_1)

    try:
        p_title = reg_p_title.findall(product.css('.p-name.p-name-type-2 a em').extract_first())[0]
    except Exception as e:
        p_title = reg_p_title_em.findall(product.css('.p-name.p-name-type-2 a em').extract_first())[0]

    if 'font' in p_title:
        print("pre=>", p_title)
        p_title = p_title.split("</font>")[-1].strip()
        print("after=>", p_title)

    p_paipai_url = 'https:' + product.css('.p-commit a::attr(href)').extract_first()
    p_comments = product.css('.p-commit strong a::text').extract_first() + "条评论"
    p_type = 'jd'  # 京东网站抓取的
    update_time = datetime.datetime.now(tz)

    # print(p_id)
    # print(p_detail_url)
    # print(p_price)
    # print(p_name)
    # print(p_title)
    # print(p_paipai_url)
    # print(p_comments)
    # print(p_type)

    jd_item['p_id'] = p_id
    jd_item['p_detail_url'] = p_detail_url
    jd_item['p_price'] = p_price
    jd_item['p_name'] = p_name
    jd_item['p_title'] = p_title
    jd_item['p_paipai_url'] = p_paipai_url
    jd_item['p_comments'] = p_comments
    jd_item['p_type'] = p_type
    jd_item['update_time'] = update_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    return jd_item


def parse_tianmao(product):
    tianmao_item = ProductsInfoItem()

    p_id = product.css('div::attr(data-id)').extract_first()
    p_detail_url = "https:" + product.css(".productImg-wrap a::attr(href)").extract_first()
    p_price = product.css(".productPrice em::attr(title)").extract_first()
    p_name = product.css(".productTitle .H::text").extract_first()
    p_title = product.css(".productTitle a::attr(title)").extract_first()
    p_paipai_url = None
    p_comments = None
    p_type = 'tianmao'
    update_time = datetime.datetime.now(tz)


    # print(p_id)
    # print(p_detail_url)
    # print(p_price)
    # print(p_name)
    # print(p_title)
    # print(p_paipai_url)
    # print(p_comments)
    # print(p_type)
    # print(update_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))

    tianmao_item['p_id'] = p_id
    tianmao_item['p_detail_url'] = p_detail_url
    tianmao_item['p_price'] = p_price
    tianmao_item['p_name'] = p_name
    tianmao_item['p_title'] = p_title
    tianmao_item['p_paipai_url'] = p_paipai_url
    tianmao_item['p_comments'] = p_comments
    tianmao_item['p_type'] = p_type
    tianmao_item['update_time'] = update_time

    return tianmao_item
