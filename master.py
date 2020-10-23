import pandas as pd
import os
import numpy as np
from models.data_processing import remove_values
from models.data_load import read_processed, basic_processing
import plotly.graph_objects as go

covid_cases = read_processed('covid_cases')
cases_climate = read_processed('cases_climate')

cases_climate.date = pd.to_datetime(cases_climate.date)
cases_climate = cases_climate.query("municipio == 'FLORIANOPOLIS'").sort_values('date')
covid_cases.data_inicio_sintomas = pd.to_datetime(covid_cases.data_inicio_sintomas)
cases_count = covid_cases.groupby('data_inicio_sintomas').count()

cases_model = cases_count.resample('1D').sum()

trace1 = go.Scatter(
    x=cases_model.index,
    y=cases_model.id,
    yaxis="y1"
)
trace2 = go.Scatter(
    x=cases_climate.date,
    y=cases_climate.AT,
    yaxis="y2"
)
data = [trace1, trace2]
layout = go.Layout(
    yaxis=dict(
        domain=[1/4, 1]
    ),
    yaxis2=dict(
        domain=[0, 1/4]
    )
)
fig = go.Figure(data=data, layout=layout)
fig.show()