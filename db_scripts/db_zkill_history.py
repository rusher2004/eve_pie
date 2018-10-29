import requests as rq
import csv

s = rq.session()
year = int(input("Give year: "))

for m in range(1,13):
	csv_path = "./csv/zkill_history/" + str(year) + "{:0>2d}".format(m) + ".csv"
	print("working on file " + csv_path)
	with open(csv_path, "w", newline = '') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['kill_id', 'kill_hash'])
		for d in range(1,32):
			date = str(year) + "{:0>2d}".format(m) + "{:0>2d}".format(d)
			query = "https://zkillboard.com/api/history/" + date + "/"

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
