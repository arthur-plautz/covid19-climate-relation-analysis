from models.data_load import *
from models.data_analysis import *
from models.data_columns import *
from models.data_processing import *

covid_cases = read_processed(f'florianopolis_covid_cases')
cases_climate = read_processed(f'florianopolis_cases_climate_retroactive')

df = process_union(covid_cases, cases_climate)
print(df)

df.to_csv('florianopolis_data.csv')