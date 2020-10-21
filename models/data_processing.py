import numpy as np
import pandas as pd
import math
from calendar import monthrange
from models.data_extraction import load_counties_data, load_climate_data

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
    year, month, day = start_date.split('-')
    day_int = int(day)
    month_int = int(month)
    month_dict = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    inicial_date = day_int - 10
    list_date = []
    if inicial_date < 1:
        previous_month_value = month_dict[month_int - 1]
        previous_month = month_int - 1
        for i in range(abs(inicial_date)+1):
            if i < 10:
                list_date.append(year + '-0' + str(previous_month) + '-' + str(previous_month_value + inicial_date + i))
            else:
                list_date.append(year + '-' + str(previous_month) + '-' + str(previous_month_value + inicial_date + i))
        for i in range(1, day_int):
            if i < 10:
                list_date.append(year + '-' + month + '-0' + str(i))
            else:
                list_date.append(year + '-' + month + '-' + str(i))
    else:
        for i in range(day_int - 10, day_int):
            if i < 10:
                list_date.append(year + '-' + month + '-0' + str(i))
            else:
                list_date.append(year + '-' + month + '-' + str(i))
    infection_period_df = climate_df.loc[climate_df['date'].isin(list_date)]
    return infection_period_df

def climate_data_dict(df, counties_unique_values):
    climate_dict = {}
    for county in counties_unique_values:
        df_new = load_climate_data(county)
        climate_dict[county.replace(" ", "_")] = df_new
    return climate_dict
