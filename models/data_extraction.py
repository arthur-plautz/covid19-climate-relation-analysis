import requests

state = 'sc'
url = f'https://s3-sa-east-1.amazonaws.com/ckan.saude.gov.br/dados-{state}.csv'

r = requests.get(url, allow_redirects=True)
open(f'../data/covid_{state}_notifications.csv', 'wb').write(r.content)