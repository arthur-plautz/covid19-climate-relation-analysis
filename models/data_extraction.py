import requests
import os
import pandas as pd
from horology import timed

CURRENT_DIR = os.getcwd()

@timed
def download_data(local_url, source_url):
    r = requests.get(source_url, allow_redirects=True)
    open(local_url, 'wb').write(r.content)
    print('File Size: '+os.stat(local_url).st_size) 

def extract_covid_data(source_url, uf):
    local_url = f"{CURRENT_DIR}/data/covid_{uf['initials'].lower()}.csv"
    download_data(local_url, source_url)
    return local_url

def load_covid_data(uf):
    data_file = f"{CURRENT_DIR}/data/covid_{uf['initials'].lower()}.csv"
    df = pd.read_csv(data_file, encoding='ISO-8859-1', sep=';', error_bad_lines=False,index_col=False)
    df['id'] = range(1, len(df) + 1)
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
