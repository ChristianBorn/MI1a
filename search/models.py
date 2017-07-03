import re
from django.db import models
import psycopg2
import importlib.util
#from Data.data_migration import connect_to_db
from django.core import serializers


def django_object_to_json(obj, fields):
    if len(fields) == 0:
        return serializers.serialize('json', [obj, ])
    else:
        return serializers.serialize('json', [obj, ], fields=fields)

def connect_to_db(path='../mysite/settings.py'):
    #Holt die Datenbankeinstellungen aus der Settings.py
    spec = importlib.util.spec_from_file_location('settings.DATABASES', path)
    database_settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(database_settings)
    database_settings = database_settings.DATABASES['default']
    db_name = database_settings['NAME']
    db_user = database_settings['USER']
    db_pw = database_settings['PASSWORD']
    #Verbindung mit den geholten Daten
    conn = psycopg2.connect(dbname=db_name,
                            user=db_user,
                            password=db_pw)
    return conn

def transform_coords(result):
    conn = connect_to_db(path='mysite/settings.py')
    cur = conn.cursor()
    sql_string = '''SELECT ST_asGeoJSON(ST_flipcoordinates(ST_Transform(ST_SetSRID(St_GeomFromText(%s),3857),4326)))'''

    cur.execute(sql_string, [result])
    rows = cur.fetchone()
    tmp_val = rows[0]
    return tmp_val


class Beschaeftigte(models.Model):
    id = models.IntegerField(primary_key=True)
    nr = models.IntegerField(blank=True, null=True)
    stadtteil = models.TextField(blank=True, null=True)
    beschaeftigte = models.IntegerField(blank=True, null=True)
    quote = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    arbeitslose = models.IntegerField(blank=True, null=True)
    arbeitslosenquote = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jugendarbeitslosenquote = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    @staticmethod
    # parameter: Stadtteil als String. zB. 'Altstadt-Nord'
    # gibt
    def get_arbeitslosenquote(stdteil):
        results = []
        for ele in Beschaeftigte.objects.raw("SELECT b.id, b.stadtteil, b.arbeitslosenquote "
                                            "FROM beschaeftigte b, planet_osm_polygon p "
                                            "WHERE p.boundary = 'administrative' AND p.admin_level::integer >= 9"
                                            "AND b.stadtteil = p.name "
                                             "AND b.stadtteil = %s", [stdteil]):
            results.append(ele)
            return results

    @staticmethod
    # parameter: Stadtteil als String. zB. 'Altstadt-Nord'
    def get_jugendarbeitslosenquote(stdteil):
        results = []
        for ele in Beschaeftigte.objects.raw("SELECT b.id, b.stadtteil, b.jugendarbeitslosenquote "
                                           "FROM beschaeftigte b, planet_osm_polygon p "
                                           "WHERE p.boundary = 'administrative' AND p.admin_level::integer >= 9"
                                           "AND b.stadtteil = p.name "
                                           "AND b.stadtteil = p.name "
                                             "AND b.stadtteil = %s", [stdteil]):

            results.append(ele)
            return results

    class Meta:
        managed = False
        db_table = 'beschaeftigte'


class DurchschnittlicheMietpreise(models.Model):
    stadtteil = models.TextField(blank=True, null=True)
    mietpreis = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    @staticmethod
    # parameter: Stadtteil als String. zB. 'Altstadt-Nord'
    def get_mietpreise(stdteil):
        results = []
        for ele in DurchschnittlicheMietpreise.objects.raw\
                    ("SELECT m.id, m.stadtteil, m.mietpreis from durchschnittliche_mietpreise m, planet_osm_polygon p "
                     "WHERE p.boundary = 'administrative' AND p.admin_level::integer >= 9 "
                     "AND m.stadtteil = p.name "
                    "AND m.stadtteil = %s", [stdteil]):
            results.append(ele)
            return results

    class Meta:
        managed = False
        db_table = 'durchschnittliche_mietpreise'


class Durchschnittsalter(models.Model):
    id = models.IntegerField(primary_key=True)
    nr = models.IntegerField(blank=True, null=True)
    stadtteil = models.TextField(blank=True, null=True)
    durchschnittsalter = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    @staticmethod
    # parameter: Stadtteil als String. zB. 'Altstadt-Nord'
    def get_durchschnittsalter(stdteil):
        results = []
        for ele in Durchschnittsalter.objects.raw \
                    ("SELECT a.id, a.stadtteil, a.durchschnittsalter from durchschnittsalter a, planet_osm_polygon p "
                     "WHERE p.boundary = 'administrative' "
                     "AND p.admin_level::integer >= 9 "
                     "AND a.stadtteil = p.name "
                     "AND a.stadtteil = %s", [stdteil]):
            results.append(ele)
        return results

    class Meta:
        managed = False
        db_table = 'durchschnittsalter'


