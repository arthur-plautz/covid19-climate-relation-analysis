import pandas as pd
import os
from models.data_load import read_processed

covid_cases = read_processed('covid_cases')
cases_climate = read_processed('cases_climate')

print(covid_cases.head())
print(cases_climate.head())