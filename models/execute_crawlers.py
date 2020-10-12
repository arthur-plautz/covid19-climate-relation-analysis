import os
import json
import random
import datetime

TMP = './crawlers/tmp'
BASE_URL = "https://www.timeanddate.com"
TIME_RANGE = 4

def format_date(date):
    if date < 10:
        return f"0{date}"
    else:
        return date

def max_date():
    today = datetime.date.today()
    if today.day < 10:
        day = f"0{today.day}"
    else:
        day = today.day
    return int(f"{today.year}{today.month}{day}")

def process_url():
    with open(f"{TMP}/urls.json", 'r') as urls_file:
        urls = json.load(urls_file)
        rand = random.randint(0, len(urls)-1)
        url = urls[rand]
        return url['link']

def process_data(date):
    with open(f"{TMP}/data.json", 'r') as data_file:
        try:
            data = json.load(data_file)
            data['date'] = date
        except:
            data = None
        return data

def get_url(county, uf):
    os.environ['URL'] = f"{BASE_URL}/worldclock/?query={county.lower()}+{uf.lower()}+"
    os.environ['COUNTY'] = f"{county.lower()}"
    os.system(
        f"scrapy runspider ./crawlers/url_spider.py --output={TMP}/urls.json"
    )
    target_url = f"{BASE_URL}{process_url()}"
    os.system(f"rm -R {TMP}")
    return target_url

def get_data(url, year, month, day):
    date = f"{year}{format_date(month)}{format_date(day)}"
    if int(date) <= max_date():
        os.environ['URL'] = f"{url}/historic?hd={date}"
        os.system(
            f"scrapy runspider ./crawlers/climate_spider.py --output={TMP}/data.json"
        )
        tmp_data = process_data(date)
        os.system(f"rm -R {TMP}")
        if tmp_data:
            with open('data.json', 'w') as data_file:
                data_file.write(tmp_data)

