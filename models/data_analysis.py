import matplotlib.pyplot as plt
import pandas as pd
from models.data_processing import time_series, series_rate

def covidgrowthrate_climatechanges(cases_climate, covid_cases):
    cases_climate = cases_climate.query("municipio == 'FLORIANOPOLIS'").sort_values('date')

    covid_cases_serie = time_series(covid_cases, 'data_inicio_sintomas').sum().resample('W').sum()

    cases_climate_serie = time_series(cases_climate, 'date').mean().resample('W').mean()

    fig, ax1 = plt.subplots(figsize=(12,5))

    ax1.set_xlabel('date')
    ax1.plot(covid_cases_serie.index, series_rate(covid_cases_serie, "id"), color='red')
    ax1.set_ylabel('', color='red')


    ax2 = ax1.twinx()

    ax2.plot(covid_cases_serie.index, covid_cases_serie.id, color='lightgray')
    ax2.set_ylabel('', color='gray')

    ax3 = ax1.twinx()

    ax3.plot(covid_cases_serie.index, cases_climate_serie.AT, color='purple')
    ax3.set_ylabel('', color='purple')

    plt.title('')
    plt.show()