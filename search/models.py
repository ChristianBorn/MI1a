import re
from django.db import models


class PlanetOsmLine(models.Model):
    osm_id = models.BigIntegerField(primary_key='osm_id', blank=True)
    access = models.TextField(blank=True, null=True)
    addr_housename = models.TextField(db_column='addr:housename', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_housenumber = models.TextField(db_column='addr:housenumber', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_street = models.TextField(db_column='addr:street', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_postcode = models.TextField(db_column='addr:postcode', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_city = models.TextField(db_column='addr:city', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_interpolation = models.TextField(db_column='addr:interpolation', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    admin_level = models.TextField(blank=True, null=True)
    aerialway = models.TextField(blank=True, null=True)
    aeroway = models.TextField(blank=True, null=True)
    amenity = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    barrier = models.TextField(blank=True, null=True)
    bicycle = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    bridge = models.TextField(blank=True, null=True)
    boundary = models.TextField(blank=True, null=True)
    building = models.TextField(blank=True, null=True)
    construction = models.TextField(blank=True, null=True)
    covered = models.TextField(blank=True, null=True)
    culvert = models.TextField(blank=True, null=True)
    cutting = models.TextField(blank=True, null=True)
    denomination = models.TextField(blank=True, null=True)
    disused = models.TextField(blank=True, null=True)
    embankment = models.TextField(blank=True, null=True)
    foot = models.TextField(blank=True, null=True)
    generator_source = models.TextField(db_column='generator:source', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    harbour = models.TextField(blank=True, null=True)
    highway = models.TextField(blank=True, null=True)
    historic = models.TextField(blank=True, null=True)
    horse = models.TextField(blank=True, null=True)
    intermittent = models.TextField(blank=True, null=True)
    junction = models.TextField(blank=True, null=True)
    landuse = models.TextField(blank=True, null=True)
    layer = models.TextField(blank=True, null=True)
    leisure = models.TextField(blank=True, null=True)
    lock = models.TextField(blank=True, null=True)
    man_made = models.TextField(blank=True, null=True)
    military = models.TextField(blank=True, null=True)
    motorcar = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    natural = models.TextField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    oneway = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    power = models.TextField(blank=True, null=True)
    power_source = models.TextField(blank=True, null=True)
    public_transport = models.TextField(blank=True, null=True)
    railway = models.TextField(blank=True, null=True)
    ref = models.TextField(blank=True, null=True)
    religion = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    shop = models.TextField(blank=True, null=True)
    sport = models.TextField(blank=True, null=True)
    surface = models.TextField(blank=True, null=True)
    toll = models.TextField(blank=True, null=True)
    tourism = models.TextField(blank=True, null=True)
    tower_type = models.TextField(db_column='tower:type', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    tracktype = models.TextField(blank=True, null=True)
    tunnel = models.TextField(blank=True, null=True)
    water = models.TextField(blank=True, null=True)
    waterway = models.TextField(blank=True, null=True)
    wetland = models.TextField(blank=True, null=True)
    width = models.TextField(blank=True, null=True)
    wood = models.TextField(blank=True, null=True)
    z_order = models.IntegerField(blank=True, null=True)
    way_area = models.FloatField(blank=True, null=True)
    way = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_line'


class PlanetOsmNodes(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lat = models.IntegerField()
    lon = models.IntegerField()
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_nodes'


class PlanetOsmPoint(models.Model):
    osm_id = models.BigIntegerField(primary_key='osm_id', blank=True)
    access = models.TextField(blank=True, null=True)
    addr_housename = models.TextField(db_column='addr:housename', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_housenumber = models.TextField(db_column='addr:housenumber', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_street = models.TextField(db_column='addr:street', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_postcode = models.TextField(db_column='addr:postcode', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_city = models.TextField(db_column='addr:city', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_interpolation = models.TextField(db_column='addr:interpolation', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    admin_level = models.TextField(blank=True, null=True)
    aerialway = models.TextField(blank=True, null=True)
    aeroway = models.TextField(blank=True, null=True)
    amenity = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    barrier = models.TextField(blank=True, null=True)
    bicycle = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    bridge = models.TextField(blank=True, null=True)
    boundary = models.TextField(blank=True, null=True)
    building = models.TextField(blank=True, null=True)
    capital = models.TextField(blank=True, null=True)
    construction = models.TextField(blank=True, null=True)
    covered = models.TextField(blank=True, null=True)
    culvert = models.TextField(blank=True, null=True)
    cutting = models.TextField(blank=True, null=True)
    denomination = models.TextField(blank=True, null=True)
    disused = models.TextField(blank=True, null=True)
    ele = models.TextField(blank=True, null=True)
    embankment = models.TextField(blank=True, null=True)
    foot = models.TextField(blank=True, null=True)
    generator_source = models.TextField(db_column='generator:source', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    harbour = models.TextField(blank=True, null=True)
    highway = models.TextField(blank=True, null=True)
    historic = models.TextField(blank=True, null=True)
    horse = models.TextField(blank=True, null=True)
    intermittent = models.TextField(blank=True, null=True)
    junction = models.TextField(blank=True, null=True)
    landuse = models.TextField(blank=True, null=True)
    layer = models.TextField(blank=True, null=True)
    leisure = models.TextField(blank=True, null=True)
    lock = models.TextField(blank=True, null=True)
    man_made = models.TextField(blank=True, null=True)
    military = models.TextField(blank=True, null=True)
    motorcar = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    natural = models.TextField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    oneway = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    power = models.TextField(blank=True, null=True)
    power_source = models.TextField(blank=True, null=True)
    public_transport = models.TextField(blank=True, null=True)
    railway = models.TextField(blank=True, null=True)
    ref = models.TextField(blank=True, null=True)
    religion = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    shop = models.TextField(blank=True, null=True)
    sport = models.TextField(blank=True, null=True)
    surface = models.TextField(blank=True, null=True)
    toll = models.TextField(blank=True, null=True)
    tourism = models.TextField(blank=True, null=True)
    tower_type = models.TextField(db_column='tower:type', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    tunnel = models.TextField(blank=True, null=True)
    water = models.TextField(blank=True, null=True)
    waterway = models.TextField(blank=True, null=True)
    wetland = models.TextField(blank=True, null=True)
    width = models.TextField(blank=True, null=True)
    wood = models.TextField(blank=True, null=True)
    z_order = models.IntegerField(blank=True, null=True)
    way = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_point'


class PlanetOsmPolygon(models.Model):

    def get_city_point(city):
        results = []
        for p in PlanetOsmPolygon.objects.raw("SELECT name, ST_asGEOJSON(ST_transform(way,4326)) FROM planet_osm_point "
                                              "WHERE place='city' "
                                              "AND name = %s", [city]):
            results.append((p.name, p.way))
        return results


    @staticmethod
    def get_city_point(city_var):
        results = []
        plz = re.findall(r"[0-9]{4,5}", str(city_var))
        if len(plz) == 1:
            for p in PlanetOsmPolygon.objects.raw(
                    "SELECT city.osm_id, city.name, St_asGeoJSON(ST_Transform(city.way,4326)) AS way "
                    "FROM planet_osm_polygon city JOIN planet_osm_polygon postcode "
                    "ON ST_INTERSECTS(city.way, postcode.way) "
                    "WHERE city.boundary = 'administrative' "
                    "AND city.admin_level = ANY ('{6,7,8}') "
                    "AND postcode.boundary = 'postal_code' AND postcode.postal_code =%s", [plz[0]]):
                results.append((p.name, p.way))

        else:
            for p in PlanetOsmPolygon.objects.raw(
                    "SELECT p.osm_id, p.name, ST_asGEOJSON(ST_transform(p.way,4326)) AS way "
                    "FROM planet_osm_polygon p WHERE p.boundary = 'administrative' "
                    "AND p.admin_level = ANY ('{6,7,8}') AND p.name ILIKE %s", [city_var]):
                results.append((p.name, p.way))
        return results

    @staticmethod
    def get_city_polygon(city_var):
        results = []
        plz = re.findall(r"[0-9]{4,5}", str(city_var))
        if len(plz) == 1:
            for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, St_asGeoJSON(ST_Transform(city.way,4326)) AS way "
                                                  "FROM planet_osm_polygon city JOIN planet_osm_polygon postcode "
                                                  "ON ST_INTERSECTS(city.way, postcode.way) "
                                                  "WHERE city.boundary = 'administrative' "
                                                  "AND city.admin_level = ANY ('{6,7,8}') "
                                                  "AND postcode.boundary = 'postal_code' AND postcode.postal_code ILIKE %s", [plz[0]]):
                results.append((p.name, p.way))

        else:
            for p in PlanetOsmPolygon.objects.raw("SELECT p.osm_id, p.name, ST_asGEOJSON(ST_transform(p.way,4326)) AS way "
                                                  "FROM planet_osm_polygon p WHERE p.boundary = 'administrative' "
                                                  "AND p.admin_level = ANY ('{6,7,8}') AND p.name ILIKE %s", [city_var]):
                print ("--")
                print (p.name)
                print ("--")
                results.append((p.name, p.way))
        return results

    # gibt alle PLZ & Polygone einer Stadt zurück. Vielleicht nützlich für später.
    @staticmethod
    def get_all_postal_codes_in_a_city(city):
        results = []
        for p in PlanetOsmPolygon.objects.raw("SELECT city.name, postcode.postal_code, "
                                              "ST_asGEOJSON(ST_transform(a.way,4326)) as way FROM "
                                              "planet_osm_polygon postcode JOIN planet_osm_polygon city "
                                              "ON ST_INTERSECTS(city.way, postcode.way) "
                                              "AND NOT ST_Touches(city.way, postcode.way) WHERE city.name =%s "
                                              "AND city.boundary = 'administrative'"
                                              "AND postcode.boundary = 'postal_code';", [city]):
            results.append((p.name, p.postal_code, p.way))
        return results

    # gibt Gebäude eines bestimmten Tags (Krankenhaus, Schule
    @staticmethod
    def get_buildings_in_city(amenity, city):
        results = []
        for p in PlanetOsmPolygon.objects.raw("SELECT a.osm_id, a.name, ST_asGEOJSON(ST_transform(a.way,4326)) AS way "
                                              "FROM planet_osm_point a, planet_osm_polygon b "
                                              "WHERE ST_Intersects(a.way, b.way) AND  a.amenity=%s "
                                              "AND b.name =%s", [amenity, city]):
            results.append((p.name, p.way))
        return results

    # Felder der Klasse PlanetOsmPolygon
    osm_id = models.BigIntegerField(primary_key='osm_id', blank=True)
    access = models.TextField(blank=True, null=True)
    addr_housename = models.TextField(db_column='addr:housename', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_housenumber = models.TextField(db_column='addr:housenumber', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_street = models.TextField(db_column='addr:street', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_postcode = models.TextField(db_column='addr:postcode', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_city = models.TextField(db_column='addr:city', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_interpolation = models.TextField(db_column='addr:interpolation', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    admin_level = models.TextField(blank=True, null=True)
    aerialway = models.TextField(blank=True, null=True)
    aeroway = models.TextField(blank=True, null=True)
    amenity = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    barrier = models.TextField(blank=True, null=True)
    bicycle = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    bridge = models.TextField(blank=True, null=True)
    boundary = models.TextField(blank=True, null=True)
    building = models.TextField(blank=True, null=True)
    construction = models.TextField(blank=True, null=True)
    covered = models.TextField(blank=True, null=True)
    culvert = models.TextField(blank=True, null=True)
    cutting = models.TextField(blank=True, null=True)
    denomination = models.TextField(blank=True, null=True)
    disused = models.TextField(blank=True, null=True)
    embankment = models.TextField(blank=True, null=True)
    foot = models.TextField(blank=True, null=True)
    generator_source = models.TextField(db_column='generator:source', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    harbour = models.TextField(blank=True, null=True)
    highway = models.TextField(blank=True, null=True)
    historic = models.TextField(blank=True, null=True)
    horse = models.TextField(blank=True, null=True)
    intermittent = models.TextField(blank=True, null=True)
    junction = models.TextField(blank=True, null=True)
    landuse = models.TextField(blank=True, null=True)
    layer = models.TextField(blank=True, null=True)
    leisure = models.TextField(blank=True, null=True)
    lock = models.TextField(blank=True, null=True)
    man_made = models.TextField(blank=True, null=True)
    military = models.TextField(blank=True, null=True)
    motorcar = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    natural = models.TextField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    oneway = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    power = models.TextField(blank=True, null=True)
    power_source = models.TextField(blank=True, null=True)
    public_transport = models.TextField(blank=True, null=True)
    railway = models.TextField(blank=True, null=True)
    ref = models.TextField(blank=True, null=True)
    religion = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    shop = models.TextField(blank=True, null=True)
    sport = models.TextField(blank=True, null=True)
    surface = models.TextField(blank=True, null=True)
    toll = models.TextField(blank=True, null=True)
    tourism = models.TextField(blank=True, null=True)
    tower_type = models.TextField(db_column='tower:type', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    tracktype = models.TextField(blank=True, null=True)
    tunnel = models.TextField(blank=True, null=True)
    water = models.TextField(blank=True, null=True)
    waterway = models.TextField(blank=True, null=True)
    wetland = models.TextField(blank=True, null=True)
    width = models.TextField(blank=True, null=True)
    wood = models.TextField(blank=True, null=True)
    z_order = models.IntegerField(blank=True, null=True)
    way_area = models.FloatField(blank=True, null=True)
    way = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_polygon'


        # https://gis.stackexchange.com/questions/130709/get-postal-codes-of-a-city-in-osm-via-postgis-postgresql


class PlanetOsmRels(models.Model):
    id = models.BigIntegerField(primary_key=True)
    way_off = models.SmallIntegerField(blank=True, null=True)
    rel_off = models.SmallIntegerField(blank=True, null=True)
    parts = models.TextField(blank=True, null=True)  # This field type is a guess.
    members = models.TextField(blank=True, null=True)  # This field type is a guess.
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_rels'


class PlanetOsmRoads(models.Model):
    osm_id = models.BigIntegerField(primary_key='osm_id', blank=True)
    access = models.TextField(blank=True, null=True)
    addr_housename = models.TextField(db_column='addr:housename', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_housenumber = models.TextField(db_column='addr:housenumber', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_street = models.TextField(db_column='addr:street', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_postcode = models.TextField(db_column='addr:postcode', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_city = models.TextField(db_column='addr:city', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_interpolation = models.TextField(db_column='addr:interpolation', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    admin_level = models.TextField(blank=True, null=True)
    aerialway = models.TextField(blank=True, null=True)
    aeroway = models.TextField(blank=True, null=True)
    amenity = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    barrier = models.TextField(blank=True, null=True)
    bicycle = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    bridge = models.TextField(blank=True, null=True)
    boundary = models.TextField(blank=True, null=True)
    building = models.TextField(blank=True, null=True)
    construction = models.TextField(blank=True, null=True)
    covered = models.TextField(blank=True, null=True)
    culvert = models.TextField(blank=True, null=True)
    cutting = models.TextField(blank=True, null=True)
    denomination = models.TextField(blank=True, null=True)
    disused = models.TextField(blank=True, null=True)
    embankment = models.TextField(blank=True, null=True)
    foot = models.TextField(blank=True, null=True)
    generator_source = models.TextField(db_column='generator:source', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    harbour = models.TextField(blank=True, null=True)
    highway = models.TextField(blank=True, null=True)
    historic = models.TextField(blank=True, null=True)
    horse = models.TextField(blank=True, null=True)
    intermittent = models.TextField(blank=True, null=True)
    junction = models.TextField(blank=True, null=True)
    landuse = models.TextField(blank=True, null=True)
    layer = models.TextField(blank=True, null=True)
    leisure = models.TextField(blank=True, null=True)
    lock = models.TextField(blank=True, null=True)
    man_made = models.TextField(blank=True, null=True)
    military = models.TextField(blank=True, null=True)
    motorcar = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    natural = models.TextField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    oneway = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    power = models.TextField(blank=True, null=True)
    power_source = models.TextField(blank=True, null=True)
    public_transport = models.TextField(blank=True, null=True)
    railway = models.TextField(blank=True, null=True)
    ref = models.TextField(blank=True, null=True)
    religion = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    shop = models.TextField(blank=True, null=True)
    sport = models.TextField(blank=True, null=True)
    surface = models.TextField(blank=True, null=True)
    toll = models.TextField(blank=True, null=True)
    tourism = models.TextField(blank=True, null=True)
    tower_type = models.TextField(db_column='tower:type', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    tracktype = models.TextField(blank=True, null=True)
    tunnel = models.TextField(blank=True, null=True)
    water = models.TextField(blank=True, null=True)
    waterway = models.TextField(blank=True, null=True)
    wetland = models.TextField(blank=True, null=True)
    width = models.TextField(blank=True, null=True)
    wood = models.TextField(blank=True, null=True)
    z_order = models.IntegerField(blank=True, null=True)
    way_area = models.FloatField(blank=True, null=True)
    way = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_roads'


class PlanetOsmWays(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nodes = models.TextField()  # This field type is a guess.
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planet_osm_ways'