import re
from django.db import models
import psycopg2
import importlib.util
from django.core import serializers
import json


def django_object_to_json(obj_list, fields):
    data = []
    for element in obj_list:
        for attr in fields:
            data.append({'name': element.name, 'admin_level': element.admin_level, 'way': element.way})

    #serializers.serialize('json', [obj, ], fields=fields)


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
    sql_string = '''SELECT ST_asText(ST_flipcoordinates(ST_Transform(ST_SetSRID(St_GeomFromText(%s),3857),4326)))'''
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
        for ele in Beschaeftigte.objects.raw("SELECT b.id, b.stadtteil, b.arbeitslosenquote::float, "
                                             "b.jugendarbeitslosenquote::float "
                                            "FROM beschaeftigte b "
                                            "WHERE b.stadtteil = %s", [stdteil]):
            results.append(ele)
        data = []
        for element in results:
            data.append({'stadtteil': element.stadtteil, 'arbeitslosenquote': element.arbeitslosenquote,
                         'jugendarbeitslosenquote': element.jugendarbeitslosenquote})
        return data

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
                    ("SELECT m.id, m.stadtteil, m.mietpreis::float from durchschnittliche_mietpreise m, planet_osm_polygon p "
                     "WHERE p.boundary = 'administrative' AND p.admin_level::integer >= 9 "
                     "AND m.stadtteil = p.name "
                    "AND m.stadtteil = %s", [stdteil]):
            results.append(ele)
        data = []
        for element in results:
            data.append({'stadtteil': element.stadtteil, 'mietpreis': element.mietpreis})
        return data

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
                    ("SELECT a.id, a.stadtteil, a.durchschnittsalter::float from durchschnittsalter a "
                     "WHERE a.stadtteil = %s", [stdteil]):
            results.append(ele)
        data = []
        for element in results:
            data.append({'stadtteil': element.stadtteil, 'durchschnittsalter': element.durchschnittsalter})
        return data

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
    path = models.TextField(blank=True, null=True)  # This field type is a guess.


    @staticmethod
    # parameter: punkt als geoJSON,
    #            distanz in metern
    def get_learmpegel(point, distance):
        results = []
        for lpegel in Laermpegel.objects.raw("SELECT l.id, l.dezibel::float, ST_asText(st_flipcoordinates(ST_setSRID(rings,4326))) as rings,"
                                             "ST_asText(st_flipcoordinates(ST_setSRID(path,4326))) as path "
                                             "FROM laermpegel l "
                                        "WHERE ST_DWithin(ST_SetSRID(rings,4326)::geography, "
                                        "ST_SetSRID(ST_GeomfromText(%s),4326)::geography, %s)", [point, distance]):

            results.append(lpegel)
        data = []
        for element in results:
            data.append({'dezibel': element.dezibel, 'rings': element.rings, 'path': element.path}, )
        return data

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
        for lkw_verbot in LkwVerbotszonen.objects.raw("SELECT l.id, l.bereich, ST_asText(st_flipcoordinates(ST_setSRID(rings,4326))) as rings "
                                             "FROm \"lkw-verbotszonen\" l "
                                             "WHERE ST_DWithin(ST_SetSRID(rings,4326)::geography, "
                                            "st_setsrid(ST_GeomFromText(%s),4326)::geography, %s::Integer)", [point, distance]):
            results.append(lkw_verbot)
        data = []
        for element in results:
            data.append({'bereich': element.bereich, 'rings': element.rings})
        return data

    class Meta:
        managed = False
        db_table = 'lkw-verbotszonen'


