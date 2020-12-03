# covid19-climate-relation-analysis
An Statistical model to watch possible correlations of covid-19 and weather/climate factors. Including data extraction, processing and transformations, for variable regions and covid-19 propagation data. 

# pre-requisites

1. Install *virtualenv*: `python3 -m pip install --user virtualenv`
2. Create a *virtualenv*: `virtualenv -p python3 venv`
3. Source *venv*: `source venv/bin/activate`
4. Install Requirements: `pip install -r requirements.txt`

# setup dataset columns

Create a `.env` file in the project root, like this:
```sh
export MUNICIPIO='municipio_notificacao'
export INICIO_SINTOMAS='data_inicio_sintomas' 
export SINTOMAS='sintomas' 
export IDADE='idade'
```
then before start your analysis, run the following command:
```sh
source .env
```