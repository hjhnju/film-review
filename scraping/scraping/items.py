#coding:utf8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapingItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class MovieItem(Item):
    mid = Field()
    title = Field()
    #上映时间
    year = Field()
    date = Field()
    #导演，演员
    directors = Field()
    stars = Field()
    #类型
    tags = Field()
    types = Field()
    #国家或地区
    district = Field()
    #别名
    alias = Field()
    #宣传海报
    img = Field()
    #剧情
    story = Field()
    #时长
    runtime = Field()

class RateItem(Item):
    mid = Field()
    #评分
    rate_douban = Field()
    vote_douban = Field()
    url_douban = Field()

    #Item的基类已经实现__repr__方法
    #def __str__(self):

if __name__=='__main__':
     item = MovieItem()
     print item
