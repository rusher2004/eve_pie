from neo4j.v1 import GraphDatabase as gd
import db_queries as dbq
import csv

driver = dbq.driver
write_item = dbq.write_item

with driver.session() as session:
	with open('csv/invTypes.csv') as item_file:
		readCSV = csv.reader(item_file, delimiter = ',')
		for row in readCSV:
			type_id = int(row[0])
			group_id = int(row[1])
			name = row[2]
			desc = row[3] if row[3] else ''
			portion_size = int(row[7])
			race_id = int(row[8]) if row[8].lower() != 'none' else ''
			published = True if row[10] == '1' else False
			market_group = int(row[11]) if row[11].lower() != 'none' else ''
			icon_id = int(row[12]) if row[12].lower() != 'none' else ''
			graphic_id = int(row[14])

			print('writing item: ' + name)
			print(str(group_id))
			session.write_transaction(write_item, type_id, group_id, name, desc, portion_size, race_id, published, market_group, icon_id, graphic_id)
