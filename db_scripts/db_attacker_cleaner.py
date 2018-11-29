from neo4j.v1 import GraphDatabase as gd
import db_queries as dbq

driver = dbq.driver
attacker_cleaner = dbq.attacker_cleaner

while True:
    try:
        with driver.session() as session:
            res = session.read_transaction(attacker_cleaner)
            
            for i in res:
                print(i)
    except Exception as e:
        print(e)
