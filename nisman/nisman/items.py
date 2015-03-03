# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EscuchaItem(scrapy.Item):
    # define the fields for your item here like:
    filename = scrapy.Field()
    origen = scrapy.Field()
    destino = scrapy.Field()
    inicio = scrapy.Field()
    fin = scrapy.Field()
    direccion = scrapy.Field()
    numero = scrapy.Field()
    localidad = scrapy.Field()
    provincia = scrapy.Field()
    pass
