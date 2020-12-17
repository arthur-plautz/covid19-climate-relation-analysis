from models.data_load import *
from models.data_analysis import *
from models.data_columns import *
from models.data_processing import *


covid_cases = read_processed('recife_covid_cases')
cases_climate = read_processed('recife_cases_climate_retroactive')

covid_cases = covid_cases.query('dt_primeiros_sintomas >= "2020-03-01"')

covid_cases = rolling_mean(covid_cases, 7)

cases_climate = time_series(cases_climate, 'date').mean()

covid_cases = covid_cases.query('dt_primeiros_sintomas >= "2020-03-07"')
cases_climate = cases_climate.query('date >= "2020-03-07"')

#cases_hist(covid_cases['id'])

#cases_hist_log(covid_cases['id'])

#all_measures(covid_cases['id'])

for attr in ['AT', 'RH', 'W', 'P']:
    rolling_meanXclimate_scatter(covid_cases, cases_climate, attr)

for attr in ['AT', 'RH', 'W', 'P']:
    linear_regression_rolling_meanXclimate_scatter(covid_cases, cases_climate, attr)

#data = transform_boxcox(covid_cases['id'])
#print(covid_cases['id'].max())
#cases_hist(data)

