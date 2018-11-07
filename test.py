import os
import requests
from time import time as timer
from multiprocessing.pool import ThreadPool

session = requests.session()
q = "https://esi.evetech.net/latest/killmails/73309886/5014d3f4f8390f4620807aa7f91bdd5498e4957c/"

res = session.get(q).json()

if 'character_id' in res['victim']:
    print(f"character: {res['victim']['character_id']}")
elif 'corporation_id' in res['victim']:
    print(f"corp: {res['victim']['corporation_id']}")
elif 'alliance_id' in res['victim']:
    print(f"alliance: {res['victim']['alliance_id']}")
elif 'faction_id' in res['victim']:
    print(f"faction: {res['victim']['faction_id']}")

