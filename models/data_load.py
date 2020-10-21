import os
import pandas as pd
import asyncio
from horology import timed
from models.data_extraction import load_covid_data, extract_covid_data, load_uf_data, load_counties_data, extract_climate_data, load_climate_data
from models.data_processing import select_counties, select_infection_period, climate_data_dict, compile_cases_climate

CURRENT_DIR = os.getcwd()

@timed
def load_processed(df, name):
    local_url = f"{CURRENT_DIR}/data/processed_data/processed_{name}.csv"
    df.to_csv(local_url)

def basic_processing(uf):
    uf_data = load_uf_data(uf)
    covid_data = load_covid_data(uf_data)
    cases_sample = select_counties(covid_data, uf_data)
    load_processed(cases_sample, 'covid_cases')
    counties = cases_sample.municipio_notificacao.unique()
    climate_data = climate_data_dict(counties)
    cases_climate = compile_cases_climate(cases_sample, climate_data)
    load_processed(cases_climate, 'cases_climate')

def read_processed(name):
    local_url = f"{CURRENT_DIR}/data/processed_data/processed_{name}.csv"
    return pd.read_csv(local_url)