import pandas as pd
import os
from models.data_processing import select_counties
from models.data_extraction import load_covid_data, extract_covid_data, load_uf_data, load_counties_data

uf = load_uf_data(
    os.environ.get('uf', 'SC')
)
covid_uf_cases = load_covid_data(uf)
cases_sample = select_counties(covid_uf_cases, uf)