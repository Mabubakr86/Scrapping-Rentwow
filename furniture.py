# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import RentwowItem


class FurnitureSpider(scrapy.Spider):
    name = 'furniture'

    def __init__(self, category):
    	self.start_urls =[category]
    # start_urls = ['https://rentwow.ca/Living_Room', 'https://rentwow.ca/Dining_Room',
    # 'https://rentwow.ca/Accessories', 'https://rentwow.ca/Bedroom', 'https://rentwow.ca/Patio','https://rentwow.ca/Home_Office']

    def parse(self, response):
        my_data = response.xpath("""//table[@class ='main_frame']/tr""")[3]
        furniture_urls =   my_data.xpath(""".//a[contains(@href,'rentwow.ca')]/@href""").extract()
        for url in furniture_urls:
        	yield Request(url=url, callback=self.parse_furniture, meta={'sub': url.split('/')[-1]})


    def parse_furniture(self, response):
    	sub = response.meta['sub']
        my_data = response.xpath("""//table[@class ='main_frame']/tr""")[2]
        furniture_urls =   my_data.xpath(""".//a[contains(@href,'rentwow.ca')]/@href""").extract()
        for url in furniture_urls:
        	yield Request(url=url, callback=self.parse_piece, meta={'sub': sub} )

    def parse_piece(self,response):
    	sub = response.meta['sub']
    	items = RentwowItem()
    	name = response.xpath("""//h1/text()""").extract_first()
    	table = response.xpath("""//table[@width="270" and @align="left"]""")[1]
    	color = table.xpath(""".//p/text()""").extract_first()
    	if color is None:
    		color = 'No color description'
    	else:
    		color = color
    	table = response.xpath("""//table[@width="270" and @align="left"]""")[2]
    	price = table.xpath(""".//p/text()""").extract_first().strip()
    	image_urls = response.xpath("""//img[@height='400' and @width='600']/@src""").extract()
    	items['sub'] = sub
    	items['name'] = name
    	items['price'] = price
    	items['color'] = color
    	items['image_urls'] = image_urls

    	yield items




