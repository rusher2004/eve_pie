import db_queries as dbq
import csv

driver = dbq.driver
write_region = dbq.write_region
write_constellation = dbq.write_constellation
write_system = dbq.write_system
write_planet = dbq.write_planet
write_moon = dbq.write_moon

with driver.session() as session:
    with open('csv/mapRegions.csv') as region_file:
        readCSV = csv.reader(region_file, delimiter = ',')
        for row in readCSV:
            region_id = int(row[0])
            region_name = row[1]

            print('writing region: ' + str(region_id) + ' ' + region_name)

            session.write_transaction(write_region, region_id, region_name)

    with open('csv/mapConstellations.csv') as constellation_file:
        readCSV = csv.reader(constellation_file, delimiter = ',')
        for row in readCSV:
            region_id = int(row[0])
            constellation_id = int(row[1])
            constellation_name = row[2]

            print('writing constellation: ' + str(constellation_id) + ' ' + constellation_name)

            session.write_transaction(write_constellation, constellation_id, constellation_name, region_id)

    with open('csv/mapSolarSystems.csv') as system_file:
        readCSV = csv.reader(system_file, delimiter = ',')
        for row in readCSV:
            constellation_id = int(row[1])
            system_id = int(row[2])
            system_name = row[3]
            sec_status = float(row[21])

            print('writing system: ' + str(system_id) + ' ' + system_name)

            session.write_transaction(write_system, system_id, system_name, constellation_id, sec_status)

    with open('csv/planets_only.csv') as planet_file:
        readCSV = csv.reader(planet_file, delimiter = ',')
        for row in readCSV:
            planet_id = int(row[0])
            type_id = int(row[1])
            system_id = int(row[3])
            planet_name = row[11]
            celestial_index = int(row[13])

            print('writing planet: ' + str(planet_id) + ' ' + planet_name)

            session.write_transaction(write_planet, planet_id, type_id, system_id, planet_name, celestial_index)

    with open('csv/moons_only.csv') as moon_file:
        readCSV = csv.reader(moon_file, delimiter = ',')
        for row in readCSV:
            moon_id = int(row[0])
            type_id = int(row[1])
            system_id = int(row[3])
            orbit_id = int(row[6])
            moon_name = row[11]
            celestial_index = int(row[13])
            orbit_index = int(row[14])

            print('writing moon: ' + str(moon_id) + ' ' + moon_name)

            session.write_transaction(write_moon, moon_id, type_id, system_id, orbit_id, moon_name, celestial_index, orbit_index)
