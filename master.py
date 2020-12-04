from models.data_load import *
from models.data_analysis import *
from models.data_columns import *
import scipy.stats as s

covid_cases = read_processed('florianopolis_covid_cases')
cases_climate = read_processed('florianopolis_cases_climate_retroactive')

# rolling_meanXresample(covid_cases, 'W', 7)
covid_cases = rolling_mean(covid_cases, 7)
# print(covid_cases['id'].min())
# skewed_box_cox, lmda = s.boxcox(covid_cases['id'])
# cases_climate = time_series(cases_climate, 'date').mean()
# cases_hist(covid_cases['id'])
# cases_hist(covid_cases['id'])
# all_measures(covid_cases['id'])
# print(len(covid_cases), len(cases_climate))
# for attr in ['AT', 'RH', 'W', 'P']:
    # rolling_meanXclimate_scatter(covid_cases, cases_climate, attr)
# cases_hist_log(covid_cases)

#scatter(covid_cases)