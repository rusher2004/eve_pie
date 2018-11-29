from neo4j.v1 import GraphDatabase as gd
from .db_queries import Queries as dbq
import os
import requests
import json
import time, math
from .secrets import Secrets

username = Secrets.username
password = Secrets.password
db_driver = gd.driver("bolt://142.93.190.84:7687", auth=(username, password))
get_character_attackers = dbq.get_character_attackers
get_character_victims = dbq.get_character_victims
get_character_demos = dbq.get_character_demos
get_corporation_demos = dbq.get_corporation_demos
get_alliance_demos = dbq.get_alliance_demos

esi_session=requests.session()
esi_alliance_info_query = "https://esi.evetech.net/latest/alliances/"

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

class Character():

    def __init__(self, character_id, primary):
        main_timer_start = time.time()
        attackers_duration = 0
        victims_duration = 0

        with db_driver.session() as session:
            res = session.read_transaction(get_character_demos, character_id)
            for i in res:
                for j in i:
                    self.demos = j
        self.demos['security_status'] = truncate(self.demos['security_status'], 2)
        self.corporation = Corporation(self.demos['corporation_id'])
        if primary:
            attackers_start = time.time()
            self.attackers = []
            with db_driver.session() as attacker_session:
                res = attacker_session.read_transaction(get_character_attackers, self.demos['character_id'])
                count = 0
                for i in res:
                    for j in i:
                        self.attackers.append(Character(j['stats']['attacker_id'], False))
                        self.attackers[count].attack_count = j['stats']['attacks']
                    count += 1
            attackers_duration = (math.floor(time.time()) - attackers_start)

            victims_start = time.time()
            self.victims = []
            with db_driver.session() as victim_session:
                res = victim_session.read_transaction(get_character_victims, self.demos['character_id'])
                count = 0
                for i in res:
                    for j in i:
                        self.victims.append(Character(j['stats']['victim_id'], False))
                        self.victims[count].attack_count = j['stats']['attacks']
                    count += 1
            victims_duration = (math.floor(time.time()) - victims_start)


        if primary:
            main_duration = (math.floor(time.time()) - main_timer_start)
            print(f"Main timer: {main_duration}")
            print(f"Attackers timer: {attackers_duration}")
            print(f"Victims timer: {victims_duration}")

class Corporation():

    def __init__(self, corporation_id):
        with db_driver.session() as session:
            res = session.read_transaction(get_corporation_demos, corporation_id)
            for i in res:
                for j in i:
                    self.demos = j
        if self.demos['alliance_id'] is not None:
            self.alliance = Alliance(self.demos['alliance_id'])
        # if type(self.demos.get('faction_id')) == 'int':
        #     self.faction = Faction(self.demos['faction_id'])

class Alliance():

    def __init__(self, alliance_id):
        with db_driver.session() as session:
            res = session.read_transaction(get_alliance_demos, alliance_id)
            for i in res:
                for j in i:
                    self.demos = j

        # if type(self.demos.get('faction_id')) == 'int':
        #     self.faction = Faction(self.demos['faction_id'])

class Faction():

    def __init__(self, faction_id):
        self.faction_id = faction_id

        # with open('factions.json', 'r') as json_file:
        #     json_data = json.load(json_file)
        #     print(json_data)

class Test():

    def __init__(self, corporation_id):
        with db_driver.session() as session:
            res = session.read_transaction(get_corporation_demos, corporation_id)

        for i in res:
            print(i)
            for j in i:
                self.info = j
                # print(j)
