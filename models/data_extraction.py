import requests
import os
import pandas as pd
import asyncio
from horology import timed

CURRENT_DIR = os.getcwd()

@timed
def download_data(local_url, source_url):
    r = requests.get(source_url, allow_redirects=True)
    open(local_url, 'wb').write(r.content)
    print('File Size: '+os.stat(local_url).st_size) 

def extract_covid_data(source_url, uf):
    local_url = f"{CURRENT_DIR}/data/covid_data/covid_{uf['initials'].lower()}.csv"
    download_data(local_url, source_url)
    return local_url

def load_covid_data(uf):
    data_file = f"{CURRENT_DIR}/data/covid_data/covid_{uf['initials'].lower()}.csv"
    df = pd.read_csv(data_file, encoding='ISO-8859-1', sep=';', error_bad_lines=False,index_col=False)
    df['id'] = range(1, len(df) + 1)
    return df

def extract_climate_data(counties, uf, time_init=3, time_limit=10):
    async def extract_county_climate(county):
        os.system(
            f"python models/execute_crawlers.py {time_init}/{time_limit} '{county}' '{uf}'"
        )
    
    async def extract_counties_climate():
        for county in counties:
            await extract_county_climate(county)

    asyncio.run(extract_counties_climate())

def load_climate_data(county):
    data_file = f"{CURRENT_DIR}/data/climate_data/climate_{county.replace(' ', '_')}.csv"
    df = pd.read_csv(data_file)
    return df

def load_counties_data(uf):
    data_file = f"{CURRENT_DIR}/data/county_list.csv"
    df = pd.read_csv(data_file)
    return df.query(f"COD_UF == {uf['code']}")

def load_uf_data(initials):
    data_file = f"{CURRENT_DIR}/data/uf_list.csv"
    df = pd.read_csv(data_file)
    uf = df.query(f"SIGLA == '{initials}'")
    return {
        'nome': uf['NOME'].item(),
        'code': uf['COD'].item(),
        'initials': uf['SIGLA'].item()
    }
