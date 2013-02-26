#!/bin/env python
#coding:utf-8
from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from pprint import pprint
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scraping.items import MovieItem
from scraping.items import RateItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

class DoubanSpider(BaseSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = [
        'http://movie.douban.com/tag/?view=type'
        #'http://movie.douban.com/subject/3148068/'
        #'http://movie.douban.com/subject/1767042/'
        #'http://movie.douban.com/tag/%E8%A5%BF%E7%8F%AD%E7%89%99'
    ]

    rules = (
        # Extract links matching '' and parse them with the spider's method parse function
        Rule(SgmlLinkExtractor(allow=('tag/[0-9]+',))),
        Rule(SgmlLinkExtractor(allow=('subject/[0-9]+',)), callback='parse_movie'),
    ) 

    #override
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,callback=self.parse_tag,dont_filter=True)

    def parse_tag(self, response):
        self.log('(parse_tag)A response from %s just arrived!' % response.url)
        tag_url = 'http://movie.douban.com/tag/'
        hxs = HtmlXPathSelector(response)
        taghrefs = hxs.select("//div[@id='wrapper']/div[@id='content']//div[@class='article']//table[@class='tagCol']//a[@href]")
        tagurls = [tag_url + tref.select('@href').extract()[0] for tref in taghrefs]
        for url in tagurls:
            page_url = "%s?start=%d&type=T" %(url,0)
            log.msg("Requesting %s" % page_url)
            yield Request(page_url,callback=self.parse_list,dont_filter=True)

    def parse_list(self, response):
        self.log('(parse_list)A response from %s just arrived!' % response.url)
        hxs = HtmlXPathSelector(response)
        tbs = hxs.select("//div[@id='wrapper']/div[@id='content']//div[@class='article']/div[@id='subject_list']/table")
        for tb in tbs:
            img_alt = subject_url = rate = None
            for t in tb.select(".//img/@alt").extract():
                img_alt = t
            for u in tb.select(".//a/@href").extract():
                subject_url = u
            for r in tb.select(".//div[@class='star clearfix']/span[@class='rating_nums']/text()").extract():
                rate = r
            item = MovieItem()
            item['mid'] = subject_url.split('/')[-2]
            #parse_subject无法获取title
            item['title'] = img_alt
            yield item
            yield Request(subject_url,callback=self.parse_subject,dont_filter=True)

        if len(tbs)> 0:
            m = re.match('([^\?]*)(\?start=([0-9]+).*)?', response.url)
            base = m.group(1)
            start = 0
            if m.group(3) is not None:
                start = int(m.group(3))
            start = start + 20
            next_list_url = "%s?start=%d&type=T" % (base, start)
            yield Request(next_list_url,callback=self.parse_list,dont_filter=True)

    def parse_subject(self, response):
        self.log('(parse_subject)A response from %s just arrived!' % response.url, level=log.INFO)
        hxs = HtmlXPathSelector(response)
        article = hxs.select("//div[@id='wrapper']/div[@id='content']//div[@class='article']")
        img = article.select(".//div[@id='mainpic']//img[@src]/@src").extract()
        info = article.select(".//div[@id='info']")
        item = MovieItem()
        item['mid'] = response.url.split('/')[-2]
        #item['title'] = None
        #for t in hxs.select("//div[@id='wrapper']//span[@property='v:itemreviewed']/text()").extract():
        #    item['title'] = t
        for im in img:
            item['img'] = im
        item['year'] = item['date'] = item['runtime'] = None
        #返回为列表，仅取一项
        for y in map(lambda x:x.strip(u'()（）'), hxs.select("//div[@id='wrapper']//span[@class='year']/text()").extract()):
            item['year'] = y
        item['directors'] = info.select(".//a[@rel='v:directedBy']/text()").extract()
        item['stars'] = info.select(".//a[@rel='v:starring']/text()").extract()
        item['types'] = info.select(".//span[@property='v:genre']/text()").extract()
        for d in info.select(".//span[@property='v:initialReleaseDate']/@content").extract():
            item['date'] = d
        for t in info.select(".//span[@property='v:runtime']/@content").extract():
            item['runtime'] = int(t)
        item['story'] = "\n".join(article.select(".//div[@class='related_info']//span[@class='all hidden']/text()").extract())
        if len(item['story']) == 0:
            item['story'] = "\n".join(article.select(".//div[@class='related_info']//span[@property='v:summary']/text()").extract())

        item['tags'] = article.select(".//div[@class='related_info']//div[@id='db-tags-section']//a[@href]/text()").extract()
        yield item

        #RateItem
        ritem = RateItem()
        ritem['mid'] = item['mid']
        ritem['rate_douban'] = ritem['vote_douban'] = None
        for r in article.select("//strong[@property='v:average']/text()").extract():
            ritem['rate_douban'] = float(r)
        votes = article.select(".//span[@property='v:votes']/text()").extract()
        for v in votes:
            ritem['vote_douban'] = int(v)
        ritem['url_douban'] = response.url
        yield ritem
        pass

