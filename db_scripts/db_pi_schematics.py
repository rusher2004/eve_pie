from neo4j.v1 import GraphDatabase as gd
import db_queries as dbq
import csv

driver = dbq.driver
write_schematic = dbq.write_schematic
write_schematic_map = dbq.write_schematic_map

with driver.session() as session:
# 	with open('csv/planetSchematics.csv') as schematics:
# 		readCSV = csv.reader(schematics, delimiter=',')
# 		for row in readCSV:
# 			schematic_id = int(row[0])
# 			schematic_name = row[1]
# 			cycle_time = int(row[2])

# 			print('writing schematic: ' +  schematic_name)

# 			session.write_transaction(write_schematic, schematic_id, schematic_name, cycle_time)

	with open('csv/planetSchematicsTypeMap.csv') as schematics_map:
		readCSV = csv.reader(schematics_map, delimiter=',')
		next(readCSV, None)
		for row in readCSV:
			schematic_id = int(row[0])
			type_id = int(row[1])
			quantity = int(row[2])
			is_input = True if row[3] == '1' else False

			print('writing type: ' + str(type_id))

			session.write_transaction(write_schematic_map, schematic_id, type_id, quantity, is_input)

