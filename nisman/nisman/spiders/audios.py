# -*- coding: utf-8 -*-
import scrapy, re, os
from scrapy.http import Request

from nisman.items import AudioItem

class AudiosSpider(scrapy.Spider):
    name = "audios"
    allowed_domains = ["infobae.com"]
    start_urls = (
        'http://www.infobae.com/archivos-de-nisman/',
    )

    def parse(self, response):
        res = []
        titulos = response.xpath('//a[@class="entry-title url"]')

        for t in titulos:
            title_start = t.xpath('text()').extract()[0][:8]

            if title_start == 'Escuchas':
                req = Request(url=t.xpath('@href').extract()[0], callback=self.parse_escucha)
                res.append(req)

        view_more = response.xpath('//a[@class="vermasnoticias"]/@href').extract()
        next = view_more + response.xpath('//h4[@class="b-next"]/a/@href').extract()

        if len(next) > 0:
            req = Request(url=next[0], callback=self.parse)
            res.append(req)


        return res

    def parse_escucha(self, response):
        data = response.xpath('//div[@class="single-content entry-content narrowcontent fleft"]/div[@class="clearfix"]/div/text()').extract()

        item = AudioItem()
        item['url'] = response.xpath('//audio/@src').extract()[0]

        return item
