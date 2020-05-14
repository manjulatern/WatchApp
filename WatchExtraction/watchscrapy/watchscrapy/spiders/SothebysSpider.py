# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import FormRequest
import re, json, pprint
from datetime import datetime
import time

## additions
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import logging,traceback

from bs4 import BeautifulSoup
from watchscrapy.items import WatchItem
from watchapp.models import Setup


class SothebysSpider(scrapy.Spider):
    name = "sothebysSpider"
    allowed_domains = ["www.sothebys.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def __init__(self, url='',job='', *args, **kwargs):
        super(SothebysSpider, self).__init__(*args, **kwargs)
        self.start_urls = url.split(",")
        self.job = job

    def sel_configuration(self):
        # Selenium Configuration
        setup = Setup.objects.first()
        SELENIUM_CHROMEDRIVER_PATH = setup.chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36")
        browser = webdriver.Chrome(executable_path=SELENIUM_CHROMEDRIVER_PATH, chrome_options=options)
        return browser

    def start_requests(self):
        for source_url in self.start_urls:
            try:
                browser = self.sel_configuration()
                browser.set_window_size(1440, 900)
                logging.warn("SothebysSpider; msg=Spider started;url= %s",source_url)
                if '/auctions/' in source_url:
                    sothebys_version = 1
                else:
                    sothebys_version = 2

                lots_urls = []

                if sothebys_version == 2:
                    is_loaded = False
                    self.scrollAndLoad(browser)
                    logging.debug("SothebysSpider; msg=Scrolling for the first time;url= %s",source_url)
                    while True:
                        browser.get(source_url)
                        self.scrollAndLoad(browser)
                        logging.debug("SothebysSpider; msg=Scrolling Again;url= %s",source_url)
                        total_lots_info = browser.find_element_by_css_selector(".css-kajn87-label-book")
                        if total_lots_info:
                            total_lots = total_lots_info.text.split(" ")[0]
                            logging.debug("SothebysSpider; msg=Actual Total Lots: %s;url= %s",total_lots,source_url)
                            links_count = self.get_links_count(browser)
                            logging.debug("SothebysSpider; msg= Fetching Lots: %s;url= %s",links_count,source_url)
                            if int(total_lots) == links_count:
                                logging.debug("SothebysSpider; msg=Lots Matched hence processing;url= %s",source_url)
                                is_loaded = True
                                break
                    logging.debug("SothebysSpider; msg=Page Loaded completely;url= %s",source_url)
                    if is_loaded:
                        links = browser.find_elements_by_css_selector("a.css-1um49bp")

                        page_source = browser.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')

                        #date_location_info_pre = soup.find('span', {'class': 'css-183l6yv-label-book'})

                        #if not date_location_info_pre:
                            #date_location_info_pre = soup.find('p', {'class': 'css-1wnmcn0-p-book'})
                        #print(date_location_info_pre)
                        #date_location_info = date_location_info_pre.text.split("•")
                        #date = date_location_info[0].strip()
                        #location = date_location_info[-1].strip()
                        script = soup.find('script',{'type': 'application/ld+json'}).string
                        pre_data = json.loads(script)
                        date = pre_data[0]['endDate'].split("T")[0]
                        location = pre_data[0]['location']['name']
                        for link in links:
                            link_url = link.get_attribute('href')
                            if link_url is not None:
                                lots_urls.append(link_url)
                        total_lots = len(lots_urls)
                        logging.warn("SothebysSpider; msg=Total Lots: %s;url= %s",len(lots_urls),source_url)
                        i = 0
                        for url in lots_urls:
                            i = i + 1
                            logging.debug("SothebysSpider; msg=Crawling triggerred - %s;url= %s",i,url)
                            yield scrapy.Request("https://www.google.com",dont_filter=True,callback=self.parseBSv2, meta={'url':url,'browser':browser,'source_url':source_url,'date':date,'location':location,'lots':total_lots})


                else:
                    browser.get(source_url)
                    self.scrollAndLoadV1(browser)
                    while True:
                        total_lots_info = browser.find_element_by_css_selector(".page-info")
                        if total_lots_info:
                            total_lots = total_lots_info.text.split(" ")[-1]
                            logging.debug("SothebysSpider; msg=Actual Total Lots: %s;url= %s",total_lots,source_url)
                            break
                    
                    page_source = browser.page_source
                    
                    links = browser.find_elements_by_css_selector(".image a")

                    logging.debug("SothebysSpider; msg=Fetching Total Lots: %s;url= %s",len(links),source_url)
                    
                    name = browser.find_element_by_css_selector(".eventdetail-headerleft h1").text
                    date = browser.find_element_by_css_selector(".dtstart").text
                    location = browser.find_element_by_css_selector(".location").text
                    for link in links:
                        link_url = link.get_attribute('href')
                        if link_url is not None:
                            lots_urls.append(link_url)
                    total_lots = len(lots_urls)
                    logging.warn("SothebysSpider; msg=Total Lots: %s;url= %s",len(lots_urls),source_url)
                    i = 0
                    for url in lots_urls:
                        i = i + 1
                        logging.debug("SothebysSpider; msg=Crawling started;url= %s",url)
                        #url = lots_urls[0]
                        yield scrapy.Request("https://www.google.com",dont_filter=True,callback=self.parseBS, meta={'url':url,'browser':browser,'source_url':source_url,'name':name,'date':date,'location':location,'lots':total_lots})
            except Exception as e:
                item = WatchItem()
                item['status'] = "Failed"
                logging.error("SothebysSpider; msg=Crawling Failed > %s;url=%s",str(e),source_url)
                logging.error("SothebysSpider; msg=Crawling Failed;url=%sError=%s",traceback.format_exc(),source_url)
                yield item

    def parseBS(self, response):
        url = response.meta.get('url')
        browser = response.meta.get('browser')
        source_url = response.meta.get('source_url')
        item = WatchItem()
        try:
            browser.get(url)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            #1 House Name
            item['house_name'] = 9

            #2 Auction Name
            item['name'] = response.meta.get('name')

            #3 Date
            item['date'] = datetime.strptime(response.meta.get('date'),'%d %B %Y').strftime('%b %d,%Y')

            #4 Location
            item['location'] =response .meta.get('location')

            #5 Lot
            lot_number_info = soup.find('div', {'class': 'lotdetail-lotnumber hidden-phone'}).text
            item['lot'] = re.findall(r'\d+',lot_number_info)[0]

            #6 Images
            images_links = ""
            images_info = soup.find_all('div', {'id': 'lotDetail-carousel'})
            if images_info:
                images = images_info[0].find_all('img',{'class':'copyright'})
                for image in images:
                    images_links = "https://" + self.allowed_domains[0] + image['src'] + "," + images_links
            else:
                images_links = "https://" + self.allowed_domains[0] + soup.find('div', {'id': 'main-image-container'}).find('img')["src"]
            
            
            item['images'] = images_links

            #7 Title
            item['title'] = soup.find('div', {'class': 'lotdetail-guarantee'}).text

            #8 Description
            subtitle_info = soup.find('div', {'class': 'lotdetail-subtitle'})
            subtitle = ""
            if subtitle_info:
                subtitle = subtitle_info.text
            desc = soup.find('div', {'class': 'lotdetail-description-text'}).text
            description = subtitle + "\n" + desc
            item['description'] = description

            #9 Lot Currency
            item['lot_currency'] = soup.find('a', {'class': 'dropdown-toggle btn btn-link'}).text

            #10 Est Min Price
            item['est_min_price'] = soup.find('span', {'class': 'range-from'}).text.replace(",","")

            #11 Est Max Price 
            item['est_max_price'] = soup.find('span', {'class': 'range-to'}).text.replace(",","")

            #12 Sold Price
            sold_info = soup.find('div', {'class': "price-sold"})
            sold = sold_price = 0
            if sold_info:
                sold_price = sold_info.text.split()[-2].replace(",","")
                sold = 1

            item['sold_price'] = sold_price
            item['sold'] = sold
            #13 Sold Price Dollar
            item['sold_price_dollar'] = 0

            #14  URL
            item['url'] = url
            item["status"] = "Success"
        except Exception as e:
            item['status'] = "Failed"
            logging.error("SothebysSpider; msg=Crawling Failed > %s;url= %s",str(e),url)
            logging.error("SothebysSpider; msg=Crawling Failed;url= %s;Error=%s",url,traceback.format_exc())
        item['total_lots'] = response.meta.get("lots")
        item["auction_url"] = source_url
        item["job"] = self.job
        return item

    def parseBSv2(self,response):
        url = response.meta.get('url')
        browser = response.meta.get('browser')
        source_url = response.meta.get('source_url')
        logging.warn("SothebysSpider; msg=Crawling going to start;url= %s",url)
        item = WatchItem()
        try:
            browser.get(url)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            #1 House Name
            item['house_name'] = 9

            #2 Auction Name
            item['name'] = soup.find('h5', {'class': 'css-nqjhlo'}).text

            #3 Date
            item['date'] = datetime.strptime(response.meta.get('date'),'%Y-%m-%d').strftime('%b %d,%Y')

            #4 Location
            item['location'] = response.meta.get('location')

            #5 Lot
            lot_number_info = soup.find('span', {'class': 'css-yxsueo'}).text
            item['lot'] = re.findall(r'\d+',lot_number_info)[0]

            #6 Images
            images = soup.find_all('img', {'class': 'css-3rldmv'})
            images_links = ""
            for image in images:
                images_links = image['src'] + "," + images_links
            
            item['images'] = images_links

            #7 Title
            item['title'] = soup.find('h1', {'class': 'css-1ikrrc9'}).text

            #8 Description
            description = soup.find('div', {'class': 'css-xs9w33'})
            if not description:
                description = soup.find('div', {'class': 'css-1ewow1l'})
            item['description'] = description.text

            price_text = soup.find('p', {'class': 'css-1g8ar3q'}).text
            if price_text is not None:
                price_text = price_text.replace('Estimate: ', '')
                lot_currency = price_text.strip()[-3:]
                est_min_price = price_text[:-3].split('-')[0].strip()
                est_max_price = price_text[:-3].split('-')[1].strip()
            else:
                lot_currency = None
                est_min_price = None
                est_max_price = None
            #9 Lot Currency
            item['lot_currency'] = lot_currency

            #10 Est Min Price
            item['est_min_price'] = est_min_price.replace(",","")

            #11 Est Max Price 
            item['est_max_price'] = est_max_price.replace(",","")

            #12 Sold Price
            sold_price_info = soup.find('span', {'class': "css-15o7tlo"})
            sold = sold_price = 0
            if sold_price_info:
                sold_price = sold_price_info.text.replace(",","")
                sold_currency = soup.find('span', {'class': "css-wfxyp0"}).text
                sold = 1
            item['sold_price'] = sold_price
            
            item['sold'] = sold
            #13 Sold Price Dollar
            item['sold_price_dollar'] = 0

            #14  URL
            item['url'] = url
            item["status"] = "Success"
            logging.debug("SothebysSpider; msg=Crawling Completed > %s;url= %s",item,url)
        except Exception as e:
            item['status'] = "Failed"
            logging.error("SothebysSpider; msg=Crawling Failed > %s;url= %s",str(e),url)
            logging.error("SothebysSpider; msg=Crawling Failed;url= %s;Error=%s",url,traceback.format_exc())
        item['total_lots'] = response.meta.get("lots")
        item["auction_url"] = source_url
        item["job"] = self.job
        return item

    def scrollAndLoad(self,browser):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load content
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scrollAndLoadV1(self,browser):
        pre_scroll_height = browser.execute_script('return document.body.scrollHeight;')
        run_time, max_run_time = 0, 1
        while True:
            iteration_start = time.time()
            # Scroll webpage, the 100 allows for a more 'aggressive' scroll
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight-1000);')

            post_scroll_height = browser.execute_script('return document.body.scrollHeight;')

            scrolled = post_scroll_height != pre_scroll_height
            timed_out = run_time >= max_run_time

            if scrolled:
                run_time = 0
                pre_scroll_height = post_scroll_height
            elif not scrolled and not timed_out:
                run_time += time.time() - iteration_start
            elif not scrolled and timed_out:
                break
    
    def get_links_count(self,browser):
        is_loaded = False
        links_count = 0
        while True:
            try:
                elem_check = browser.find_element_by_css_selector('div.css-al9y2g')
                elem_check.click()
                time.sleep(5)
                self.scrollAndLoad(browser)
            except NoSuchElementException:
                is_loaded = True
                break
        if is_loaded:
            links = browser.find_elements_by_css_selector("a.css-1um49bp")
            links_count = len(links)
        return links_count
        
