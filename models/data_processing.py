import numpy as np
import pandas as pd
import math
import datetime
from horology import timed
from calendar import monthrange
from models.data_extraction import load_counties_data, load_climate_data
from models.tools.formats import format_date, max_date, month_days, format_climate
from models.data_columns import *

def iterate_query_values(df, column):
    selection = ''
    for value in df[column]:
        selection += f"'{value}', "
    return selection[:-2]

def remove_values(df, column, target=[]):
    target = [str(t).lower() for t in target] + ['nan', 'undefined', 'null', 'none', '']
    values = df[column].unique()
    mapping = {}
    for value in values:
        if str(value).lower() not in target:
            mapping[value] = value
        else:
            mapping[value] = np.nan
    df[column] = df[column].map(mapping)
    return df[df[column].notna()]
    
def select_counties(covid_df, uf):
    cases_county = covid_df.groupby(MUNICIPIO, as_index=False).count()
    mean_cases_county = cases_county.id.sum()/len(cases_county.id.unique())
    print(f"UF Mean: {math.floor(mean_cases_county)}")
    cases_county = cases_county.query(f"id > {mean_cases_county}")
    print(f"Counties: {len(cases_county)}")
    selected_counties = iterate_query_values(cases_county, MUNICIPIO)
    return covid_df.query(f"{MUNICIPIO} in ({selected_counties})")

def select_infection_period(climate_df, start_date):
    retroactive_period = 10
    year, month, day = start_date.split('-')
    day_int = int(day)
    month_int = int(month)
    date_list = []
    i = day_int
    while i >= (day_int-retroactive_period):
        if i < 0:
            previous_month = month_days(month_int-1)
            date_list.append(f"{year}-{format_date(month_int-1)}-{format_date(previous_month+i)}")
        else:
            date_list.append(f"{year}-{format_date(month_int)}-{format_date(i)}")
        i -= 1
    infection_period_df = climate_df.loc[climate_df['date'].isin(date_list)]
    return infection_period_df

def climate_data_dict(counties):
    climate_dict = {}
    for county in counties:
        df = load_climate_data(county)
        climate_dict[county] = df
    return climate_dict

@timed
def compile_cases_climate(cases_df, climate_df, county=''):
    cases_infection_climate = []
    for case in cases_df.to_records():
        if not isinstance(case[INICIO_SINTOMAS], float):
            case_date = str(case[INICIO_SINTOMAS]).split(' ')[0]
            df = select_infection_period(climate_df, case_date)
            means = format_climate(df, case.id, case_date, county)
            cases_infection_climate.append(means)
    df = pd.DataFrame(cases_infection_climate)
    return df

def time_series(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.groupby(date_column)
    return df

def rolling_mean(df, window, column=INICIO_SINTOMAS):
    return time_series(df, column).sum().rolling(window).mean()

def series_rate(df, column):
    rate = []
    values = df[column]
    for i in range(len(values)):
        if values[i-1] == 0:
            growth_rate = np.nan
        else:
            growth_rate = values[i]/values[i-1]
        rate.append(growth_rate)
    return rate

def measure_function(serie, measure):
    functions = {
        'kurtosis': serie.kurtosis(),
        'skew': serie.skew(),
        'median': serie.median(),
        'mean': serie.mean(),
        'std': serie.std(),
        'mode': serie.mode()
    }
    return functions[measure]

def counties_group_measure(data_df, column, measure='kurtosis', county_column='municipio'):
    measures = []
    for county in data_df[county_column].unique():
        df = data_df.query(f"{county_column} == '{county}'").sort_values('date')
        x = df[column].dropna()
        measures.append(measure_function(x, measure))
    return measures

def growth_rate_measure(covid_cases, interval='W', measure='kurtosis'):
    measures = []
    for county in covid_cases[MUNICIPIO].unique():
        df = covid_cases.query(f"{MUNICIPIO} == '{county}'").sort_values(INICIO_SINTOMAS)
        df = time_series(df, INICIO_SINTOMAS).count().resample(interval).sum()
        serie = pd.Series(series_rate(df, 'id'))
        measures.append(measure_function(serie, measure))
    return measures

def single_symptoms_list(covid_cases):
    symptoms = {}
    for symptom in covid_cases[SINTOMAS].dropna().unique():
        symptoms_combined = symptom.replace(' ','').split(',')
        for single_symptom in symptoms_combined:
            if single_symptom not in symptoms.keys():
                symptoms[single_symptom] = 0
    return symptoms

def cases_symptoms_count(covid_cases):
    symptoms = single_symptoms_list(covid_cases)
    for case in covid_cases.to_records():
        case_symptoms = case[SINTOMAS]
        if str(case_symptoms) != 'nan':
            for symptom in case_symptoms.replace(' ','').split(','):
                symptoms[symptom] += 1
    return pd.DataFrame([{'sintoma': key, 'casos': value} for (key, value) in symptoms.items()])


def cases_age_count(covid_cases):
    ages = {'Abaixo dos 10': 0, 'De 10 a 18': 0, 'De 18 a 25': 0, 'De 25 a 35': 0, 'De 35 a 50': 0, 'De 50 a 70': 0, 'Acima dos 70': 0}
    for case in covid_cases.to_records():
        case_age = case[IDADE]
        if str(case_age) != 'nan':
            if case_age < 10:
                ages['Abaixo dos 10'] += 1
            elif case_age < 18:
                ages['De 10 a 18'] += 1
            elif case_age < 25:
                ages['De 18 a 25'] += 1
            elif case_age < 35:
                ages['De 25 a 35'] += 1
            elif case_age < 50:
                ages['De 35 a 50'] += 1
            elif case_age < 70:
                ages['De 50 a 70'] += 1
            else:
                ages['Acima dos 70'] += 1
    return pd.DataFrame([{'idade': key, 'casos': value} for (key, value) in ages.items()])