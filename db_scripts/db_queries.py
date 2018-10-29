from neo4j.v1 import GraphDatabase as gd
import csv

driver = gd.driver("bolt://localhost:7687", auth=("neo4j", "notneo4j"))

#Universe
def write_region(tx, region, name):
    tx.run("MERGE (r:region {region_id: $region_id, name: $name})",
           region_id=region, name=name)

def write_constellation(tx, constellation, name, region):
    tx.run("MERGE (r:region {region_id: $region_id}) MERGE (c:constellation {constellation_id: $constellation_id, name: $constellation_name}) MERGE (c)-[:CONSTELLATION_IN]->(r)",
           region_id=region, constellation_id=constellation, constellation_name=name)

def write_system(tx, system, name, constellation, sec_status):
    tx.run("MERGE (c:constellation {constellation_id: $constellation_id}) MERGE (s:system {system_id: $system_id, name: $system_name, security_status: $security_status}) MERGE (s)-[:SYSTEM_IN]->(c)",
           constellation_id=constellation, system_id=system, system_name=name, security_status=sec_status)

def write_planet(tx, planet, type_id, system, name, celestial_index):
    tx.run("MERGE (s:system {system_id: $system_id}) MERGE (p:planet {planet_id: $planet_id, name: $planet_name, type_id: $type_id, celestial_index: $celestial_index}) MERGE (p)-[:PLANET_IN]->(s)",
           planet_id=planet, type_id=type_id, system_id=system, planet_name=name, celestial_index=celestial_index)

def write_moon(tx, moon_id, type_id, system_id, orbit_id, moon_name, celestial_index, orbit_index):
	tx.run("MATCH (p:planet {celestial_index: $celestial_index})-[:PLANET_IN]-(s:system {system_id: $system_id}) WITH p,s MERGE (m:moon {moon_id: $moon_id, type_id: $type_id, orbit_id: $orbit_id, name: $moon_name, orbit_index: $orbit_index}) MERGE (p)<-[:ORBITS]-(m)-[:MOON_IN]->(s)",
			moon_id=moon_id, type_id=type_id, system_id=system_id, orbit_id=orbit_id, moon_name=moon_name, celestial_index=celestial_index, orbit_index=orbit_index)

#PI Schematics
def write_schematic(tx, schematic, name, time):
	tx.run("MERGE (s:schematic {schematic_id: $schematic, name: $name, cycle_time: $time})",
			schematic=schematic, name=name, time=time)

def write_schematic_map(tx, schematic, item_type, quant, input):
	if input:
		tx.run("MATCH (s:pi_schematic {schematic_id: $schematic}) MATCH (i:item {item_id: $item_type}) MERGE (i)-[:INPUTS {quantity: $quant}]->(s)",
				schematic=schematic, item_type=item_type, quant=quant)
	else:
		tx.run("MATCH (s:pi_schematic {schematic_id: $schematic}) MATCH (i:item {item_id: $item_type}) MERGE (s)-[:OUTPUTS {quantity: $quant}]->(i)",
				schematic=schematic, item_type=item_type, quant=quant)

#Items
def write_item(tx, type_id, group_id, name, desc, portion_size, race_id, published, market_group, icon_id, graphic_id):
	tx.run("MERGE (i:item {type_id: $type_id}) WITH i SET i.group_id=$group_id, i.name=$name, i.description=$desc, i.portion_size=$portion_size, i.race_id=$race_id, i.published=$published, i.market_group=$market_group, i.icon_id=$icon_id, i.graphic_id=$graphic_id",
			type_id=type_id, group_id=group_id, name=name, desc=desc, portion_size=portion_size, race_id=race_id, published=published, market_group=market_group, icon_id=icon_id, graphic_id=graphic_id)

#Entities
def write_alliance_ids(tx, alliance_id):
    tx.run("MERGE (a:alliance {alliance_id: $alliance_id}) RETURN a",
    alliance_id=alliance_id)

def alliances_without_names_db_query(tx):
    res = tx.run("MATCH (a:alliance) WHERE a.name IS NULL RETURN a LIMIT 100")
    return res

def write_alliance_names(tx, id, name):
    tx.run("MATCH (a:alliance {alliance_id: $id}) SET a.name=$name RETURN a",
        id=id, name=name)    

#Meta
def get_labels(tx):
	res = tx.run("CALL db.labels")
	return res

def write_index(tx, label, unique, constraint):
	if unique:
		query = "CREATE CONSTRAINT ON (label:" + label + ") ASSERT " + label + "." + constraint + " IS UNIQUE"
	else:
		query = "CREATE INDEX ON :" + label + "(" + label + "_id)"

	tx.run(query)
