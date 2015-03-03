# -*- coding: utf-8 -*-
import scrapy, re, os
from scrapy.http import Request

from nisman.items import EscuchaItem

class EscuchasSpider(scrapy.Spider):
    name = "escuchas"
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

        item = EscuchaItem()
        item['filename'] = os.path.basename(response.xpath('//audio/@src').extract()[0])

        for datum in data:
            stripped = datum.strip()
            search_origen = re.search('Origen: (.*)', stripped)
            search_destino = re.search('Destino: (.*)', stripped)
            search_inicio = re.search('Inicio: (.*)', stripped)
            search_fin = re.search('Fin: (.*)', stripped)
            search_calle = re.search('Calle: (.*)', stripped)
            search_numero = re.search('Número: (.*)', stripped)
            search_localidad = re.search('Localidad: (.*)', stripped)
            search_provincia = re.search('Provincia: (.*)', stripped)

            if search_origen:
                item['origen'] = search_origen.group(1)
            if search_destino:
                item['destino'] = search_destino.group(1)
            if search_inicio:
                item['inicio'] = search_inicio.group(1)
            if search_fin:
                item['fin'] = search_fin.group(1)
            if search_calle:
                item['calle'] = search_calle.group(1)
            if search_numero:
                item['numero'] = search_numero.group(1)
            if search_localidad:
                item['localidad'] = search_localidad.group(1)
            if search_provincia:
                item['provincia'] = search_provincia.group(1)

        return item
