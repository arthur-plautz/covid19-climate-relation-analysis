import pandas as pd
import os
import numpy as np
from models.data_processing import remove_values, time_series, series_rate, series_variation
from models.data_load import read_processed, basic_processing
from models.data_analysis import covidgrowthrate_climatechanges
import matplotlib.pyplot as plt

covid_cases = read_processed('covid_cases')
cases_climate = read_processed('cases_climate')

covidgrowthrate_climatechanges(cases_climate, covid_cases)