class Landtagswahl(models.Model):
    stadtteil = models.CharField(max_length=65535, blank=True, null=True)
    gesamt_spd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_cdu = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_gruene = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_fdp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_piraten = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_die_linke = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_npd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gesamt_afd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'landtagswahl'

    @staticmethod
    def get_parteiverteilung_in_stadtteil(stadtteil):
        results = []
        for verteilung in Landtagswahl.objects.raw("SELECT id, stadtteil, gesamt_spd::float, gesamt_cdu::float, gesamt_gruene::float,"
                                                   " gesamt_fdp::float, "
                                                   "gesamt_die_linke::float, gesamt_afd::float, gesamt_npd::float, gesamt_piraten::float FROM "
                                                   "landtagswahl WHERE stadtteil = %s ",
                                                      [stadtteil]):
            results.append(verteilung)
        data = []
        for element in results:
            data.append({'stadtteil': element.stadtteil, 'gesamt_spd': element.gesamt_spd, 'gesamt_cdu': element.gesamt_cdu,
                         'gesamt_gruene': element.gesamt_gruene, 'gesamt_fdp': element.gesamt_fdp,
                         'gesamt_die_linke': element.gesamt_die_linke, 'gesamt_afd': element.gesamt_afd,
                         'gesamt_afd': element.gesamt_afd, 'gesamt_piraten': element.gesamt_piraten})
        return data


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


    @staticmethod
    def get_query_string_polyfilter(number,outer_radius, inner_radius):
        return "ST_MakePolygon(ST_ExteriorRing(ST_Buffer(point{}.way, {}*1.6)), " \
               "ARRAY[ST_ExteriorRing(ST_Buffer(point{}.way, {}*1.6, 6))])".format(number, outer_radius, number, inner_radius)

    @staticmethod
    def get_filter_intersection(osm_id_polygon, filter_lines):
        print(osm_id_polygon, filter_lines)
        filter_dict = {'school': 'amenity', 'kindergarten': 'amenity', 'college': 'amenity', 'university': 'amenity',
                       'pharmacy': 'amenity', 'doctors': 'amenity', 'hospital': 'amenity', 'clinic': 'amenity',
                       'dentist': 'amenity', 'nursing_home': 'amenity', 'veterinary': 'amenity',
                       'social_facility': 'amenity', 'bank': 'amenity', 'atm': 'amenity', 'place_of_worship': 'amenity',
                       'theatre': 'amenity', 'nightclub': 'amenity', 'cinema': 'amenity', 'bus_station': 'amenity',
                       'restaurant': 'amenity', 'bus_stop': 'highway', 'station': 'railway',
                       'subway_entrance': 'railway',
                       'tram_stop': 'railway', 'terminal': 'aeroway', 'dog_park': 'leisure',
                       'fitness_centre': 'leisure',
                       'park': 'leisure', 'playground': 'leisure', 'attraction': 'tourism', 'museum': 'tourism',
                       'recreation_ground': 'landuse', 'mall': 'shop', 'supermarket': 'shop', 'chemist': 'shop'}
        if len(filter_lines) == 1:
            filter_data = filter_lines[0].strip().split(':')
            type_filter = filter_data[0].strip()
            radius = filter_data[1].strip().split(',')
            inner_radius = int(radius[0])
            outer_radius = int(radius[1])
            query_poly = PlanetOsmPoint.get_query_string_polyfilter('', outer_radius, inner_radius)
            query = "SELECT point.osm_id, ST_asText({}) AS intersection " \
                    "FROM planet_osm_polygon polygon, planet_osm_point point WHERE polygon.osm_id = {}" \
                    " AND point.{} = '{}'AND ST_Intersects(point.way, polygon.way);".format(query_poly, osm_id_polygon,
                                                                                            filter_dict[type_filter],
                                                                                            type_filter)
        elif len(filter_lines) == 2:
            filter_data_1 = filter_lines[0].strip().split(':')
            type_filter_1 = filter_data_1[0].strip()
            radius_1 = filter_data_1[1].strip().split(',')
            inner_radius_1 = int(radius_1[0])
            outer_radius_1 = int(radius_1[1])
            query_poly_1 = PlanetOsmPoint.get_query_string_polyfilter('1',outer_radius_1, inner_radius_1)
            #print(query_poly_1)
            filter_data_2 = filter_lines[1].strip().split(':')
            type_filter_2 = filter_data_2[0].strip()
            radius_2 = filter_data_2[1].strip().split(',')
            inner_radius_2 = int(radius_2[0])
            outer_radius_2 = int(radius_2[1])
            query_poly_2 = PlanetOsmPoint.get_query_string_polyfilter('2',outer_radius_2, inner_radius_2)
            query = "SELECT point1.osm_id, ST_asText(ST_Intersection({},{})) AS intersection " \
                    "FROM planet_osm_point point1, planet_osm_point point2, planet_osm_polygon polygon " \
                    "WHERE polygon.osm_id = {} AND point1.{} = '{}' AND point2.{} = '{}' " \
                    "AND ST_Intersects(polygon.way, point1.way) AND ST_Intersects(polygon.way, point2.way) " \
                    "AND ST_Intersects({}, {})".format(query_poly_1, query_poly_2, osm_id_polygon,
                                                       filter_dict[type_filter_1],type_filter_1,
                                                       filter_dict[type_filter_2], type_filter_2 ,
                                                       query_poly_1, query_poly_2)
        elif len(filter_lines) == 3:
            filter_data_1 = filter_lines[0].strip().split(':')
            type_filter_1 = filter_data_1[0].strip()
            radius_1 = filter_data_1[1].strip().split(',')
            inner_radius_1 = int(radius_1[0])
            outer_radius_1 = int(radius_1[1])
            query_poly_1 = PlanetOsmPoint.get_query_string_polyfilter('1', outer_radius_1, inner_radius_1)
            #print(query_poly_1)
            filter_data_2 = filter_lines[1].strip().split(':')
            type_filter_2 = filter_data_2[0].strip()
            radius_2 = filter_data_2[1].strip().split(',')
            inner_radius_2 = int(radius_2[0])
            outer_radius_2 = int(radius_2[1])
            query_poly_2 = PlanetOsmPoint.get_query_string_polyfilter('2', outer_radius_2, inner_radius_2)
            filter_data_3 = filter_lines[2].strip().split(':')
            type_filter_3 = filter_data_3[0].strip()
            radius_3 = filter_data_3[1].strip().split(',')
            inner_radius_3 = int(radius_3[0])
            outer_radius_3 = int(radius_3[1])
            query_poly_3 = PlanetOsmPoint.get_query_string_polyfilter('3',outer_radius_3, inner_radius_3)
            query = "SELECT point1.osm_id, ST_asText(ST_Intersection(ST_Intersection({},{}),ST_Intersection({},{}))) " \
                    "AS intersection FROM planet_osm_point point1, planet_osm_point point2, planet_osm_point point3, " \
                    "planet_osm_polygon polygon " \
                    "WHERE polygon.osm_id = {} AND point1.{} = '{}' AND point2.{} = '{}' AND point3.{} = '{}'" \
                    "AND ST_Intersects(polygon.way, point1.way) AND ST_Intersects(polygon.way, point2.way) " \
                    "AND ST_Intersects(polygon.way, point3.way) AND ST_Intersects({}, {}) AND ST_Intersects({}, {}) " \
                    "AND ST_Intersects({}, {})".format(query_poly_1,query_poly_2, query_poly_2, query_poly_3,
                                                       osm_id_polygon,
                                                       filter_dict[type_filter_1], type_filter_1,
                                                       filter_dict[type_filter_2], type_filter_2,
                                                       filter_dict[type_filter_3], type_filter_3,
                                                       query_poly_1, query_poly_2,
                                                       query_poly_1, query_poly_3,
                                                       query_poly_2, query_poly_3)
        else:
            print('zu viele Filter')
            return None
        data = list()
        for p in PlanetOsmPoint.objects.raw(query):
            p.way = transform_coords(p.intersection)
            print(p.name, p.way)
            data.append({'name': p.name, 'osm_id': p.osm_id, 'way': p.way})
        #print(len(data))
        return data


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
            results.append(p)
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
                    results.append(p)
            else:
                for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, "
                                                      "ST_asText(city.way) AS way "
                                                      "FROM planet_osm_polygon city "
                                                      "WHERE city.boundary = 'administrative' "
                                                      "AND city.admin_level = ANY ('{6,8,9,10}') "
                                                      "AND city.name ILIKE %s "
                                                      "GROUP BY city.osm_id, city.name, city.admin_level, way "
                                                      "ORDER BY city.admin_level::integer ASC", [city_var]):
                    p.way = transform_coords(p.way)
                    results.append(p)
                if len(results) > 0:
                    PlanetOsmPolygon.insert_stadtteile_to_results(results)

        else:
            for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, "
                                                  "ST_asText(city.way) AS way "
                                                  "FROM planet_osm_polygon city "
                                                  "WHERE city.boundary = 'administrative' "
                                                  "AND city.osm_id = %s::bigint "
                                                  "GROUP BY city.osm_id, city.name, city.admin_level, way "
                                                  "ORDER BY city.admin_level::integer ASC", [city_var]):
                p.way = transform_coords(p.way)
                results.append(p)
            if len(results)> 0:
                PlanetOsmPolygon.insert_stadtteile_to_results(results)


        results = set(results)
        results = list(results)
        results = sorted(results, key=lambda x: int(p.admin_level))  # Sortiere Liste anhand des 2. Elements
        data = []
        for element in results:
            #print(element.way)
            data.append({'name': element.name, 'osm_id':element.osm_id, 'admin_level': element.admin_level, 'way': element.way})
        return data

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