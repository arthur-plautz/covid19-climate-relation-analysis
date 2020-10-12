import scrapy
import os

class ClimateSpider(scrapy.Spider):
    name = 'urlspider'
    start_urls = [os.environ.get('URL')]

    def parse(self, response):
        hour_counter = 0
        for hour in response.css('table#wt-his>tbody>tr'):
            if hour_counter in [8, 10, 12, 14, 16, 18, 20, 22]:
                hour_metrics = {}
                metric_counter = 0
                metrics = [None, None, 'AT', None, 'W', 'RH']
                hour_metrics['time'] = hour.css('th ::text').get()
                for metric in hour.css('td ::text'):
                    if metric_counter in [2,4,5]:
                        hour_metrics[metrics[metric_counter]] = metric.get()
                    metric_counter +=1
                yield hour_metrics
            hour_counter += 1