from neo4j.v1 import GraphDatabase as gd
from .db_queries import Queries as dbq
import os
import requests
import json

username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')
db_driver = gd.driver("bolt://142.93.190.84:7687", auth=(username, password))
get_character_attackers = dbq.get_character_attackers
get_character_victims = dbq.get_character_victims

esi_session=requests.session()
esi_character_info_query = "https://esi.evetech.net/latest/characters/"
esi_corporation_info_query = "https://esi.evetech.net/latest/corporations/"
esi_alliance_info_query = "https://esi.evetech.net/latest/alliances/"



class Character():

    def __init__(self, character_id, primary):
        self.character_id = character_id
        self.info = esi_session.get(esi_character_info_query + str(self.character_id)).json()
        self.name = self.info['name']
        self.corporation_id = self.info['corporation_id']
        self.corporation = Corporation(self.corporation_id)
        if 'alliance_id' in self.info:
            self.alliance_id = self.info['alliance_id']
            self.alliance = Alliance(self.alliance_id)
        if 'faction_id' in self.info:
            self.faction_id = self.info['faction_id']
            self.faction = Faction(self.faction_id)
        if primary:
            self.attackers = []
            with db_driver.session() as session:
                res = session.read_transaction(get_character_attackers, self.character_id)
                count = 0
                for i in res:
                    self.attackers.append(Character(i['stats']['attacker_id'], False))
                    self.attackers[count].attack_count = i['stats']['attacks']
                    count += 1

            self.victims = []
            with db_driver.session() as session:
                res = session.read_transaction(get_character_victims, self.character_id)
                count = 0
                for i in res:
                    self.victims.append(Character(i['stats']['victim_id'], False))
                    self.victims[count].attack_count = i['stats']['attacks']
                    count +=1

class Corporation():

    def __init__(self, corporation_id):
        self.corporation_id = corporation_id
        self.info = esi_session.get(esi_corporation_info_query + str(self.corporation_id)).json()
        self.name = self.info['name']
        self.ticker = self.info['ticker']

        if 'alliance_id' in self.info:
            self.alliance_id = self.info['alliance_id']
            self.alliance = Alliance(self.alliance_id)
        if 'faction_id' in self.info:
            self.faction_id = self.info['faction_id']
            self.faction = Faction(self.faction_id)

class Alliance():

    def __init__(self, alliance_id):
        self.alliance_id = alliance_id
        self.info = esi_session.get(esi_alliance_info_query + str(self.alliance_id)).json()
        self.name = self.info['name']
        self.ticker = self.info['ticker']

        if 'faction_id' in self.info:
            self.faction_id = self.info['faction_id']
            self.faction = Faction(self.faction_id)

class Faction():

    def __init__(self, faction_id):
        self.faction_id = faction_id

        # with open('factions.json', 'r') as json_file:
        #     json_data = json.load(json_file)
        #     print(json_data)

