import scrapy
import os
import re
import unicodedata as ud

class UrlSpider(scrapy.Spider):
    name = 'urlspider'
    start_urls = [os.environ.get('URL')]

    def clear_str(self, s):
        s = ud.normalize('NFKD', s)
        return re.sub('[^A-Za-z0-9]+', '', s.lower())

    def parse(self, response):
        county = os.environ.get('COUNTY')
        uf = os.environ.get('UF')
        for link in response.css('td>a'):
            link_text = link.css('a ::text').get()
            link_text = self.clear_str(link_text)
            location = f"brazil{uf}{county}"
            location = self.clear_str(location)
            if location.find(link_text) != -1:
                link_url = link.css('a').attrib['href']
                yield {'link': link_url.replace('worldclock', 'weather'), 'title': link_text}