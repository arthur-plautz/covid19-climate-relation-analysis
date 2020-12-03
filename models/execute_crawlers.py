import os
import json
import random
import datetime
import sys
import re
import asyncio
import math
import pandas as pd
from tools.formats import format_date, max_date, month_days

TMP = './crawlers/tmp'
DATA = './data/climate_data'
BASE_URL = "https://www.timeanddate.com"


async def process_url():
    with open(f"{TMP}/urls.json", 'r') as urls_file:
        urls = json.load(urls_file)
        rand = random.randint(0, len(urls)-1)
        url = urls[rand]
        return url['link']

async def process_data(date):
    with open(f"{TMP}/data.json", 'r') as data_file:
        try:
            data = json.load(data_file)
            if data:
                df = pd.DataFrame(data)
                return clean_data(df)
        except:
            pass

def clean_data(df):
    props = ['AT', 'W', 'RH', 'P', 'V']
    mean = {}
    for prop in props:
        df[prop] = [int(re.sub('[^0-9]','', value)) for value in df[prop]]
        mean[prop] = df[prop].mean()
    return mean

async def get_url(county, uf):
    os.environ['URL'] = f"{BASE_URL}/worldclock/?query={county.lower()}+{uf.lower()}+"
    os.environ['UF'] = f"{uf.lower()}"
    os.environ['COUNTY'] = f"{county.lower()}"
    os.system(
        f"scrapy runspider ./crawlers/url_spider.py --output={TMP}/urls.json"
    )
    county_url = await process_url()
    target_url = f"{BASE_URL}{county_url}"
    os.system(f"rm -R {TMP}")
    return target_url

async def get_data(url, year, month, day):
    date = f"{year}{format_date(month)}{format_date(day)}"
    if int(date) <= max_date():
        os.environ['URL'] = f"{url}/historic?year={year}&month={month}&hd={date}"
        os.system(
            f"scrapy runspider ./crawlers/climate_spider.py --output={TMP}/data.json"
        )
        data_avg = await process_data(date)
        os.system(f"rm -R {TMP}")
        return data_avg

async def main():
    if len(sys.argv) == 4:
        date = sys.argv[1].split('/')
        county = sys.argv[2]
        uf = sys.argv[3]
        url = await get_url(county, uf)
        data = []
        for month in range(int(date[0]), int(date[1])):
            for day in range(1, month_days(month)):
                avg = await get_data(url, str(2020), str(month), str(day))
                if avg:
                    avg['date'] = datetime.date(2020, month, day)
                    data.append(avg)
        if data:
            df = pd.DataFrame(data)
            df_file = f"{DATA}/climate_{county.replace(' ', '_')}.csv"
            if os.path.exists(df_file):
                data_df = pd.read_csv(df_file)
                data_df.append(df)
                os.system(f"rm {df_file}")
                df = data_df
            os.system(f"touch {df_file}")
            with open(df_file, 'w') as data_file:
                data_file.write(df.to_csv())

if __name__ == '__main__':
    if not os.path.exists(DATA):
        os.mkdir(DATA)
    asyncio.run(main())