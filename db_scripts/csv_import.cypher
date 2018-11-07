//Create Indexes and Constraints
CREATE CONSTRAINT ON (n:region) ASSERT n.region_id IS UNIQUE;
CREATE CONSTRAINT ON (n:constellation) ASSERT n.constellation_id IS UNIQUE;
CREATE CONSTRAINT ON (n:system) ASSERT n.system_id IS UNIQUE;
CREATE CONSTRAINT ON (n:planet) ASSERT n.planet_id IS UNIQUE;
CREATE CONSTRAINT ON (n:moon) ASSERT n.moon_id IS UNIQUE;
CREATE CONSTRAINT ON (n:item) ASSERT n.item_id IS UNIQUE;
CREATE CONSTRAINT ON (n:station) ASSERT n.station_id IS UNIQUE;
CREATE CONSTRAINT ON (n:character) ASSERT n.character_id IS UNIQUE;
CREATE CONSTRAINT ON (n:corporation) ASSERT n.corporation_id IS UNIQUE;
CREATE CONSTRAINT ON (n:alliance) ASSERT n.alliance_id IS UNIQUE;
CREATE CONSTRAINT ON (n:faction) ASSERT n.faction_id IS UNIQUE;
CREATE CONSTRAINT ON (n:killmail) ASSERT n.killmail_id IS UNIQUE;

//Create Nodes

//Regions
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapRegions.csv" AS row
MERGE (r:region {region_id: toInteger(row.regionID), name: row.regionName, x: row.x, y: row.y, z: row.z, xMin: row.xMin, xMax: row.xMax, yMin: row.yMin, yMax: row.yMax, zMin: row.zMin, zMax: row.zMax})
FOREACH(nothing in CASE WHEN trim(row.factionID) <> "" THEN [1] ELSE [] END | SET r.faction_id = toInteger(row.factionID));

//Constellations
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapConstellations.csv" AS row
MERGE (c:constellation {region_id: toInteger(row.regionID), constellation_id: toInteger(row.constellationID), name: row.constellationName, x: row.x, y: row.y, z: row.z, xMin: row.xMin, xMax: row.xMax, yMin: row.yMin, yMax: row.yMax, zMin: row.zMin, zMax: row.zMax})
FOREACH(nothing in CASE WHEN trim(row.factionID) <> "" THEN [1] ELSE [] END | SET c.faction_id = toInteger(row.factionID));

//Systems
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapSolarSystems.csv" AS row
MERGE (s:system {region_id: toInteger(row.regionID), constellation_id: toInteger(row.constellationID), system_id: toInteger(row.solarSystemID), name: row.solarSystemName, x: row.x, y: row.y, z: row.z, xMin: row.xMin, xMax: row.xMax, yMin: row.yMin, y: row.yMax, zMin: row.zMin, zMax: row.zMax, luminosity: toFloat(row.luminosity), border: toInteger(row.border), fringe: toInteger(row.fringe), corridor: toInteger(row.corridor), hub: toInteger(row.hub), international: toInteger(row.international), regional: toInteger(row.regional), security: toFloat(row.security), radius: toInteger(row.radius)})
FOREACH(nothing in CASE WHEN trim(row.factionID) <> "" THEN [1] ELSE [] END | SET s.faction_id = toInteger(row.factionID))
FOREACH(nothing in CASE WHEN trim(row.securityClass) <> "" THEN [1] ELSE [] END | SET s.security_class = row.securityClass)
FOREACH(nothing in CASE WHEN trim(row.sunTypeID) <> "" THEN [1] ELSE [] END | SET s.sun_type_id = toInteger(row.sunTypeID));

//Planets
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/planets_only.csv" AS row
MERGE (p:planet {planet_id: toInteger(row.itemID), type_id: toInteger(row.typeID), system_id: toInteger(row.solarSystemID), constellation_id: toInteger(row.constellationID), region_id: toInteger(row.regionID), orbit_id: toInteger(row.orbitID), x: row.x, y: row.y, z: row.z, radius: toInteger(row.radius), name: row.itemName, security: toFloat(row.security), celestial_index: toInteger(row.celestialIndex)})
FOREACH(nothing in CASE WHEN trim(row.orbitID) <> "" THEN [1] ELSE [] END | SET p.orbit_index = toInteger(row.orbitID));

//Moons
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/moons_only.csv" AS row
MERGE (:moon {moon_id: toInteger(row.itemID), type_id: toInteger(row.typeID), system_id: toInteger(row.solarSystemID), constellation_id: toInteger(row.constellationID), region_id: toInteger(row.regionID), orbit_id: toInteger(row.orbitID), x: row.x, y: row.y, z: row.z, radius: toInteger(row.radius), name: row.itemName, security: toFloat(row.security), celestial_index: toInteger(row.celestialIndex), orbit_index: toInteger(row.orbitIndex)});

//Stations
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/staStations.csv" AS row
MERGE (:station {station_id: toInteger(row.stationID), security: toFloat(row.security), docking_cost_per_volume: toFloat(row.dockingCostPerVolume), max_ship_volume: toInteger(row.maxShipVolumeDockable), office_rental_cost: toFloat(row.officeRentalCost), operation_id: toInteger(row.operationID), station_type_id: toInteger(row.stationTypeID), corporation_id: toInteger(row.corporationID), system_id: toInteger(row.solarSystemID), constellation_id: toInteger(row.constellationID), region_id: toInteger(row.regionID), name: row.stationName, x: toInteger(row.x), y: toInteger(row.y), z: toInteger(row.z),	reprocessing_efficiency: toFloat(row.reprocessingEfficiency), reprocessing_station_take: toFloat(row.reprocessingStationsTake), reprocessing_hangar_flag: toInteger(row.reprocessingHangarFlag)});

