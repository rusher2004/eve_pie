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






MATCH (a:character)-[at:ATTACKER]->(k:killmail)<-[:VICTIM]-(v:character)
WITH a,at,k LIMIT 50
MERGE (a)-[nat:ATTACKER]->(an:attacker :character_attacker)-[:ATTACKED]->(k)
SET an.attacker_id=a.character_id, an.killmail_id=k.killmail_id, an.corporation_id=at.corporation_id, an.alliance_id=at.alliance_id, an.faction_id=at.faction_id, an.damage_done=at.damage_done, an.final_blow=at.final_blow, an.security_status=at.security_status, an.ship_type_id=at.ship_type_id, an.weapon_type_id=at.weapon_type_id
RETURN *


#Attackers
MATCH (c:character {character_id: 91418572})-[v:VICTIM]->(k)<-[at:ATTACKED]-(a)
RETURN {
attacker_id: a.attacker_id,
attacks: count(DISTINCT at)
} as stats
ORDER BY stats.attacks DESC LIMIT 3



MATCH (c:character {character_id: 91418572})-[v:VICTIM]->(k)<-[at:ATTACKED]-(a)
WITH {
attacker_id: a.attacker_id,
attacks: count(DISTINCT at)
} as stats, c
ORDER BY stats.attacks DESC LIMIT 3
CREATE (tp:top_attacker {attacker_id: stats.attacker_id, attacks: stats.attacks})
CREATE (tp)-[:top_attacker]->(c)
RETURN {
attacker_id: tp.attacker_id,
attacks: tp.attacks
} as new_stats
ORDER BY new_stats.attacks DESC







#Victims
MATCH (c:character {character_id: 91817438})
MATCH (c)-[]->(at:attacker)-[ak:ATTACKED]->(k)<-[v:VICTIM]-(d:character)
RETURN {
victim_id: d.character_id,
attacks: count(at)
} as stats
ORDER BY stats.attacks DESC LIMIT 3






MATCH (c:character {name: 'Fungus Amongus'})
MATCH (c)-[a]->(k:killmail)<-[b]-(d:character)
RETURN {
name: d.name,
id: d.character_id,
victim: count(CASE WHEN type(b) = 'VICTIM' THEN a ELSE NULL END)
} as stats
ORDER BY stats.victim DESC LIMIT 3
