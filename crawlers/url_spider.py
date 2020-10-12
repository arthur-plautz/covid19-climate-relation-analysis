import scrapy
import os
import re

class UrlSpider(scrapy.Spider):
    name = 'urlspider'
    start_urls = [os.environ.get('URL')]

    def parse(self, response):
        county = os.environ.get('COUNTY')
        uf = os.environ.get('UF')
        for link in response.css('td>a'):
            link_text = link.css('a ::text').get()
            link_text = re.sub('[^A-Za-z0-9]+', '', link_text.lower())
            location = f"brazil{uf}{county}"
            location = re.sub('[^A-Za-z0-9]+', '', location.lower())
            if location.find(link_text) != -1:
                link_url = link.css('a').attrib['href']
                yield {'link': link_url.replace('worldclock', 'weather'), 'title': link_text}