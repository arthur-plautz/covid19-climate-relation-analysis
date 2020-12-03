from models.data_load import *
from models.data_analysis import *
from models.data_columns import *

covid_cases = read_processed('florianopolis_covid_cases')
cases_climate = read_processed('florianopolis_cases_climate')

# rolling_meanXresample(covid_cases, '2W', 15)
cases_climate = compile_cases_climate(covid_cases, cases_climate)
covid_cases = rolling_mean(covid_cases, 7)
casesXclimate_hist(covid_cases, 'id')
