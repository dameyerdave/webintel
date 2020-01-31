# -*- coding: utf-8 -*-
import scrapy
import hashlib


class BlickSpider(scrapy.Spider):
    name = 'blick'
    allowed_domains = ['blick.ch']
    start_urls = [
        'https://www.blick.ch/news/rss.xml',
        'https://www.blick.ch/news/schweiz/rss.xml',
        'https://www.blick.ch/news/ausland/rss.xml',
        'https://www.blick.ch/news/wirtschaft/rss.xml',
        'https://www.blick.ch/digital/rss.xml'
    ]

    def parse(self, response):
        urls = response.css('link::text').getall()[1:]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('title::text').get()
        id = hashlib.sha256((response.url + title).encode('utf-8')).hexdigest()
        yield { 
            'id': id,
            'reference': response.url,
            'title': title,
            'summary': response.css('div.article-lead::text').get(),
            'content': ' '.join(response.css('div.article-body p::text').getall()),
            'published': response.css('meta[property="article:published_time"]::attr(content)').get(),
            'modified': response.css('meta[property="article:modified_time"]::attr(content)').get()
        } 
