import numpy as np
import pandas as pd
import math
import datetime
from horology import timed
from calendar import monthrange
from models.data_extraction import load_counties_data, load_climate_data
from tools.formats import format_date, max_date, month_days, format_climate

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
    cases_county = covid_df.groupby('municipio_notificacao', as_index=False).count()
    mean_cases_county = cases_county.id.sum()/len(cases_county.id.unique())
    print(f"UF Mean: {math.floor(mean_cases_county)}")
    cases_county = cases_county.query(f"id > {mean_cases_county}")
    print(f"Counties: {len(cases_county)}")
    selected_counties = iterate_query_values(cases_county, 'municipio_notificacao')
    return covid_df.query(f"municipio_notificacao in ({selected_counties})")

def select_infection_period(climate_df, start_date):
    retroactive_period = 7
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
def compile_cases_climate(cases_df, climate_dict):
    cases_infection_climate = []
    for case in cases_df.to_records():
        case_date = case.data_inicio_sintomas.split(' ')[0]
        case_county = str(case.municipio_notificacao)
        climate_df = climate_dict[case_county]
        df = select_infection_period(climate_df, case_date)
        means = format_climate(df, case.id, case_date, case_county)
        cases_infection_climate.append(means)
    df = pd.DataFrame(cases_infection_climate)
    return df
