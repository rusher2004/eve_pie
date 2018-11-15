# Attackers

class Queries:

    def get_character_attackers(tx, victim_id):
        res = tx.run("MATCH (c:character {character_id: " + str(victim_id) + "})-[v:VICTIM]->(k)<-[at:ATTACKED]-(a:character_attacker)\n" \
                    + "RETURN {\n" \
                    + "attacker_id: a.attacker_id,\n" \
                    + "attacks: count(DISTINCT at)\n" \
                    + "} as stats\n" \
                    + "ORDER BY stats.attacks DESC LIMIT 3")
        return res

    def get_character_victims(tx, attacker_id):
        res = tx.run("MATCH (c:character {character_id: " + str(attacker_id) + "})\n" \
                    + "MATCH (c)-[]->(at:attacker)-[ak:ATTACKED]->(k)<-[v:VICTIM]-(d:character)\n" \
                    + "RETURN {\n" \
                    + "victim_id: d.character_id,\n" \
                    + "attacks: count(at)\n" \
                    + "} as stats\n" \
                    + "ORDER BY stats.attacks DESC LIMIT 3")
        return res