class Laermpegel(models.Model):
    id = models.IntegerField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    pegel = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    shape_length = models.TextField(blank=True, null=True)
    shape_area = models.TextField(blank=True, null=True)
    dezibel = models.IntegerField(blank=True, null=True)
    rings = models.TextField(blank=True, null=True)  # This field type is a guess.


    @staticmethod
    # parameter: punkt als geoJSON,
    #            distanz in metern
    def get_learmpegel(point, distance):
        results = []
        for lpegel in Laermpegel.objects.raw("SELECT l.id, l.dezibel, ST_asText(ST_setSRID(rings,4326)) as rings from laermpegel l "
                                        "WHERE ST_DWithin(ST_SetSRID(rings,4326)::geography, "
                                        "st_setsrid(ST_geomFromGeoJson(%s),4326)::geography, %s)", [point, distance]):
            lpegel.rings = transform_coords(lpegel.rings)
            results.append(lpegel)
        return results

    class Meta:
        managed = False
        db_table = 'laermpegel'


class LkwVerbotszonen(models.Model):
    #id = models.IntegerField(primary_key=True)
    bereich = models.TextField(blank=True, null=True)
    shape_leng = models.TextField(blank=True, null=True)
    shape_length = models.TextField(blank=True, null=True)
    shape_area = models.TextField(blank=True, null=True)
    rings = models.TextField(blank=True, null=True)  # This field type is a guess.

    @staticmethod
    # parameter: punkt als geoJSON,
    #            distanz in metern
    def get_verbotszone(point, distance):
        results = []
        for lkw_verbot in LkwVerbotszonen.objects.raw("SELECT l.id, l.bereich, ST_AsText(rings) as rings "
                                             "FROm lkw_verbotszonen l "
                                             "WHERE ST_DWithin(ST_SetSRID(rings,4326)::geography, "
                                            "st_setsrid(ST_geomFromGeoJson(%s),4326)::geography, %s)", [point, distance]):
            lkw_verbot.rings = transform_coords(lkw_verbot.rings)
            results.append(lkw_verbot)
        return results

    class Meta:
        managed = False
        db_table = 'lkw_verbotszonen'


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

    @staticmethod
    def get_city_point(city):
        results = []
        for p in PlanetOsmPolygon.objects.raw("SELECT name, St_asText(ST_transform(way,4326)) FROM planet_osm_point "
                                              "WHERE place=ANY ('{city,town}')"
                                              "AND name =%s", [city]):
            results.append((p.name, p.way))
        return results


    # gibt Gebäude eines bestimmten Tags (Krankenhaus, Schule.)s
    @staticmethod
    def get_buildings_in_city(amenity, point, start_rad, end_rad):
        results = []
        for p in PlanetOsmPoint.objects.raw("SELECT pt.osm_id, pt.name, pt.amenity, St_asText(pt.way) as way FROM planet_osm_point pt "
                                              "WHERE  pt.amenity = %s "
                                              "AND NOT ST_DWithin(ST_setSRID(ST_GeomFromGeoJSON(%s),4326)::geography, "
                                                    "ST_TRANSFORM(pt.way,4326)::geography, %s)"
                                              "AND ST_DWithin(ST_setSRID(ST_GeomFromGeoJSON(%s),4326)::geography,"
                                                    "ST_TRANSFORM(pt.way,4326)::geography, %s)"
                                              "GROUP BY pt.osm_id, pt.name, pt.amenity, pt.way ", [amenity, point, start_rad, point, end_rad]):
            p.way = transform_coords(p.way)
            results.append(p)
        return results

    @staticmethod
    def get_osm_points_in_district(osm_id_polygon= -62578, type_filter='restaurant', inner_radius=1000, outer_radius=3000):
        '''Gibt Ringe/Donuts um alle gesuchten Punkte zurück, mit mindest (inner_radius) und maximal Abstand (outer_radius).
        type_filter = Name bzw. Art des Filters (amenity='restaurant', railway='station'), Spaltenname wird aus dict generiert 
        '''
        filter_dict = {'school': 'amenity', 'kindergarten': 'amenity', 'college': 'amenity', 'university': 'amenity',
                       'pharmacy': 'amenity', 'doctors': 'amenity', 'hospital': 'amenity', 'clinic': 'amenity',
                       'dentist': 'amenity', 'nursing_home': 'amenity', 'veterinary': 'amenity',
                       'social_facility': 'amenity', 'bank': 'amenity', 'atm': 'amenity', 'place_of_worship': 'amenity',
                       'theatre': 'amenity', 'nightclub': 'amenity', 'cinema': 'amenity', 'bus_station': 'amenity',
                       'restaurant': 'amenity', 'bus_stop': 'highway', 'station': 'railway', 'subway_entrance': 'railway',
                       'tram_stop': 'railway', 'terminal': 'aeroway', 'dog_park': 'leisure', 'fitness_centre': 'leisure',
                       'park': 'leisure', 'playground': 'leisure', 'attraction': 'tourism', 'museum': 'tourism',
                       'recreation_ground': 'landuse', 'mall': 'shop', 'supermarket': 'shop', 'chemist': 'shop'}

        results = list()
        for p in PlanetOsmPoint.objects.raw("SELECT point.osm_id, point.name, ST_asText(ST_MakePolygon("
                                            "ST_ExteriorRing(ST_Buffer(point.way, {}*1.6)), "
                                            "ARRAY[ST_ExteriorRing(ST_Buffer(point.way, {}*1.6, 6))])) AS cway "
                                            "FROM planet_osm_polygon polygon, planet_osm_point point "
                                            "WHERE polygon.osm_id = {} AND point.{} = '{}'"
                                            " AND ST_Intersects(point.way, polygon.way);".format(
                outer_radius, inner_radius, osm_id_polygon, filter_dict[type_filter], type_filter)):
            p.way = transform_coords(p.cway)
            results.append(p.way[32:-1])
        return results

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

    @staticmethod
    def insert_stadtteile_to_results(results):
        for p in PlanetOsmPolygon.objects.raw("SELECT osm_id, name, admin_level, "
                                                  "ST_asText(way) AS way  "
                                              "FROM planet_osm_polygon "
                                              "WHERE boundary = 'administrative' "
                                              "AND admin_level::integer >= %s "
                                              "AND admin_level::integer <=10 "
                                              "AND ST_CONTAINS "
                                              "(ST_SetSRID(ST_GeomFromText(%s),3857), way)"
                                              "GROUP BY osm_id, name, admin_level, way "
                                              "ORDER BY admin_level::integer ASC ",[results[0].admin_level, results[0].way]):
            p.way = transform_coords(p.way)
            results.append(p.way[32:-1])
        return results

    @staticmethod
    def get_city_polygon(city_var, osm_id):
        results = []
        plz = re.findall(r"[0-9]{4,5}", str(city_var))
        if not osm_id:
            if len(plz) == 1:
                for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, postcode.postal_code, "
                                                      "ST_asText(city.way) AS cway FROM "
                                                      "planet_osm_polygon city JOIN planet_osm_polygon postcode ON "
                                                      "ST_INTERSECTS(city.way, postcode.way) "
                                                        "AND NOT ST_Touches(city.way, postcode.way)"
                                                      "WHERE city.boundary = 'administrative' "
                                                      "AND city.admin_level::integer = ANY ('{6,7,8,9,10}') "
                                                      "AND postcode.boundary = 'postal_code' "
                                                      "AND postcode.postal_code ILIKE %s "
                                                      "GROUP BY city.osm_id, city.name, city.admin_level, postcode.postal_code, cway "
                                                      "ORDER BY city.admin_level::integer ASC", [plz[0]]):
                    p.way = transform_coords(p.cway)
                    results.append(p.way[32:-1])
            else:
                print("++")
                for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, "
                                                      "ST_asText(city.way) AS way "
                                                      "FROM planet_osm_polygon city "
                                                      "WHERE city.boundary = 'administrative' "
                                                      "AND city.admin_level = ANY ('{6,8,9,10}') "
                                                      "AND city.name ILIKE %s "
                                                      "GROUP BY city.osm_id, city.name, city.admin_level, way "
                                                      "ORDER BY city.admin_level::integer ASC", [city_var]):
                    p.way = transform_coords(p.way)
                    results.append(p.way[32:-1])
                #if len(results) > 0:
                #    PlanetOsmPolygon.insert_stadtteile_to_results(results)

        else:
            for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, "
                                                  "ST_asText(city.way) AS way "
                                                  "FROM planet_osm_polygon city "
                                                  "WHERE city.boundary = 'administrative' "
                                                  "AND city.admin_level = ANY ('{6,8,9,10}') "
                                                  "AND city.osm_id = %s "
                                                  "GROUP BY city.osm_id, city.name, city.admin_level, way "
                                                  "ORDER BY city.admin_level::integer ASC", [city_var]):
                p.way = transform_coords(p.way)
                results.append(p.way[32:-1])
            #if len(results)> 0:
            #    PlanetOsmPolygon.insert_stadtteile_to_results(results)


        #results = set(results)
        #results = list(results)
        #results = sorted(results, key=lambda x: int(p.admin_level))  # Sortiere Liste anhand des 2. Elements
        return results

    # gibt alle PLZ & Polygone einer Stadt zurück. Vielleicht nützlich für später.
    @staticmethod
    def get_all_postal_codes_in_a_city(city):
        results = []
        for p in PlanetOsmPolygon.objects.raw("SELECT city.name, postcode.postal_code, "
                                              "ST_asText(ST_transform(a.way,4326)) as way FROM "
                                              "planet_osm_polygon postcode JOIN planet_osm_polygon city "
                                              "ON ST_INTERSECTS(city.way, postcode.way) "
                                              "AND NOT ST_Touches(city.way, postcode.way) WHERE city.name =%s "
                                              "AND city.boundary = 'administrative'"
                                              "AND postcode.boundary = 'postal_code';", [city]):
            p.way = transform_coords(p.way)
            results.append(p)
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