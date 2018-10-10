from neo4j.v1 import GraphDatabase as gd
import csv

driver = gd.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))

def create_region(tx, region, name):
    tx.run("MERGE (r:region {region_id: $region_id, name: $name})",
           region_id=region, name=name)

def create_constellation(tx, constellation, name, region):
    tx.run("MERGE (r:region {region_id: $region_id}) MERGE (c:constellation {constellation_id: $constellation_id, name: $constellation_name}) MERGE (c)-[:CONSTELLATION_IN]->(r)",
           region_id=region, constellation_id=constellation, constellation_name=name)

def create_system(tx, system, name, constellation, sec_status):
    tx.run("MERGE (c:constellation {constellation_id: $constellation_id}) MERGE (s:system {system_id: $system_id, name: $system_name, security_status: $security_status}) MERGE (s)-[:SYSTEM_IN]->(c)",
           constellation_id=constellation, system_id=system, system_name=name, security_status=sec_status)

def create_planet(tx, planet, name, region):
    tx.run("MERGE (s:system {system_id: $system_id}) MERGE (p:planet {planet_id: $planet_id, name: $planet_name, type_id: $type_id, celestial_index: $celestial_index}) MERGE (p)-[:PLANET_IN]->(s)",
           system_id=system, planet_id=planet, planet_name=name)

with open('mapRegions.csv') as region_file:
    readCSV = csv.reader(region_file, delimiter=',')
    for row in readCSV:
        region_id = int(row[0])
        region_name = row[1]

        print('writing region: ' region_id + ' ' + region_name)

        with driver.session() as session:
            session.write_transaction(create_region, region_id, region_name)

with open('mapConstellations.csv') as constellation_file:
    readCSV = csv.reader(constellation_file, delimiter=',')
    for row in readCSV:
        region_id = int(row[0])
        constellation_id = int(row[1])
        constellation_name = row[2]

        print('writing constellation: ' constellation_id + ' ' + constellation_name)

        with driver.session() as session:
            session.write_transaction(create_constellation, constellation_id, constellation_name, region_id)

with open('mapSolarSystems.csv') as system_file:
    readCSV = csv.reader(system_file, delimiter=',')
    for row in readCSV:
        constellation_id = int(row[1])
        system_id = int(row[2])
        system_name = row[3]
        sec_status = float(row[21])

        print('writing system: ' system_id + ' ' + system_name)

        with driver.session() as session:
            session.write_transaction(create_system, system_id, system_name, constellation_id, sec_status)

with open('planet.csv') as planet_file:
    readCSV = csv.reader(planet_file, delimiter='')
    for row in readCSV:
        planet_id = int(row[0])
        type_id = int(row[1])
        system_id = int(row[3])
        planet_name = row[11]
        celestial_index = int(row[13])

        print('writing planet: ' planet_id + ' ' + planet_name)

        with driver.sesstion() as session:
            session.write_transaction(create_planet, planet_id, type_id, system_id, planet_name, celestial_index)