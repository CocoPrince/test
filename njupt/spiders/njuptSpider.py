# -*- coding: utf-8 -*-
import scrapy
from njupt.items import NjuptItem
import logging


class njuptSpider(scrapy.Spider):
    name = "njupt"
    #爬虫名称，在后面启动爬虫的命令当中会用到
    allowed_domains = ["njupt.edu.cn"]
    #允许爬虫爬取的域名范围（如果连接到范围以外的就不爬取）
    start_urls = [
        "http://news.njupt.edu.cn/s/222/t/1100/p/1/c/6866/i/1/list.htm",
    ]#爬虫首次启动之后访问的第一个Url，其结果会被自动返回给parse函数。

    def parse(self, response):
        #scrapy框架中定义的置函数，用来处理请求start_urls之后返回的response，由我们实现
        news_page_num = 14
        page_num = 386
        if response.status == 200:
            for i in range(2, page_num + 1):
                for j in range(1, news_page_num + 1):
                    item = NjuptItem()
                    item['news_url'], item['news_title'], item['news_date'] = response.xpath(
                        "//div[@id='newslist']/table[1]/tr[" + str(j) + "]//a/font/text()"
                                                                        "|//div[@id='newslist']/table[1]/tr[" + str(
                            j) + "]//td[@class='postTime']/text()"
                                 "|//div[@id='newslist']/table[1]/tr[" + str(j) + "]//a/@href").extract()
                    #通过item = NjuptItem()来使用我们之前定义的item，用来存储新闻的url、标题、日期。
                    # （这里面有一个小技巧就是通过|来接连xpath可以一次返回多个想要抓取的xpath）

                    yield item
                    #通过yield item来将存储下来的item交由后续的pipelines处理

                next_page_url = "http://news.njupt.edu.cn/s/222/t/1100/p/1/c/6866/i/" + str(i) + "/list.htm"
                #通过生成next_page_url来通过scrapy.Request抓取下一页的新闻信息
                yield scrapy.Request(next_page_url, callback=self.parse_news)
                #scrapy.Request的两个参数，一个是请求的URL另外一个是回调函数用于处理这个request的response，
                # 这里我们的回调函数是parse_news

    def parse_news(self, response):
        news_page_num = 14
        if response.status == 200:
            for j in range(1, news_page_num + 1):
                item = NjuptItem()
                item['news_url'], item['news_title'], item['news_date'] = response.xpath(
                    "//div[@id='newslist']/table[1]/tr[" + str(j) + "]//a/font/text()"
                                                                    "|//div[@id='newslist']/table[1]/tr[" + str(
                        j) + "]//td[@class='postTime']/text()"
                             "|//div[@id='newslist']/table[1]/tr[" + str(j) + "]//a/@href").extract()
                yield item