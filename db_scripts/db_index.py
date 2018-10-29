from neo4j.v1 import GraphDatabase as gd
import db_queries as dbq

driver = dbq.driver
get_labels = dbq.get_labels
write_index = dbq.write_index


with driver.session() as session:
	res = session.read_transaction(get_labels)

	for i in res:
		print('Creating index for node ' + i['label'] + ' on ' + i['label'] + '_id')
		session.write_transaction(write_index, i['label'], False, 0)