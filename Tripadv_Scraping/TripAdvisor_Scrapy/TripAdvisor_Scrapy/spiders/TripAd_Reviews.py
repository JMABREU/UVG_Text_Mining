# -*- coding: utf-8 -*-
import scrapy
from scrapy.responsetypes import Response
from scrapy import Request
from TripAdvisor_Scrapy.items import TripadvScrapyItem

class TripadReviewsSpider(scrapy.Spider):
    name = 'TripAd_Reviews'
    allowed_domains = ['www.tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g295366-Antigua_Sacatepequez_Department-Hotels.html']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'file:C://Users//jabreu//UVG//Data Scients//TM_DM//wikipedia_scraping//wiki_scrapy//featured_article-%(time)s.json'
    }

    def parse(self, response):
        urls = []
        cant = 1

        for href in response.css('div.meta_listing').xpath('@data-url').extract():
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback=self.parse_page)

                if cant == 10:
                    break
                cant = cant+1

        next_page = response.css("a.nav.next").xpath('@href').get()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.parse)

                if cant == 10:
                    break
                cant = cant+1


    def parse_page(self, response: Response):

        sub_div = response.css('div.location-review-review-list-parts-SingleReview__mainCol--1hApa')

        for review in sub_div:
            item = TripadvScrapyItem()

            contents = review.css(
                'q.location-review-review-list-parts-ExpandableReview__reviewText--gOmRC span::text').get()
            content = contents.encode("utf-8")

            ratings = review.css('span.ui_bubble_rating').xpath('@*').get()
            rating = int(ratings.split(' ')[-1].replace('bubble_', ''))

            item['rating'] = rating
            item['review'] = content
            yield item

        next_page = response.css("a.nav.next").xpath('@href').get()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.parse_page)
