# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging,traceback
from datetime import datetime

from watchscrapy.items import WatchItem


class BukowskisSpider(scrapy.Spider):
    name = "bukowskisSpider"
    allowed_domains = ["www.bukowskis.com"]
    
    def __init__(self, url='', job='', *args, **kwargs):
        super(BukowskisSpider, self).__init__(*args, **kwargs)
        self.start_urls = url.split(",")
        self.job = job

    def parse(self, response):

        # -1 because, there is a span called as next or previous
        pagination = response.xpath('//nav[@class="c-pagination"]')
        page_numbers = 1
        if pagination:
            page_numbers = len(pagination[0].xpath('span'))
        total_lots = response.xpath('//div[@class="c-lot-index__top-pagination-count"]/text()').extract()[0].split(" ")[0]

        logging.warn("BukowskisSpider; msg=Total Lots : %s ;url= %s",total_lots,response.url)
        auction_url = response.url
        for page in range(page_numbers):
            absolute_url = response.url+"/page/"+str(page+1)
            yield scrapy.Request(absolute_url,callback=self.parse_urls,meta={"auction_url":auction_url,"lots":total_lots})

    def parse_urls(self,response):
        logging.warn("BukowskisSpider; msg=Spider started;url= %s",response.url)
        try:
            all_lots = response.xpath('//div[@class="c-lot-index__lots"]/div/div')

            #1
            house_name = 4

            #2
            name = response.xpath('//div[@class="c-headline-block"]/h1/text()').extract()[0]

            #3
            date = response.xpath('//div[@class="c-search-filters__link c-search-filters__link--headline"]/text()').extract()[0].replace("Auction","").replace("\xa0"," ").strip()

            for lots in all_lots:
                url_segment = lots.xpath('a[1]/@href').extract()
                if url_segment:
                    final_url = "https://" + self.allowed_domains[0] + url_segment[0]
                    lot_number = lots.xpath('a[@class="c-lot-index-lot__title u-line-clamp"]/text()').extract()[0].split(".")[0]
                    items = {'name':name,'date':date,'lot_number':lot_number,'auction_url':response.meta.get("auction_url"),'lots':response.meta.get("lots")}
                    yield scrapy.Request(final_url,callback=self.parse_lot_url,meta=items)
        except Exception as e:
            item = WatchItem()
            item['url'] = response.url
            item['status'] = "Failed"
            logging.error("BukowskisSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("BukowskisSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
            yield item

    def parse_lot_url(self,response):

        item = WatchItem()
        try:
            #1 HouseName
            house_name = 4
            item["house_name"] = house_name

            #2 Name
            name = response.meta.get("name")
            item["name"] = name

            #3 Date
            date = response.meta.get("date")
            item["date"] = datetime.strptime(date.strip(),'%b %d, %Y').strftime('%b %d,%Y')

            #4 Location
            location_info = response.xpath('//div[@class="c-live-lot-show-navigation"]/a[1]/text()').extract()[0]
            location = location_info.split(name)[1].strip()
            item["location"] = location

            #5 Lot Number
            lot_number = response.meta.get("lot_number")
            item["lot"] = lot_number.replace("A","")

            #6 images
            images = response.xpath('//div[@class="c-live-lot-show-thumbnails"]/div/a/div/img/@src').extract()
            item["images"] = images

            #7 title
            title = response.xpath('//div[@class="c-live-lot-show-header__title"]/text()').extract()[0]
            item["title"] = title
        
            #8 Description
            description = response.xpath('//div[@class="c-live-lot-show-info__description"]').extract()[0]
            item["description"] = description

            #9 Lot Currency

            estimation_info = response.xpath('//div[@class="c-live-lot-show-info__estimate-ranges"]/p[1]/text()').extract()[0].replace("\xa0"," ")
            lot_currency = estimation_info.split(" ")[-1]
            item['lot_currency'] = lot_currency
            
            #10 Est min Price
            estimation = estimation_info.replace(estimation_info.split(" ")[-1],"").strip().split("-")
            est_min_price = estimation[0].strip().replace(" ","")
            item["est_min_price"] = est_min_price

            #11 Est max Price
            est_max_price = 0
            if len(estimation)>1:
                est_max_price = estimation[1].strip().replace(" ","")
            item["est_max_price"] = est_max_price
        
            #12 sold
            sold = 0
            sold_price = 0
            sold_info = response.xpath('//div[@class="c-live-lot-show-info__final-price-amount"]/text()')
            if sold_info:
                sold = 1
                sold_price = sold_info[0].extract().replace("SEK","").replace("\xa0","")
            
            item["sold"] = sold

            #13 sold_price
            item["sold_price"] = sold_price

            #14 sold_price_dollar
            item["sold_price_dollar"] = 0

            #15 url
            item["url"] = response.url
            item["status"] = "Success"
        except Exception as e:
            item['status'] = "Failed"
            logging.error("BukowskisSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("BukowskisSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
        item['total_lots'] = response.meta.get("lots")
        item["auction_url"] = response.meta.get("auction_url")
        item["job"] = self.job
        yield item

        
