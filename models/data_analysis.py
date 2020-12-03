import matplotlib.pyplot as plt
import pandas as pd
from models.data_processing import time_series, series_rate, counties_group_measure, growth_rate_measure, cases_symptoms_count, cases_age_count
from models.data_columns import *

def growth_rateXcases(covid_cases, interval, county=None):
    if county:
        covid_cases = covid_cases.query(f"municipio == '{county}'")
    covid_cases_serie = time_series(covid_cases, INICIO_SINTOMAS).sum().resample(interval).sum()

    fig, ax1 = plt.subplots(figsize=(12,5))

    ax1.set_xlabel('date')
    ax1.plot(covid_cases_serie.index, series_rate(covid_cases_serie, "id"), color='grey')
    ax1.set_ylabel('Growth Rate', color='gray')

    ax2 = ax1.twinx()
    ax2.plot(covid_cases_serie.index, covid_cases_serie.id, color='black')
    ax2.set_ylabel('Cases Registered', color='black')

    plt.title(f'Growth Rate X Cases ({county})')
    plt.show()
    
def growth_rateXclimate_changes(cases_climate, covid_cases, interval, county=None):
    if county:
        cases_climate = cases_climate.query(f"municipio == '{county}'")
        covid_cases = covid_cases.query(f"municipio == '{county}'")
    cases_climate = cases_climate.sort_values('date')
    cases_climate_serie = time_series(cases_climate, 'date').mean().resample(interval).mean()

    covid_cases_serie = time_series(covid_cases, INICIO_SINTOMAS).sum().resample(interval).sum()

    fig, ax1 = plt.subplots(figsize=(12,5))

    ax1.set_xlabel('date')
    ax1.plot(covid_cases_serie.index, series_rate(covid_cases_serie, "id"), color='black')
    ax1.set_ylabel(f'Covid Growth Rate (Last {interval})', color='black')

    ax2 = ax1.twinx()
    ax2.plot(covid_cases_serie.index, cases_climate_serie.AT, color='red')
    ax2.set_ylabel('Ambient Temperature', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax3 = ax1.twinx()
    ax3.plot(covid_cases_serie.index, cases_climate_serie.RH, color='blue')
    ax3.set_ylabel('Relative Humidity', color='blue')
    ax3.tick_params(axis='y', labelcolor='blue')

    plt.title(f'Growth Rate X Temperature X Relative Humidity ({county})')
    plt.show()

def casesXclimate(cases_climate, county=None):
    if county:
        cases_climate = cases_climate.query(f"municipio == '{county}'")
    fig, ax1 = plt.subplots(figsize=(5,12))
    ax1.boxplot([cases_climate.AT.dropna(), []])
    ax1.set_ylabel('Ambient Temperature')
    
    ax2 = ax1.twinx()
    ax2.boxplot([[], cases_climate.RH.dropna()])
    ax2.set_ylabel('Relative Humidity')
    plt.title(f'Cases Infection Week Conditions ({county})')
    plt.show()

def climateXcases_age(covid_cases, cases_climate):
    pass

def cases_age_analysis(covid_cases):
    ages = cases_age_count(covid_cases)
    print(ages)
    ages = ages.sort_values('casos')
    print(ages.casos.kurtosis())
    print(ages.casos.std())
    plt.bar(ages.idade, ages.casos)
    plt.show()

def growth_rate_analysis(covid_cases):

    growth_rates_skew = growth_rate_measure(covid_cases, interval='W', measure='skew')
    growth_rates_kurtosis = growth_rate_measure(covid_cases, interval='W', measure='kurtosis')

    fig, ax1 = plt.subplots(figsize=(5,12))
    ax1.boxplot([growth_rates_kurtosis, []])
    ax1.set_ylabel('Valores de Curtose para Taxa de Crescimento')
    
    ax2 = ax1.twinx()
    ax2.boxplot([[], growth_rates_skew])
    ax2.set_ylabel('Valores do Coeficiente de Assimetria para Taxa de Crescimento')
    plt.title(f'Análise da Taxa de Crescimento de Casos')
    plt.show()

def cases_symptoms_analysis(covid_cases):
    symptoms = cases_symptoms_count(covid_cases).sort_values('casos')
    print(symptoms)
    print(symptoms.casos.kurtosis())
    print(symptoms.casos.std())
    plt.bar(symptoms.sintoma, symptoms.casos)
    plt.show()