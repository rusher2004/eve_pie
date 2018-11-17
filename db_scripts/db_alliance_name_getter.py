from time import sleep
from  datetime import datetime
import requests as rq
import db_queries as dbq

driver = dbq.driver

s = rq.session()
esi_query = "https://esi.evetech.net/latest/alliances/names/?alliance_ids="
datasource = "&datasource=tranquility"
user_agent = "&user_agent=eve-pie"

alliances_without_names_db_query = dbq.alliances_without_names_db_query
write_alliance_names = dbq.write_alliance_names

while True:
    name_list = []
    names_to_set = True

    with driver.session() as session:
        res = session.read_transaction(alliances_without_names_db_query)
        for i in res:
            name_list.append(i[0]['alliance_id'])

    get_query = esi_query
    for i in name_list:
        get_query += str(i) + ","
    get_query = get_query[:-1] + user_agent + datasource

    res = s.get(get_query).json()
    for j in res:
        print(j)

    try:
        count = 1
        for i in res:
            id = int(i['alliance_id'])
            name = i['alliance_name']

            print("writing alliance number " + str(count) + " of " + str(len(res)))
            with driver.session() as session:
                session.write_transaction(set_alliance_names, id, name)
            count += 1
    except Exception as e:
        print(e)
        names_to_set = False

    if names_to_set == False:
        print(str(datetime.now().time()) + ": No names to assign right now")
        break
