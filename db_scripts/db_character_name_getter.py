from time import sleep
from  datetime import datetime
import requests as rq
import db_queries as dbq

driver = dbq.driver

s = rq.session()
esi_query = "https://esi.evetech.net/latest/universe/names/"
datasource = "?datasource=tranquility"
user_agent = "&user_agent=NERDB-test"
headers = {'User-Agent':'NERDb', 'Maintainer':'robertinthecloud@icloud.com'}
esi_payload = {"datasource":"tranquility"}

# post_query = esi_query + datasource + user_agent

characters_without_names_db_query = dbq.characters_without_names_db_query
set_character_names = dbq.set_character_names

while True:
    char_list = []
    names_to_set = True

    with driver.session() as session:
        res = session.read_transaction(characters_without_names_db_query)
        #print(res["character_id"])
        for i in res:
            char_list.append(i[0]['character_id'])

    try:
        res = s.post(esi_query, headers=headers, params=esi_payload, json = char_list)
        res = res.json()
    except Exception as e:
        print(e)

    try:
        count = 1
        with driver.session() as session:
            for i in res:
                id = int(i['id'])
                name = i['name']

                # print("writing character number " + str(count) + " of " + str(len(res)) + ": " + name)
                session.write_transaction(set_character_names, id, name)
                count += 1
    except Exception as e:
        print('setting false')
        print(e)
        names_to_set = False

    if names_to_set == False:
        print(str(datetime.now().time()) + ": No names to assign right now. Checking again in 5 minutes.")
        sleep(300)
