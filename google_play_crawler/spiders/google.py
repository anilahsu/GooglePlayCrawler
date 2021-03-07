import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import GooglePlayCrawlerItem
from urllib.parse import urlparse
from datetime import datetime
import re

class GoogleSpider(CrawlSpider):
    name = 'google'
    allowed_domains = ['play.google.com']
    start_urls = ["https://play.google.com/store/apps/"]

    rules = (
        Rule(LinkExtractor(allow=("/store/apps/details", )), follow=True, callback='parse_detail'),
    )

    def parse_detail(self,response):
        items = []
        for title in response.xpath('/html'):
            item = GooglePlayCrawlerItem()
            item["Link"] = title.xpath('head/link[4]/@href').extract_first()
            item["Name"] = title.xpath('//h1[@class="AHFaub"]/span/text()').extract_first()
            item["LastUpdated"] = title.xpath('//div[contains(text(), "Updated")]/following-sibling::span[1]/div/span/text()').extract_first()
            item["Author"] = title.xpath('//div[contains(text(), "Offered By")]/following-sibling::span[1]/div/span/text()').extract_first()

            filesize = title.xpath('//div[contains(text(), "Size")]/following-sibling::span[1]/div/span/text()').extract_first()
            if re.search('[0-9]+\.?[0-9]*M', filesize):
                item["Filesize"] = float(filesize.replace(",", "").rstrip('M')) * 1024
            elif re.search('[0-9]+\.?[0-9]*k', filesize):
                item["Filesize"] = float(filesize.replace(",", "").rstrip('k'))
            else:
                item["Filesize"] = -1

            installs = title.xpath('//div[contains(text(), "Installs")]/following-sibling::span[1]/div/span/text()').extract_first()
            if installs:
                item["Installs"] = int(installs.replace(",", "").rstrip("+"))
            else:
                item["Installs"] = 0

            version = title.xpath('//div[contains(text(), "Current Version")]/following-sibling::span[1]/div/span/text()').extract_first()
            if version:
                item["Version"] = version
            else:
                item["Version"] = 'Unknown'
            
            compatibility = title.xpath('//div[contains(text(), "Requires Android")]/following-sibling::span[1]/div/span/text()').extract_first()
            if compatibility:
                item["Compatibility"] = compatibility
            else:
                item["Compatibility"] = 'Unknown'

            content_rating = title.xpath('//div[contains(text(), "Content Rating")]/following-sibling::span[1]/div/span/div/text()').extract_first()
            if content_rating:
                item["ContentRating"] = content_rating
            else:
                item["ContentRating"] = ''

            item["Genre"] = title.xpath('//a[@itemprop="genre"]/text()').extract_first()

            price = title.xpath('//meta[@itemprop="price"]/@content').extract_first()
            if price:
                item["Price"] = float(price.lstrip('NT$').replace(",", ""))
            else:
                item["Price"] = 0.0
            
            rating_value = title.xpath('//div[@class="K9wGie"]/div/text()').extract_first()
            if rating_value:
                item["RatingValue"] = float(rating_value)
            else:
                item["RatingValue"] = 0.0

            review_number = title.xpath('//span[@class="EymY4b"]/span[2]/text()').extract_first()
            if review_number:
                item["ReviewNumber"] = int(review_number.replace(",", ""))
            else:
                item["ReviewNumber"] = 0

            yield item
