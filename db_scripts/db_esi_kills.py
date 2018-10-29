import requests as rq
import csv
from pandas.io.json import json_normalize

s = rq.session()
query = "https://esi.evetech.net/latest/killmails/68347436/fe520294467fc9e668646459839736e5aa8a4609/?datasource=tranquility"

res = s.get(query).json()

pd_data = json_normalize(res)
csv_data = pd_data.to_csv()

with open("test.csv", "w", newline = '') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow([csv_data])

print(csv_data)