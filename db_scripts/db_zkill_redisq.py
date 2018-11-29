import requests as rq
import db_queries as dbq
import os
import json
from datetime import datetime as dt


driver = dbq.driver
s = rq.Session()
query = "https://redisq.zkillboard.com/listen.php"

write_character_kill = dbq.write_character_kill
write_corp_kill = dbq.write_corp_kill
write_alliance_kill = dbq.write_alliance_kill
write_faction_kill = dbq.write_faction_kill

while True:
    with driver.session() as session:
        try:
            res = s.get(query).json()
            print(f"got kill {res['package']['killID']}")
            killmail = res['package']['killmail']

            if 'character_id' in killmail['victim']:
                session.write_transaction(write_character_kill, killmail)
            elif 'corporation_id' in killmail['victim']:
                session.write_transaction(write_corp_kill, killmail)
            elif 'alliance_id' in killmail['victim']:
                session.write_transaction(write_alliance_kill, killmail)
            elif 'faction_id' in killmail['victim']:
                session.write_transaction(write_faction_kill, killmail)

        except Exception as e:
            now_timestamp = str(dt.now().isoformat())
            hour_timestamp = dt.now().strftime("%Y-%m-%d-%H")
            with open(f"logs/{hour_timestamp}_redisq_log.txt",'a') as log_file:
                log_file.write(f"{now_timestamp} - {e}\n")
            print(e)
