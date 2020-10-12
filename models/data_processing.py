import numpy as np
import pandas as pd
import math
from models.data_extraction import load_counties_data

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