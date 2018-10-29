//Create Indexes
CREATE INDEX ON :region(region_id);
CREATE INDEX ON :constellation(constellation_id);
CREATE INDEX ON :system(system_id);
CREATE INDEX ON :planet(planet_id);
CREATE INDEX ON :moon(moon_id);
CREATE INDEX ON :item(item_id);

//Create Nodes

//Regions
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapRegions.csv" AS row
MERGE (:region {region_id: toInteger(row.regionID), name: row.regionName, x: row.x, y: row.y, z: row.z, xMin: row.xMin, xMax: row.xMax, yMin: row.yMin, yMax: row.yMax, zMin: row.zMin, zMax: row.zMax, faction_id: toInteger(row.factionID), radius: toInteger(row.radius)});

//Constellations
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapConstellations.csv" AS row
MERGE (:constellation {region_id: toInteger(row.regionID), constellation_id: toInteger(row.constellationID), name: row.constellationName, x: row.x, y: row.y, z: row.z, xMin: row.xMin, xMax: row.xMax, yMin: row.yMin, yMax: row.yMax, zMin: row.zMin, zMax: row.zMax, faction_id: toInteger(row.factionID), radius: toInteger(row.radius)});

//Systems
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/mapSolarSystems.csv" AS row
MERGE (:system {region_id: toInteger(row.regionID), constellation_id: toInteger(row.constellationID), system_id: toInteger(row.solarSystemID), name: row.solarSystemName, x: row.x, y: row.y, z: row.z, xMin: row.xMin, xMax: row.xMax, yMin: row.yMin, y: row.yMax, zMin: row.zMin, zMax: row.zMax, luminosity: toFloat(row.luminosity), border: toInteger(row.border), fringe: toInteger(row.fringe), corridor: toInteger(row.corridor), hub: toInteger(row.hub), international: toInteger(row.international), regional: toInteger(row.regional), constellation: toInteger(row.constellation), security: toFloat(row.security), faction_id: toInteger(row.factionID), radius: toInteger(row.radius), sun_type_id: toInteger(row.sunTypeID), security_class: row.securityClass});

//Planets
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///csv/sde/planets_only.csv" AS row
MERGE (:planet {planet_id: toInteger(row.itemID), type_id: toInteger(row.typeID), system_id: toInteger(row.solarSystemID), constellation_id: toInteger(row.constellationID), region_id: toInteger(row.regionID), orbit_id: toInteger(row.orbitID), x: row.x, y: row.y, z: row.z, radius: toInteger(row.radius), name: row.itemName, security: toFloat(row.security), celestial_index: toInteger(row.celestialIndex), orbit_index: toInteger(row.orbitIndex)});

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
MERGE (:item {item_id: toInteger(row.typeID), group_id: toInteger(row.groupID), name: row.typeName, description: row.description, mass: toFloat(row.mass), volume: toFloat(row.volume), capacity: toFloat(row.capacity), portion_size: toInteger(row.portionSize), race_id: toInteger(row.raceID), base_price: toInteger(row.basePrice), published: toInteger(row.published), market_group_id: toInteger(row.marketGroupID), icon_id: toInteger(row.iconID), sound_id: toInteger(row.soundID), graphic_id: toInteger(row.graphicID)});

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

