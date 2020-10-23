import pandas as pd
import os
import numpy as np
from models.data_processing import remove_values, time_series, series_rate, series_variation
from models.data_load import read_processed, basic_processing
import matplotlib.pyplot as plt

covid_cases = read_processed('covid_cases')
cases_climate = read_processed('cases_climate')

cases_climate.date = pd.to_datetime(cases_climate.date)
cases_climate = cases_climate.query("municipio == 'FLORIANOPOLIS'").sort_values('date')

covid_cases_serie = time_series(covid_cases, 'data_inicio_sintomas')