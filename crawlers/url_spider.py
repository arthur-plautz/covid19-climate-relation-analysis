import scrapy
import os

class UrlSpider(scrapy.Spider):
    name = 'urlspider'
    start_urls = [os.environ.get('URL')]

    def parse(self, response):
        print(os.environ.get('URL'))
        for link in response.css('td>a'):
            link_text = link.css('a ::text').get()
            county = os.environ.get('COUNTY')
            if link_text.lower().find(county) != -1:
                link_url = link.css('a').attrib['href']
                yield {'link': link_url.replace('worldclock', 'weather'), 'title': link_text}