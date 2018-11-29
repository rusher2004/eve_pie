class Queries:

    def get_character_demos(tx, character_id):
        time_limit = 86400000
        c = "c:c"
        res_props = """
            character_id: results.c.character_id,
            alliance_id: results.c.alliance_id,
            ancestry_id: results.c.ancestry_id,
            birthday: results.c.birthday,
            bloodline_id: results.c.bloodline_id,
            corporation_id: results.c.corporation_id,
            description: results.c.description,
            faction_id: results.c.faction_id,
            gender: results.c.gender,
            name: results.c.name,
            race_id: results.c.race_id,
            security_status: results.c.security_status
        """
        query_string = f"""
            MERGE (c:character {{character_id: {character_id}}})
            WITH c, (CASE WHEN c.demos_timestamp IS NULL THEN false WHEN timestamp() - c.demos_timestamp < {time_limit} THEN true ELSE false END) as bool
            CALL apoc.do.when(bool, "RETURN c", "CALL apoc.load.json('https://esi.evetech.net/latest/characters/{character_id}') YIELD value as n RETURN n",{{{c}}}) YIELD value as val
            WITH c, c.character_id as char_id, (val.n IS NULL) as bool2, (CASE WHEN val.n IS NOT NULL THEN val.n ELSE c END) as props
            SET c = props, c.character_id = char_id
            WITH c, bool2, props
            CALL apoc.do.when(bool2, "RETURN c","SET c.demos_timestamp = timestamp() RETURN c",{{{c}}}) YIELD value as results
            RETURN {{{res_props}}} as char
        """
        res = tx.run(query_string)
        return res

    def get_character_attackers(tx, victim_id):
        time_limit = 86400000
        res = tx.run("MATCH (c:character {character_id: " + str(victim_id) + "})\n" \
                    + "WITH c\n" \
                    + "CALL apoc.do.when(c.attacker_timestamp IS NULL, 'MATCH (c)-[v:VICTIM]->(k)<-[at:ATTACKED]-(a:character_attacker) WITH { attacker_id: a.attacker_id, attacks: count(DISTINCT at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_attacker {attacker_id: pre_stats.attacker_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_ATTACKER]->(c) SET c.attacker_timestamp = timestamp() RETURN c', 'RETURN c', {c:c}) YIELD value as cee\n" \
                    + "WITH c, ((timestamp() - c.attacker_timestamp) > " + str(time_limit) + ") as bool\n" \
                    + "CALL apoc.do.when(bool, 'MATCH (c)<-[:TOP_ATTACKER]-(d:top_attacker) DETACH DELETE d WITH c MATCH (c)-[v:VICTIM]->(k)<-[at:ATTACKED]-(a:character_attacker) WITH { attacker_id: a.attacker_id, attacks: count(DISTINCT at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_attacker {attacker_id: pre_stats.attacker_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_ATTACKER]->(c) SET c.attacker_timestamp = timestamp() RETURN { attacker_id: tp.attacker_id, attacks: tp.attacks } as stats ORDER BY stats.attacks DESC', 'MATCH (c)<-[:TOP_ATTACKER]-(d:top_attacker) RETURN { attacker_id: d.attacker_id, attacks: d.attacks } as stats ORDER BY stats.attacks DESC', {c:c}) YIELD value as stats\n" \
                    + "RETURN stats")
        return res

    def get_character_victims(tx, attacker_id):
        time_limit = 86400000
        res = tx.run("MATCH (c:character {character_id: " + str(attacker_id) + "})\n" \
                    + "WITH c\n" \
                    + "CALL apoc.do.when(c.victim_timestamp IS NULL, 'MATCH (c)-[]->(at:attacker)-[ak:ATTACKED]->(k)<-[v:VICTIM]-(d:character) WITH { victim_id: d.character_id, attacks: count(at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_victim {victim_id: pre_stats.victim_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_VICTIM]->(c) SET c.victim_timestamp = timestamp() RETURN c', 'RETURN c', {c:c}) YIELD value as cee\n" \
                    + "WITH c, ((timestamp() - c.victim_timestamp) > " + str(time_limit) + ") as bool\n" \
                    + "CALL apoc.do.when(bool, 'MATCH (c)<-[:TOP_VICTIM-(d:top_victim) DETACH DELETE D WITH c MATCH (c)-[]->(at:attacker)-[ak:ATTACKED]->(k)<-[v:VICTIM]-(d:character) WITH { victim_id: d.character_id, attacks: count(at) } as pre_stats, c ORDER BY pre_stats.attacks DESC LIMIT 3 CREATE (tp:top_victim {victim_id: pre_stats.victim_id, attacks: pre_stats.attacks}) CREATE (tp)-[:TOP_VICTIM]->(c) SET c.victim_timestamp = timestamp() RETURN { victim_id: tp.victim_id, attacks: tp.attacks } as stats ORDER BY stats.attacks DESC', 'MATCH (c)<-[:TOP_VICTIM]-(d:top_victim) RETURN { victim_id: d.victim_id, attacks: d.attacks } as stats ORDER BY stats.attacks DESC', {c:c}) YIELD value as stats\n" \
                    + "RETURN stats")
        return res

    def get_corporation_demos(tx, corporation_id):
        time_limit = 86400000
        c = "c:c"
        res_props = """
            corporation_id: results.c.corporation_id,
            alliance_id: results.c.alliance_id,
            ceo_id: results.c.ceo_id,
            description: results.c.description,
            faction_id: results.c.faction_id,
            name: results.c.name,
            ticker: results.c.ticker
        """
        query_string = f"""
            MERGE (c:corporation {{corporation_id: {corporation_id}}})
            WITH c, (CASE WHEN c.demos_timestamp IS NULL THEN false WHEN timestamp() - c.demos_timestamp < {time_limit} THEN true ELSE false END) as bool
            CALL apoc.do.when(bool, "RETURN c", "CALL apoc.load.json('https://esi.evetech.net/latest/corporations/{corporation_id}') YIELD value as n RETURN n",{{{c}}}) YIELD value as val
            WITH c, c.corporation_id as corp_id, (val.n IS NULL) as bool2, (CASE WHEN val.n IS NOT NULL THEN val.n ELSE c END) as props
            SET c = props, c.corporation_id = corp_id
            WITH c, bool2, props
            CALL apoc.do.when(bool2, "RETURN c","SET c.demos_timestamp = timestamp() RETURN c",{{{c}}}) YIELD value as results
            RETURN {{{res_props}}} as corp
        """
        res = tx.run(query_string)
        return res

    def get_alliance_demos(tx, alliance_id):
        time_limit = 86400000
        a = "a:a"
        res_props = """
            alliance_id: results.a.alliance_id,
            executor_corporation_id: results.a.executor_corporation_id,
            faction_id: results.a.faction_id,
            name: results.a.name,
            ticker: results.a.ticker
        """
        query_string = f"""
            MERGE (a:alliance {{alliance_id: {alliance_id}}})
            WITH a, (CASE WHEN a.demos_timestamp IS NULL THEN false WHEN timestamp() - a.demos_timestamp < {time_limit} THEN true ELSE false END) as bool
            CALL apoc.do.when(bool, "RETURN a", "CALL apoc.load.json('https://esi.evetech.net/latest/alliances/{alliance_id}') YIELD value as n RETURN n",{{{a}}}) YIELD value as val
            WITH a, a.alliance_id as alli_id, (val.n IS NULL) as bool2, (CASE WHEN val.n IS NOT NULL THEN val.n ELSE a END) as props
            SET a = props, a.alliance_id = alli_id
            WITH a, bool2, props
            CALL apoc.do.when(bool2, "RETURN a","SET a.demos_timestamp = timestamp() RETURN a",{{{a}}}) YIELD value as results
            RETURN {{{res_props}}} as alliance
        """
        res = tx.run(query_string)
        return res
