# Attackers

class Queries:

    def get_character_attackers(tx, victim_id):
        time_limit = int(86400000)
        res = tx.run("MATCH (c:character {character_id: " + str(victim_id) + "})\n" \
                    + "WITH c\n" \
                    + "CALL apoc.do.when(c.attacker_timestamp IS NULL, 'MATCH (c)-[v:VICTIM]->(k)<-[at:ATTACKED]-(a:character_attacker) WITH { attacker_id: a.attacker_id, attacks: count(DISTINCT at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_attacker {attacker_id: pre_stats.attacker_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_ATTACKER]->(c) SET c.attacker_timestamp = timestamp() RETURN c', 'RETURN c', {c:c}) YIELD value as cee\n" \
                    + "WITH c, ((timestamp() - c.attacker_timestamp) > " + str(time_limit) + ") as bool\n" \
                    + "CALL apoc.do.when(bool, 'MATCH (c)<-[:TOP_ATTACKER]-(d:top_attacker) DETACH DELETE d WITH c MATCH (c)-[v:VICTIM]->(k)<-[at:ATTACKED]-(a:character_attacker) WITH { attacker_id: a.attacker_id, attacks: count(DISTINCT at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_attacker {attacker_id: pre_stats.attacker_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_ATTACKER]->(c) SET c.attacker_timestamp = timestamp() RETURN { attacker_id: tp.attacker_id, attacks: tp.attacks } as stats ORDER BY stats.attacks DESC', 'MATCH (c)<-[:TOP_ATTACKER]-(d:top_attacker) RETURN { attacker_id: d.attacker_id, attacks: d.attacks } as stats ORDER BY stats.attacks DESC', {c:c}) YIELD value as stats\n" \
                    + "RETURN stats")
        return res

    def get_character_victims(tx, attacker_id):
        time_limit = int(86400000)
        res = tx.run("MATCH (c:character {character_id: " + str(attacker_id) + "})\n" \
                    + "WITH c\n" \
                    + "CALL apoc.do.when(c.victim_timestamp IS NULL, 'MATCH (c)-[]->(at:attacker)-[ak:ATTACKED]->(k)<-[v:VICTIM]-(d:character) WITH { victim_id: d.character_id, attacks: count(at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_victim {victim_id: pre_stats.victim_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_VICTIM]->(c) SET c.victim_timestamp = timestamp() RETURN c', 'RETURN c', {c:c}) YIELD value as cee\n" \
                    + "WITH c, ((timestamp() - c.victim_timestamp) > " + str(time_limit) + ") as bool\n" \
                    + "CALL apoc.do.when(bool, 'MATCH (c)<-[:TOP_VICTIM-(d:top_victim) DETACH DELETE D WITH c MATCH (c)-[]->(at:attacker)-[ak:ATTACKED]->(k)<-[v:VICTIM]-(d:character) WITH { victim_id: d.character_id, attacks: count(at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_victim {victim_id: pre_stats.victim_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_VICTIM]->(c) SET c.victim_timestamp = timestamp() RETURN { victim_id: tp.victim_id, attacks: tp.attacks } as stats ORDER BY stats.attacks DESC', 'MATCH (c)<-[:TOP_VICTIM]-(d:top_victim) RETURN { victim_id: d.victim_id, attacks: d.attacks } as stats ORDER BY stats.attacks DESC', {c:c}) YIELD value as stats\n" \
                    + "RETURN stats")
        return res
