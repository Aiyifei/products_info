# coding=utf-8
from threading import Timer
import redis

ITEM_KEY = 'jd:start_urls'
client = redis.StrictRedis(host='localhost', port=6379)

# 定时往redis中插入启动数据,定时抓取更新
def timer_task():

    # 插入redis
    print('before_before', client.llen(ITEM_KEY))
    client.lpush(ITEM_KEY, 'https://search.jd.com/Search?keyword=iphone&page=0')
    print('after_push', client.llen(ITEM_KEY))

    Timer(10, timer_task, ()).start()

if __name__ == '__main__':

    # 给10秒钟的启动时间
    Timer(10, timer_task, ()).start()

    # 执行一次,爬虫抓取
    from scrapy.cmdline import execute
    execute("scrapy crawl jd".split(" "))
