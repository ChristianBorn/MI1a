import re
import copy
from django.db import models
import psycopg2
import importlib.util
import ast
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
    with conn.cursor() as cur:
        sql_string = '''SELECT ST_asText(ST_flipcoordinates(ST_Transform(ST_SetSRID(St_GeomFromText(%s),3857),4326)))'''
        cur.execute(sql_string, [result])
        rows = cur.fetchone()
        tmp_val = rows[0]
    return tmp_val

def str_coords_to_array_coords(result):
    '''koordinaten von POLYGON((51.0616154051779 6.77253026067161,51.0616932038293 6.77256430682088... zu 
    [[[51.0616154051779,6.77253026067161],[51.0616932038293 6.77256430682088],... 
    berücksichtigt einfache koordinatenstrings, doppelte polygone für Ringe und geometrycollections'''
    conn = connect_to_db(path='mysite/settings.py')
    #cur = conn.cursor()
    with conn.cursor() as cur:
        sql_string = '''SELECT ST_asgeojson(St_GeomFromText(%s))'''
        cur.execute(sql_string, [result])
        rows = cur.fetchone()[0]
    coords = rows[rows.index('"coordinates":') + len('"coordinates":'):-1]
    list_coords = ast.literal_eval(coords)
    return list_coords


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
    mietpreis = models.TextField(blank=True, null=True)

    @staticmethod
    # parameter: Stadtteil als String. zB. 'Altstadt-Nord'
    def get_mietpreise(stdteil):
        results = []
        for ele in DurchschnittlicheMietpreise.objects.raw\
                    ("SELECT m.id, m.stadtteil, m.mietpreis from durchschnittliche_mietpreise m WHERE"
                    " m.stadtteil = %s", [stdteil]):
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
    def get_learmpegel(osm_id, admin_level):
        results = [[], []]
        conn = connect_to_db(path='mysite/settings.py')
        with conn.cursor() as cur:
            cur.execute('''SELECT DISTINCT l.dezibel FROM laermpegel l;''')
            for element in cur.fetchall():
                cur.execute('''SELECT ST_asText(st_flipcoordinates(ST_setSRID(l.rings,4326))) 
                                FROM laermpegel l, planet_osm_polygon p 
                                WHERE l.rings IS NOT NULL AND l.dezibel = {} AND p.osm_id = {}
                                AND ST_INTERSECTS(ST_SetSRID(l.rings,4326)::geography, ST_Transform(p.way,4326)::geography);'''.format(element[0], osm_id))
                for ring in cur.fetchall():
                    results[0].append({'dezibel': element[0], 'rings': str_coords_to_array_coords(ring[0])})
                cur.execute('''SELECT ST_asText(st_flipcoordinates(ST_setSRID(l.path,4326))) 
                                FROM laermpegel l, planet_osm_polygon p 
                                WHERE l.path IS NOT NULL AND l.dezibel = {} AND p.osm_id = {}
                                AND ST_INTERSECTS(ST_SetSRID(l.path,4326)::geography, ST_Transform(p.way,4326)::geography);'''.format(element[0], osm_id))
                for path in cur.fetchall():
                    results[1].append({'dezibel': element[0], 'path': str_coords_to_array_coords(path[0])})
        if results == [[], []]:
            return 'empty'
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
    def get_verbotszone():
        results = []
        for lkw_verbot in LkwVerbotszonen.objects.raw("SELECT l.id, l.bereich, ST_asText(st_flipcoordinates(ST_setSRID(rings,4326))) as rings "
                                             "FROM \"lkw-verbotszonen\" l"):
            results.append(lkw_verbot)
        data = []
        for element in results:
            data.append({'bereich': element.bereich, 'rings': str_coords_to_array_coords(element.rings)})
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
                         'gesamt_die_linke': element.gesamt_die_linke, 'gesamt_npd': element.gesamt_npd,
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
    def get_osm_data(osm_id):
        conn = connect_to_db(path='mysite/settings.py')
        cur = conn.cursor()
        cur.execute(" SELECT osm_id, key_list, val_list FROM "
                    "osm_filter_table WHERE osm_id = %s", [osm_id])
        row = cur.fetchone()
        if row is not None:
            #keys = row[1].split(";")
            vals = row[2].split(";")
            #filter(None, keys)
            filter(None, vals)
            return vals
        else:
            return []



    @staticmethod
    def get_marker(osm_id, filter_value, session_filter_dict):
        '''gibt alle osm_daten der übergebenen Filter als liste mit dictionary zurück, 
        worin punkte, namen, die art des Filters und die Korrdinaten für die einzeichnung der marker gespeichert werden'''
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
        data = []
        for filter_lines in filter_value.strip(';').split(';'):
            filter_data = filter_lines.strip().split(':')
            type_filter = filter_data[0].strip()
            data_type_filter = []
            count_marker = 0

            #überprüfen ob maker während der session schonmal für dieses polygon ausgewählt wurden
            if type_filter in session_filter_dict:
                for element in session_filter_dict[type_filter]:
                    data.append(element)
                count_marker = len(session_filter_dict[type_filter])
                #print('Anzahl Marker:',count_marker, 'für', type_filter)
                continue

            conn = connect_to_db(path='mysite/settings.py')
            #cur = conn.cursor()
            with conn.cursor() as cur:
                cur.execute('''SELECT point.name, point.osm_id, ST_AsText(point.way) 
                              FROM planet_osm_point point, planet_osm_polygon stadtteil 
                              WHERE stadtteil.osm_id = {} AND point.{} = '{}' 
                              AND ST_Intersects(point.way, stadtteil.way);'''.format(osm_id, filter_dict[type_filter],
                                                                                        type_filter))
                for element in cur.fetchall():
                    data.append({'name': element[0],'osm_id': element[1],
                                 'way': str_coords_to_array_coords(transform_coords(element[2])),
                                 'amenity': type_filter})
                    data_type_filter.append({'name': element[0],'osm_id': element[1],
                                 'way': str_coords_to_array_coords(transform_coords(element[2])),
                                 'amenity': type_filter})

                cur.execute('''SELECT polygon.name, polygon.osm_id, ST_AsText(ST_Centroid(polygon.way)) 
                              FROM planet_osm_polygon polygon, planet_osm_polygon stadtteil 
                              WHERE stadtteil.osm_id = {} AND polygon.{} = '{}' 
                              AND ST_Intersects(polygon.way, stadtteil.way);'''.format(osm_id, filter_dict[type_filter],
                                                                                        type_filter))
                for element in cur.fetchall():
                    data.append({'name': element[0], 'osm_id': element[1],
                                 'way': str_coords_to_array_coords(transform_coords(element[2])),
                                 'amenity': type_filter})
                    data_type_filter.append({'name': element[0], 'osm_id': element[1],
                                'way': str_coords_to_array_coords(transform_coords(element[2])),
                                 'amenity': type_filter})
                if not data_type_filter:
                    return (type_filter, session_filter_dict)
            session_filter_dict[type_filter] = data_type_filter
            count_marker = len(data_type_filter)
            #print('Anzahl Marker:', count_marker, 'für', type_filter)
        #print('Anzahl Marker insgesamt: ', len(data))
        return (data, session_filter_dict)


    @staticmethod
    def get_landuse_polygons(osm_id_polygon):
        data = list()
        query_landuse = '''SELECT ST_asText(st_multi(st_union(poly.way))) 
                            FROM planet_osm_polygon stadtteil, planet_osm_polygon poly 
                            WHERE stadtteil.osm_id = {} AND ST_CoveredBy(poly.way, stadtteil.way) 
                            AND (poly.landuse IN ('grass', 'meadow', 'recreation_ground', 'village_green', 'allotments',
                             'brownfield', 'landfill', 'commercial', 'construction', 'greenfield', 'residential') 
                             OR poly.natural IN ('grassland', 'sand', 'beach', 'bare_rock', 'scree', 'shingle', 
                             'coastline'));'''.format(osm_id_polygon)
        conn = connect_to_db(path='mysite/settings.py')
        #cur = conn.cursor()
        with conn.cursor() as cur:
            cur.execute(query_landuse)
            result_landuse = cur.fetchone()[0]
        return result_landuse

    def union_osm_data(cur, query_circle_point, query_circle_polygon):
        # vereint die polygone/umkreise um die osm_daten die in planet_osm_point und planet_osm_polygon enthalten sind
        query_union_points_and_polygons = '''SELECT st_astext(st_multi(ST_Union(
                                                                ST_CollectionExtract(ST_MakeValid(st_geomfromtext(%s)), 3),
                                                                ST_CollectionExtract(ST_MakeValid(st_geomfromtext(%s)), 3))));'''
        cur.execute(query_circle_point)
        result_circle_point = cur.fetchone()[0]
        cur.execute(query_circle_polygon)
        result_circle_polygon = cur.fetchone()[0]
        if result_circle_point is not None and result_circle_polygon is not None:
            cur.execute(query_union_points_and_polygons, [result_circle_point, result_circle_polygon])
            result_circle = cur.fetchone()[0]
            return result_circle
        elif result_circle_point is not None:
            return result_circle_point
        elif result_circle_polygon is not None:
            return result_circle_polygon
        else:
            print('kein punkt oder polygon gefunden')
            return []


    @staticmethod
    def get_query_circle_osm_data(radius, tablename, marker_list):
        # variable anpassung der query für zeichnung von umkreisen.
        # kann sowohl mit planet_osm_polygon als auch planet_osm_point genutzt werden
        query_circle = '''SELECT st_astext(st_multi(st_union(st_buffer(osm_point.way, {})))) AS intersection  
                                    FROM {} osm_point WHERE osm_point.osm_id IN {};'''.format(radius*1.6, tablename, marker_list)
        return query_circle

    @staticmethod
    def get_circles_filter(cur, filter_data, marker_list):
        '''berechnet kreise mit angegebenen minimalen und maximalen abständen für angegebene filter innerhalb des 
        über die osm_id übergebenen polygons. 
        Nutzung von cursor.execute anstelle von model.raw, da bei intersects/union/difference kein primarykey vorhanden'''

        #filterstring splitten in werte (radius, filtername)
        type_filter = filter_data[0].strip()
        radius = filter_data[1].strip().split(',')
        if radius == 'marker':
            pass
        if radius[0] == '':
            inner_radius = 0
        else:
            inner_radius = int(radius[0])
        if radius[1] == '':
            outer_radius = 10000
        else:
            outer_radius = int(radius[1])

        query_inner_circle_point = PlanetOsmPoint.get_query_circle_osm_data(inner_radius, 'planet_osm_point', marker_list)
        query_outer_circle_point = PlanetOsmPoint.get_query_circle_osm_data(outer_radius, 'planet_osm_point', marker_list)
        query_inner_circle_polygon = PlanetOsmPoint.get_query_circle_osm_data(inner_radius, 'planet_osm_polygon', marker_list)
        query_outer_circle_polygon = PlanetOsmPoint.get_query_circle_osm_data(outer_radius, 'planet_osm_polygon', marker_list)

        query_difference_inner_outer = '''SELECT st_astext(ST_difference(
                                                            ST_CollectionExtract(ST_MakeValid(st_geomfromtext(%s)), 3), 
                                                            ST_CollectionExtract(ST_MakeValid(st_geomfromtext(%s)), 3)));'''
        if inner_radius == 0:
            # wenn minimaler Abstand = 0, nur äußeren Kreis zeichnen und keine Differenz bilden
            result_outer_circle = PlanetOsmPoint.union_osm_data(cur, query_outer_circle_point, query_outer_circle_polygon)
            return result_outer_circle
        else:
            # wenn minimaler Abstand > 0, Differenz zwischen innerem Kreis und äußerem bilden
            result_inner_circle = PlanetOsmPoint.union_osm_data(cur, query_inner_circle_point, query_inner_circle_polygon)
            result_outer_circle = PlanetOsmPoint.union_osm_data(cur, query_outer_circle_point, query_outer_circle_polygon)
            cur.execute(query_difference_inner_outer, [result_outer_circle, result_inner_circle])
            result_difference = cur.fetchone()[0]
            return result_difference


    @staticmethod
    def get_filter_intersection(osm_id_polygon, filter_value, session_filter_dict):
        '''schnittmengen zwischen übergebenen filtern berechnen. 
        gibt polygone zurück an denen alle filter sich schneiden und die fläche bewohnbar ist '''
        if filter_value == 'landuse':
            coords_landuse = PlanetOsmPoint.get_landuse_polygons(osm_id_polygon)
            if coords_landuse != 'GEOMETRYCOLLECTION EMPTY' or coords_landuse != 'MULTIPOLYGON EMPTY':
                data = [{'way':str_coords_to_array_coords(transform_coords(coords_landuse))}]
                return (data)
            else:
                return []

        # Daten für Marker berechnen, falls sie vorher schon über "Filter anzeigen" berechnet wurden,
        #  werden die Daten nur aus der Session geholt
        output_get_marker = PlanetOsmPoint.get_marker(osm_id_polygon, filter_value, session_filter_dict)
        if isinstance(output_get_marker[0], str):
            return output_get_marker

        filter_lines = filter_value.strip(';').split(';') # mit strip(;) wird verhindert, dass der Liste ein leeres Element hinzugefügt wird
        query_intersection = '''SELECT st_astext(st_multi(ST_Intersection(ST_CollectionExtract(ST_MakeValid(st_geomfromtext(%s)), 3),
                                                                ST_CollectionExtract(ST_MakeValid(st_geomfromtext(%s)), 3))));'''
        conn = connect_to_db(path='mysite/settings.py')
        #cur = conn.cursor()
        with conn.cursor() as cur:
            #von allen angegebenen filter die schnittmengen miteinader berechnen
            # in dem alle Umkreise der filter berechnet und anschließend intersected werden
            for filter_nr, filter in enumerate(filter_lines):
                filter_data = filter.strip().split(':')
                #für jeden Filter die passenden osmids in session suchen und diese für umkreissuche nutzen
                list_marker = tuple([element['osm_id'] for element in output_get_marker[0] if element['amenity']==filter_data[0]])
                if not list_marker:
                    print('kein marker gefunden')
                    return []
                elif len(list_marker) == 1:
                    list_marker = '('+str(list_marker[0])+')'
                coords_filter = PlanetOsmPoint.get_circles_filter(cur, filter_data, list_marker)
                if coords_filter != 'GEOMETRYCOLLECTION EMPTY' or coords_filter != 'MULTIPOLYGON EMPTY':
                    if filter_nr == 0:
                        result_intersection = coords_filter
                    else:
                        cur.execute(query_intersection, [result_intersection, coords_filter])
                        result_intersection = cur.fetchone()[0]
                else:
                    #wenn ein Filter kein Ergebnis liefert, kompletter Abbruch der Suche
                    return []

            #intersection mit landuse, um geeignete wohnfläche zu finden
            query_landuse = '''SELECT ST_asText(st_multi(st_union(poly.way))) 
                                FROM planet_osm_polygon stadtteil, planet_osm_polygon poly 
                                WHERE stadtteil.osm_id = {} AND ST_CoveredBy(poly.way, stadtteil.way) 
                                AND (poly.landuse IN ('grass', 'meadow', 'recreation_ground', 'village_green', 'allotments',
                                                    'brownfield', 'landfill', 'commercial', 'construction', 'greenfield', 'residential') 
                                    OR poly.natural IN ('grassland', 'sand', 'beach', 'bare_rock', 'scree', 'shingle', 
                                                      'coastline'));'''.format(osm_id_polygon)
            cur.execute(query_landuse)
            coords_landuse = cur.fetchone()[0]
            cur.execute(query_intersection, [result_intersection, coords_landuse])
            result_intersection_landuse = cur.fetchone()[0]

        # wenn ergebnis/polygone vorhanden dann als liste mit dictionary zurückgeben
        if result_intersection_landuse != 'MULTIPOLYGON EMPTY':
            data = [{'way': str_coords_to_array_coords(transform_coords(result_intersection_landuse))}]
            return (data, output_get_marker[1])
        else:
            return []


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
        new_admin_level = int(results[0].admin_level)
        results_size= len(results)
        tmp_results = []
        while len(results) == results_size and new_admin_level < 11:
            new_admin_level+=1
            for p in PlanetOsmPolygon.objects.raw("SELECT osm_id, name, admin_level, "
                                                      "ST_asText(way) AS way  "
                                                  "FROM planet_osm_polygon "
                                                  "WHERE boundary = 'administrative' "
                                                  "AND admin_level::integer = %s"
                                                  "AND ST_CONTAINS "
                                                  "(ST_SetSRID(ST_GeomFromText(%s),3857), way)"
                                                  "GROUP BY osm_id, name, admin_level, way "
                                                  "ORDER BY admin_level::integer ASC ",[new_admin_level, results[0].way]):
                tmp_results.append(p)
                tmp_results.sort(key=lambda poly: poly.name)
                results.extend(tmp_results)
        return results

    @staticmethod
    def get_city_polygon(city_var, osm_id):
        results = []
        multi_results = True
        plz = re.findall(r"[0-9]{4,5}", str(city_var))
        if not osm_id:
            if len(plz) == 1:
                for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, postcode.postal_code,"
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

                    results.append(p)
                    p.way = p.cway
                    tmp_results = []
                    for element in results:
                        if p.admin_level in ['6','8']:
                            tmp_results.append(element)
                    for o in tmp_results:
                        results.remove(o)

            else:
                for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, "
                                                      "ST_asText(city.way) AS way "
                                                      "FROM planet_osm_polygon city "
                                                      "WHERE city.boundary = 'administrative' "
                                                      "AND city.admin_level::integer = ANY ('{6,7,8,9,10}') "
                                                      "AND city.name ILIKE %s "
                                                      "GROUP BY city.osm_id, city.name, city.admin_level, way "
                                                      "ORDER BY city.admin_level::integer ASC", [city_var]):
                    results.append(p)

                if len(results) == 1:
                    multi_results = False
                    results = copy.deepcopy([results[0]])
                    PlanetOsmPolygon.insert_stadtteile_to_results(results)
                '''
                if len(results) > 0:
                    first_adm = results[0].admin_level
                    for e in results[1:]:
                        print("check  "+e.admin_level+ "  |  "+first_adm+"     "+str(multi_results))
                        if e.admin_level == first_adm:
                            multi_results = True
                            break
                    if not multi_results:
                        results = copy.deepcopy([results[0]])
                        PlanetOsmPolygon.insert_stadtteile_to_results(results)
                for e in results:
                    print (e.name)
                print ("----")
                print (multi_results)
                '''
        else:
    # gibt alle PLZ & Polygone einer Stadt zurück. Vielleicht nützlich für später.
            for p in PlanetOsmPolygon.objects.raw("SELECT city.osm_id, city.name, city.admin_level, "
                                                  "ST_asText(city.way) AS way "
                                                  "FROM planet_osm_polygon city "
                                                  "WHERE city.boundary = 'administrative' "
                                                  "AND city.osm_id = %s::bigint "
                                                  "GROUP BY city.osm_id, city.name, city.admin_level, way "
                                                  "ORDER BY city.admin_level::integer ASC", [city_var]):
                results.append(p)
                #print(p.name)
            if len(results) > 0:
                multi_results = False
                results = copy.deepcopy([results[0]])
                PlanetOsmPolygon.insert_stadtteile_to_results(results)
        results = set(results)
        results = list(results)

        for element in results:
            element.admin_level = int(element.admin_level)
        results = sorted(results, key=lambda x: int(x.admin_level))  # Sortiere Liste anhand des 2. Elements
        data = []
        for element in results:
            parent_osm, parent_name = PlanetOsmPolygon.get_osm_of_next_higher_place(element.osm_id, False)
            #name / osm_id der zugehörigen Stadt (ggf. auch Landkreis).
            affil_city_osm, affil_city_name = PlanetOsmPolygon.get_osm_of_next_higher_place(element.osm_id,True)
            if multi_results and affil_city_name != parent_name:
                affil_city_name += " - "+parent_name
            data.append({'name': element.name, 'osm_id': element.osm_id, 'admin_level': element.admin_level,
                         'way': str_coords_to_array_coords(transform_coords(element.way)), 'open_data': 'undefined',
                         'parent_osm': parent_osm,
                         'parent_name': parent_name,
                         'affil_city_name': affil_city_name,
                         'affil_city_osm': affil_city_osm})
        return data

        # gibt osm_id und Name der nächsten übergeordneten Ortschaft eines Ortes zurück. Falls kein Fund, Leer-String
        # Parameter:
        #   osm_id: osm_id des Ortes, dessen übergeordneter Ort gesucht werden soll.
        #       Beispiel: Stadttel -> Stadtbezirk; Stadtbezirk -> Stadt
        #
        #   city_only: bei True wird zugehörige Stadt gesucht. bei False, der nächsthöhere Ort, nach admin_level
        #       True: Oberbilk -> Düsseldorf        False: Oberbilk -> Stadtbezirk
    @staticmethod
    def get_osm_of_next_higher_place(osm_id, city_only):
        conn = connect_to_db(path='mysite/settings.py')
        with conn.cursor() as cur:
            if not city_only:
                sql_string = "SELECT poly.osm_id, poly.name, poly.admin_level FROM " \
                             "(SELECT osm_id, name, admin_level,way FROM planet_osm_polygon ) as poly," \
                             "(SELECT osm_id,admin_level,way FROM planet_osm_polygon WHERE osm_id = %s) as poly_way " \
                             "WHERE poly.admin_level::INTEGER < poly_way.admin_level::INTEGER " \
                             "AND poly.admin_level = ANY ('{6,8,9,10}') " \
                             "AND st_contains(poly.way, poly_way.way) " \
                             "GROUP BY poly.osm_id, poly.name, poly.admin_level " \
                             "ORDER BY poly.admin_level::INTEGER DESC LIMIT 1"
            else:
                sql_string = "SELECT poly.osm_id, poly.name, poly.admin_level FROM " \
                             "(SELECT osm_id, name, admin_level,way FROM planet_osm_polygon ) as poly," \
                             "(SELECT osm_id,admin_level,way FROM planet_osm_polygon WHERE osm_id = %s) as poly_way " \
                             "WHERE poly.admin_level::INTEGER < poly_way.admin_level::INTEGER " \
                             "AND poly.admin_level = ANY ('{6,8}') " \
                             "AND st_contains(poly.way, poly_way.way) " \
                             "GROUP BY poly.osm_id, poly.name, poly.admin_level " \
                             "ORDER BY poly.admin_level::INTEGER DESC LIMIT 1"
            cur.execute(sql_string, [osm_id])
            rows = cur.fetchone()
            if rows is not None:
                return rows[0], rows[1]
            else:
                return 0,''


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

    @staticmethod
    def get_city_by_coords(lat, lng):
        result = [None,'undefined']
        conn = connect_to_db(path='mysite/settings.py')
        with conn.cursor() as cur:
            sql_string = "SELECT p.osm_id, p.name, p.admin_level " \
                         "FROM planet_osm_polygon p " \
                         "WHERE p.boundary = 'administrative' " \
                         "AND p.admin_level::integer = ANY ('{6,8,9,10}') " \
                         "AND st_contains(ST_asText(ST_flipcoordinates(ST_Transform(ST_SetSRID(p.way,3857),4326)))," \
                         "Point(%s, %s)::geometry) " \
                         "GROUP BY p.osm_id, p.name, p.admin_level ORDER BY p.admin_level::integer DESC LIMIT 1;"


            #sort group-by alle felder orderby adminlevel::integer desc und limit 1
            #get_osm_ aufwärts hierachie
            cur.execute(sql_string, [lat, lng])
            rows = cur.fetchone()
            if rows:
                osm_id = rows[0]
                name = rows[1]
                result = [name, osm_id]
        return result

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
