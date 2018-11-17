from neo4j.v1 import GraphDatabase as gd
from multiprocessing.pool import ThreadPool
import requests as rq
import db_queries as dbq
import os
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

write_character_kill = dbq.write_character_kill
write_corp_kill = dbq.write_corp_kill
write_alliance_kill = dbq.write_alliance_kill
write_faction_kill = dbq.write_faction_kill
write_csv_processing = dbq.write_csv_processing
write_csv_completed = dbq.write_csv_completed
# add_character_attacker = dbq.add_character_attacker
# add_corp_attacker = dbq.add_corp_attacker
# add_alliance_attacker = dbq.add_alliance_attacker
# add_faction_attacker = dbq.add_faction_attacker

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


def api_call(url):
	esi_get_query = url
	with driver.session() as this_session:
		try:
			esi_res = esi_session.get(esi_get_query, headers=headers, params=esi_payload).json()

			if 'character_id' in esi_res['victim']:
			    this_session.write_transaction(write_character_kill, esi_res)
			elif 'corporation_id' in esi_res['victim']:
				this_session.write_transaction(write_corp_kill, esi_res)
			elif 'alliance_id' in esi_res['victim']:
			    this_session.write_transaction(write_alliance_kill, esi_res)
			elif 'faction_id' in esi_res['victim']:
			    this_session.write_transaction(write_faction_kill, esi_res)

			# with open('json/data.json','a') as json_file:
			# 	json.dump(esi_res,json_file)
			# 	json_file.write('\n')

			return esi_res

		except Exception as e:
			with open(f"logs/{year}_esi_crawler_log.txt",'a') as log_file:
				log_file.write(f"{esi_get_query}\n")
			print('##Got error from ESI: ' + esi_get_query)
			print(e)

			return

esi_urls = []
start_time = time.time()
count = 0
year = int(input("Give year: "))

directory = os.path.join(f"csv/zkill_history/{year}")

for root,dirs,files in os.walk(directory):
	for file in files:
		filename = str(str(year) + str(file))
		with driver.session() as processing_session:
			processing_session.write_transaction(write_csv_processing, filename)
		with open(os.path.join(directory, file)) as csv_file:
			esi_urls[:] = []
			count = 0
			readCSV = csv.reader(csv_file, delimiter = ',')
			next(readCSV, None)
			for row in readCSV:
				kill_id = row[0]
				kill_hash = row[1]
				esi_get_query = esi_query + kill_id + "/" + kill_hash + "/"
				esi_urls.append(esi_get_query)

		results = ThreadPool(10).imap_unordered(api_call, esi_urls)
		for thing in results:
			print(f"writing line {str(count)} of {str(len(esi_urls))}")
			count += 1
		with driver.session() as completed_session:
			completed_session.write_transaction(write_csv_completed, filename)

end_time = math.floor(time.time())

print(f"Elapsed Time: {time.time() - start_time}")

