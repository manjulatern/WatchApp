# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import FormRequest
import re, json, pprint
import requests
import math
import logging,traceback
from scrapy.http import HtmlResponse
from datetime import datetime


from watchscrapy.items import WatchItem


class BonhamsSpider(scrapy.Spider):
    name = "bonhamsSpider"
    allowed_domains = ["www.bonhams.com"]
    
    def __init__(self, url='',job='', *args, **kwargs):
        super(BonhamsSpider, self).__init__(*args, **kwargs)
        self.start_urls = url.split(",")
        self.job = job

    def parse(self,response):
        item = WatchItem()
        logging.warn("BonhamsSpider; msg=Spider started;url= %s",response.url)
        try:
            pre_item = {}
            #1 HouseName
            house_name =  3
            item["house_name"] = house_name

            #2 Name
            name = response.xpath('//div[@class="auction-slider"]/div/h1/div/text()').extract()[0]
            item["name"] = name

            #3 Date
            date_info = response.xpath('//div[@class="auction-slider__date"]/span/text()').extract()
            if date_info:
                date = date_info[0].strip().split(",")[0]
            else:
                date_info = response.xpath('//div[@class="auction-slider__date"]/text()').extract()
                date = date_info[0].strip().split("-")[-1].strip()
            item["date"] = datetime.strptime(date.strip(),'%d %b %Y').strftime('%b %d,%Y')
            
            #4 Location
            location = response.xpath('//div[@class="auction-slider"]/div/div[@class="auction-slider__divisions"]/div/a/text()').extract()[0]
            item["location"] = location
            

            auc_id = response.url.rsplit("/")[-2]
            item["auction_url"] = response.url

            base_url = "https://www.bonhams.com/api/v1/lots/"+auc_id
            resp = requests.get(base_url).text
            jresp = json.loads(resp)
            total_lot = jresp["total_lots"]
            
            url_list = []
            page_numbers = int(math.ceil(total_lot/10))
            for i in range(page_numbers):
                final_url = base_url + "?page=" + str(i+1)
                resp = requests.get(final_url).text
                jresp = json.loads(resp)
                lots = jresp["lots"]
                for lot in lots:

                    #5 Lot
                    lot_number = lot['iSaleLotNo']
                    item["lot"] = lot_number

                    #6 Images
                    images = lot['image']['url']
                    item["images"] = images

                    #7 title
                    title = lot['image']['alt']
                    item["title"] = title

                    #9 Lot Currency
                    lot_currency = lot['main_currency']
                    item["lot_currency"] = lot_currency.strip()

                    #10 Est min Price
                    #11 Est max Price
                    
                    try:
                        est_min_price = lot['high_low_estimates']['prices'][0]['low'].replace(",","")
                        est_max_price = lot['high_low_estimates']['prices'][0]['high'].replace(",","")
                    except KeyError:
                        est_min_price = 0
                        est_max_price = 0
                    
                    item["est_min_price"] = est_min_price
                    item["est_max_price"] = est_max_price

                    #12 sold
                    #13 sold_price
                    #14 sold_price_dollar
                    sold = sold_price = sold_price_dollar = 0
                    if lot['sLotStatus'] == "SOLD":
                        sold = 1
                        sold_price = lot['hammer_prices']['prices'][0]['value'].replace(",","")
                        sold_price_dollar = sold_price
                    
                    item["sold"] = sold
                    item["sold_price"] = sold_price
                    item["sold_price_dollar"] = sold_price_dollar

                    #15 url
                    url = "https://"+self.allowed_domains[0] + lot['url']
                    logging.debug("BonhamsSpider; msg=New URL is ;url= %s;",url)
                    item["url"] = url

                    resp = requests.get(url)
                    htmlr = HtmlResponse(url="test",body=resp.text,encoding='utf-8')
                    
                    #8 Description
                    description = ""
                    desc_name = htmlr.xpath('//div[@class="lot-details__description__name"]/text()').extract()[0].strip()
                    desc_content_info = htmlr.xpath('//div[@class="lot-details__description__content"]/text()').extract()
                    desc_content = ""
                    for desc in desc_content_info:
                        desc_content =  desc_content + desc
                    
                    footnote_info = htmlr.xpath('//h3[@class="lot-details__description__footnotes"]/text()').extract()
                    footnote = ""
                    if footnote_info:
                        footnote_title = "<strong>" + footnote_info[0] + "</strong>"

                        notes_info = htmlr.xpath('//div[@class="lot-details__description__content"]/text()').extract()
                        footnote_desc = ""
                        for note in notes_info:
                            footnote_desc = footnote_desc + note
                        footnote = footnote_title + "<br/>" + footnote_desc

                    item["description"] = desc_name + "<br/>" + desc_content + "<br/>" + footnote
                    item["status"] = "Success"
                    item["auction_url"] = response.url
                    item['total_lots'] = total_lot
                    item["job"] = self.job
                    yield item
        except Exception as e:
            item['url'] = response.url
            item['status'] = "Failed"
            logging.error("BonhamsSpider; msg=Crawling Failed > %s ;url= %s",str(e),response.url)
            logging.debug("BonhamsSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
            yield item
        




