# -*- coding: utf-8 -*-
import scrapy
from wiki_scrapy.items import WikiScrapyItems, WikiPageItem


class GetwikipediapagesSpider(scrapy.Spider):
    name = 'GetWikipediaPages'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']
    #start_urls = ['http://en.wikipedia.org/']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'file:C://Users//jabreu//UVG//Data Scients//TM_DM//wikipedia_scraping//wiki_scrapy//featured_article-%(time)s.json'
    }

    def parse(self, response):
        host = self.allowed_domains[0]
        cant = 1

        for link in response.css(".featured_article_metadata > a"):
            title = link.attrib.get("title"),
            link = f"https://{host}{link.attrib.get('href')}"

            yield response.follow(link,callback=self.parse_detail, meta={'url' : link,'title':title})

            if cant == 300:
                break
            cant = cant+1

    def parse_detail(self,response):
        wsItems = WikiScrapyItems()
        wpItem  = WikiPageItem()

        wsItems["link"] = response.meta["url"]
        wpItem["title"] = response.meta["title"]
        wpItem["content"] = list()

        #for text in response.css(".sart-content > p::text").extract():
        for text in response.css(".mw-parser-output > p::text").extract():
            wpItem["content"].append(text)
            #print(text)
        
        wsItems["body"] = wpItem
        
        return wsItems