//Station Services
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/staServices.csv" AS row
MERGE (ss:station_service {service_id: toInteger(row.serviceID), name: row.serviceName})
ON CREATE SET ss.description = row.description
ON MATCH SET ss.description = row.description;

//Station Operations
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/staOperations.csv" AS row
MERGE (so:station_operation {operation_id: toInteger(row.operationID)})
ON CREATE SET so.activity_id=toInteger(row.activityID), so.operation_name=row.operationName, so.description=row.description, so.fringe=toInteger(row.fringe), so.corridor=toInteger(row.corridor), so.hub=toInteger(row.hub), so.border=toInteger(row.border), so.ratio=toInteger(row.ratio), so.caldari_station_type_id=toInteger(row.caldariStationTypeID), so.minmatar_station_type_id=toInteger(row.minmatarStationTypeID), so.amarr_station_type_id=toInteger(row.amarrStationTypeID), so.gallente_station_type_id=toInteger(row.gallenteStationTypeID), so.jove_station_type_id=toInteger(row.joveStationTypeID)
ON MATCH SET so.activity_id=toInteger(row.activityID), so.operation_name=row.operationName, so.description=row.description, so.fringe=toInteger(row.fringe), so.corridor=toInteger(row.corridor), so.hub=toInteger(row.hub), so.border=toInteger(row.border), so.ratio=toInteger(row.ratio), so.caldari_station_type_id=toInteger(row.caldariStationTypeID), so.minmatar_station_type_id=toInteger(row.minmatarStationTypeID), so.amarr_station_type_id=toInteger(row.amarrStationTypeID), so.gallente_station_type_id=toInteger(row.gallenteStationTypeID), so.jove_station_type_id=toInteger(row.joveStationTypeID);

//Station Operations Services
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/staOperationServices.csv" AS row
MATCH (so:station_operation {operation_id: toInteger(row.operationID)})
MATCH (ss:station_service {service_id: toInteger(row.serviceID)})
MERGE (ss)-[:SERVICES]->(so);

//Items
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/invTypes.csv" AS row
MERGE (i:item {item_id: toInteger(row.typeID), group_id: toInteger(row.groupID), mass: toFloat(row.mass), volume: toFloat(row.volume), capacity: toFloat(row.capacity), portion_size: toInteger(row.portionSize), published: toInteger(row.published), graphic_id: toInteger(row.graphicID)})
FOREACH(nothing in CASE WHEN trim(row.name) <> "" THEN [1] ELSE [] END | SET i.name = row.name)
FOREACH(nothing in CASE WHEN trim(row.description) <> "" THEN [1] ELSE [] END | SET i.description = row.description)
FOREACH(nothing in CASE WHEN trim(row.raceID) <> "" THEN [1] ELSE [] END | SET i.race_id = toInteger(row.raceID))
FOREACH(nothing in CASE WHEN trim(row.basePrice) <> "" THEN [1] ELSE [] END | SET i.base_price = toInteger(row.basePrice))
FOREACH(nothing in CASE WHEN trim(row.marketGroupID) <> "" THEN [1] ELSE [] END | SET i.market_group_id = toInteger(row.marketGroupID))
FOREACH(nothing in CASE WHEN trim(row.iconID) <> "" THEN [1] ELSE [] END | SET i.icon_id = toInteger(row.iconID))
FOREACH(nothing in CASE WHEN trim(row.soundID) <> "" THEN [1] ELSE [] END | SET i.sound_id = toInteger(row.soundID));

//PI Schematics
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/planetSchematics.csv" AS row
MERGE (:pi_schematic {schematic_id: toInteger(row.schematicID), name: row.schematicName, cycle_time: toInteger(row.cycleTime)});

//Create Relationships

//Constellations to Regions
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapConstellations.csv" AS row
MATCH (c:constellation {constellation_id: toInteger(row.constellationID)})
MATCH (r:region {region_id: toInteger(row.regionID)})
MERGE (c)-[:CONSTELLATION_IN]->(r);

//Systems to Constellations
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapSolarSystems.csv" AS row
MATCH (s:system {system_id: toInteger(row.solarSystemID)})
MATCH (c:constellation {constellation_id: toInteger(row.constellationID)})
MERGE (s)-[:SYSTEM_IN]->(c);

//Planets to Systems
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/planets_only.csv" AS row
MATCH (p:planet {planet_id: toInteger(row.itemID)})
MATCH (s:system {system_id: toInteger(row.solarSystemID)})
MERGE (p)-[:PLANET_IN]->(s);

//Moons to Planets and Systems
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/moons_only.csv" AS row
MATCH (m:moon {moon_id: toInteger(row.itemID)})
MATCH (s:system {system_id: toInteger(row.solarSystemID)})
MATCH (p:planet {celestial_index: toInteger(row.celestialIndex)})-[:PLANET_IN]->(s)
MERGE (p)<-[:ORBITS]-(m)-[:MOON_IN]->(s);

//Stations to Systems and Operations
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/staStations.csv" AS row
MATCH (st:station {station_id: toInteger(row.stationID)})
MATCH (sy:system {system_id: toInteger(row.solarSystemID)})
MATCH (so:station_operation {operation_id: toInteger(row.operationID)})
MERGE (so)-[:OPERATES]->(st)-[:STATION_IN]->(sy);

