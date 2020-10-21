import pandas as pd
import os
import numpy as np
from models.data_load import read_processed, basic_processing
import plotly.express as px

# basic_processing('SC')
covid_cases = read_processed('covid_cases')
cases_climate = read_processed('cases_climate')

cases_climate = cases_climate.sort_values('date')
cases_count = cases_climate.groupby('date', as_index=False).count()
cases_count.id = np.log(cases_count.id)
graph = px.line(cases_climate, x='date', y='AT')
graph.add_trace(px.line(cases_climate, x='date', y='RH').data[0])
# graph.add_trace(px.line(cases_count, x='date', y='id').data[0])
graph.show()