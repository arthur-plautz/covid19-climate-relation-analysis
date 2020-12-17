import matplotlib.pyplot as plt
import pandas as pd
from models.data_processing import *
from models.data_columns import *
from sklearn.linear_model import LinearRegression

def all_climate_scatters(covid_cases, cases_climate):
    for attr in ['AT', 'RH', 'W', 'P']:
        rolling_meanXclimate_scatter(covid_cases, cases_climate, attr)

def rolling_meanXclimate_scatter(covid_cases, cases_climate, column):
    plt.scatter(cases_climate[column], covid_cases['id'])
    plt.xlabel(f'{column} (Retroactive Mean)')
    plt.ylabel('Covid Cases (Rolling Mean)')
    plt.show()

def linear_regression_rolling_meanXclimate_scatter(covid_cases, cases_climate, column):
    regr = LinearRegression()
    regr.fit(np.array(cases_climate[column]).reshape(-1, 1), covid_cases['id'])
    plt.scatter(np.array(cases_climate[column]).reshape(-1, 1), covid_cases['id'])
    plt.plot(np.array(cases_climate[column]).reshape(-1, 1), regr.predict(np.array(cases_climate[column]).reshape(-1, 1)), color='red')
    plt.xlabel(f'{column} (Retroactive Mean)')
    plt.ylabel('Covid Cases (Rolling Mean)')
    plt.show()

def rolling_meanXresample(covid_cases, interval, window):
    covid_cases_resample = time_series(covid_cases, INICIO_SINTOMAS).sum().resample(interval).sum()
    covid_cases_rolling_mean = time_series(covid_cases, INICIO_SINTOMAS).sum().rolling(window).mean()

    fig, ax1 = plt.subplots(figsize=(12,5))

    ax1.set_xlabel('date')
    ax1.plot(covid_cases_rolling_mean.index, covid_cases_rolling_mean.id, color='grey')
    ax1.set_ylabel('Rolling Mean', color='gray')

    ax2 = ax1.twinx()
    ax2.plot(covid_cases_resample.index, covid_cases_resample.id, color='black')
    ax2.set_ylabel('Resample', color='black')

    plt.title(f'Rolling Mean Method X Resample Method')
    plt.show()

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

def casesXclimate_boxplot(cases_climate, county=None):
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

def cases_hist(covid_cases):
    plt.hist(covid_cases, bins=10)
    plt.xlabel('Covid Cases (Rolling Mean)')
    plt.ylabel('Frequency')
    plt.show()

def cases_hist_log(covid_cases):
    plt.hist(np.log(covid_cases), bins=10)
    plt.xlabel('Covid Cases (Rolling Mean transformed by ln)')
    plt.ylabel('Frequency')
    plt.show()


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