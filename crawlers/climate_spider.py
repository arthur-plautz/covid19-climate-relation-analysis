import scrapy
import os

class ClimateSpider(scrapy.Spider):
    name = 'urlspider'
    start_urls = [os.environ.get('URL')]

    def parse(self, response):
        for hour in response.css('table#wt-his>tbody>tr'):
            hour_metrics = {}
            metric_counter = 0
            metrics = ['AT', 'C', 'W', None, 'RH', 'P', 'V']
            hour_metrics['time'] = hour.css('th ::text').get()
            for metric in hour.css('td ::text'):
                if metric_counter in [0,1,2,4,5,6]:
                    hour_metrics[metrics[metric_counter]] = metric.get()
                metric_counter +=1
            yield hour_metrics