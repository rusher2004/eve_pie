MERGE (k:killmail {killmail_id: killmail_id})
SET k.time=killmail_time, k.x=toFloat(x), k.y=toFloat(y), k.z=toFloat(z), k.ship_type_id=toInteger(ship_type_id), k.victim_coporation_id=toInteger(victim_coporation_id), k.victim_alliance_id=toInteger(victim_alliance_id), k.victim_faction_id=toInteger(victim_faction_id), k.damage_taken=toInteger(damage_taken)


MERGE (cv:character {character_id: victim_id})
MATCH (s:system {system_id: system_id})
MERGE (cv)-[:VICTIM]->(k)-[:HAPPENED_IN]->(s)

MATCH (k:killmail {killmail_id:killmail_id})
MERGE (ca:character {character_id: attacker_id})
MERGE (ca)-[a:ATTACKER]->(k)
SET a.corporation_id=toInteger(corporation_id), a.alliance_id=toInteger(alliance_id), a.faction_id=toInteger(faction_id), a.damage_done=toInteger(a.damage_done), a.final_blow=final_blow, a.security_status=toFloat(security_status), a.ship_type_id=toInteger(ship_type_id), a.weapon_type_id=toInteger(weapon_type_id)







WITH "https://esi.evetech.net/latest/killmails/73309886/5014d3f4f8390f4620807aa7f91bdd5498e4957c/" as url
CALL apoc.load.json