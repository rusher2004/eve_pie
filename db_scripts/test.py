import os
import csv
import glob

year = input("Give year: ")

directory = os.path.join(f"csv/zkill_history/{year}")

for root,dirs,files in os.walk(directory):
    for file in files:
        with open(os.path.join(directory, file)) as csv_file:
            readCSV = csv.reader(csv_file, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                print(f"kill id: {row[0]} - kill hash: {row[1]}")
