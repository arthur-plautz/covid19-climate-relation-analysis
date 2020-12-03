from models.data_load import *
from models.data_analysis import *
from models.data_columns import *

covid_cases = read_processed('florianopolis_covid_cases')

rolling_meanXresample(covid_cases, '2W', 15)