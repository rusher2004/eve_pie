import requests as rq
import db_queries as dbq

driver = dbq.driver

s = rq.session()
esi_query = "https://esi.evetech.net/latest/alliances/"
datasource = "?datasource=tranquility"
user_agent = "&user_agent=eve-pie"
query = esi_query + datasource + user_agent

write_alliance_ids = dbq.write_alliance_ids

res = s.get(query).json()

for i in res:
    alliance_id = int(i)
    print("writing alliance number " + str(i))

    with driver.session() as session:
        session.write_transaction(write_alliance_ids, alliance_id)