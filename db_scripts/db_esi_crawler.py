from neo4j.v1 import GraphDatabase as gd
import requests as rq
import db_queries as dbq
import csv
import json
import time, math

driver = dbq.driver
esi_session = rq.session()
zkb_session = rq.session()

esi_query = "https://esi.evetech.net/latest/killmails/"
zkb_query = "https://zkillboard.com/api/kills/killID/"
headers = {'User-Agent':'NERDb', 'Maintainer':'robertinthecloud@icloud.com'}
esi_payload = {"datasource":"tranquility"}


# res = esi_session.get('https://esi.evetech.net/latest/killmails/72460933/8d4922687cc60a9689c8176ed03042d58135a3ba/').json()

# def iterate(item):
# 	if isinstance(item,(dict)):
# 		for sub in item:
# 			iterate(item[sub])
# 	elif isinstance(item,list):
# 		for sub in item:
# 			iterate(sub)
# 	else:
# 		print(item)

# print(iterate(res))

# with open('json/data.json','a') as json_file:
# 	json.dump(res,json_file)
# 	json_file.write('\n')
start_time = math.floor(time.time())
count = 0

with driver.session() as db_session:
	with open('csv/zkill_history/test.csv') as csv_file:
		readCSV = csv.reader(csv_file, delimiter = ',')
		next(readCSV, None)
		for row in readCSV:
			kill_id = row[0]
			kill_hash = row[1]
			esi_get_query = esi_query + kill_id + "/" + kill_hash + "/"

			try:
				esi_res = esi_session.get(esi_get_query, headers=headers, params=esi_payload).json()
			except Exception as e:
				print('##Got error on kill #' + str(kill_id) + 'from ESI: ' + e)

			with open('json/data.json','a') as json_file:
				json.dump(esi_res,json_file)
				json_file.write('\n')
				print('writing line ' + str(count) + ' to file')
				count += 1

			# try:
			# 	something
			# except Exception as e:
			# 	print('##Got error on kill #' + str(kill_id) 'from ZKB: ' + e)
end_time = math.floor(time.time())

print('Processed ' + str(count) + ' rows in ' + str(end_time - start_time) + ' seconds. ' + str(math.floor(count / (end_time - start_time))) + ' rows per second.')

