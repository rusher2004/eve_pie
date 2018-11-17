import requests as rq
import csv

s = rq.session()
year = int(input("Give year: "))

for m in range(1,13):
	month = "{:0>2d}".format(m)
	for d in range(1,32):
		day = "{:0>2d}".format(d)
		csv_path = f"./csv/zkill_history/{year}/{month}{day}.csv"
		print("working on file " + csv_path)

		with open(csv_path, "w", newline = '') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(['kill_id', 'kill_hash'])

			query = f"https://zkillboard.com/api/history/{year}{month}{day}/"

			try:
				res = s.get(query).json()
				if not res:
					print(date + ' does not exist')
				else:
					for line in res:
						writer.writerow([line, res[line]])
			except Exception as e:
				print("caught error on date: " + date)
				print(e)
