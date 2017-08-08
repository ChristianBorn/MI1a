import re
import copy
from django.db import models
import psycopg2
import importlib.util
import ast
from django.core import serializers
import json


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


def check_osm_columns():
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

    conn = connect_to_db(path='../mysite/settings.py')
    city_osm_ids = []
    city_osm_id_vals = {}
    with conn.cursor() as cur:
        cur.execute("SELECT osm_id FROM planet_osm_polygon "
                    "WHERE name IS NOT NULL "
                    "AND boundary = 'administrative' "
                    "AND admin_level::INTEGER >= 6 AND "
                    "ADMIN_level::integer <= 10"
                    " GROUP BY osm_id "
                    "ORDER BY osm_id ASC")
        for osm in cur:
            city_osm_ids.append(osm[0])
    print("osm-ids der Städte gelesen. \n"
          "Überprüfe osm-filter für jede Stadt")
    cur = conn.cursor()
    cnt = 0
    for osm in city_osm_ids:
        cnt += 1
        print("Position "+str(cnt)," von ",str(len(city_osm_ids)))
        key_list = []
        val_list = []
        for element in filter_dict:
            result = check_filter(cur, osm, filter_dict[element], element)[0]
            if result == 1:
                key_list.append(filter_dict[element])
                val_list.append(element)
        city_osm_id_vals[osm] = (key_list.copy(), val_list.copy())
    return city_osm_id_vals


def fill_table(result_dict):
    conn = connect_to_db(path='../mysite/settings.py')

    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS osm_filter_table;')
    cur.execute("""CREATE TABLE osm_filter_table 
        (osm_id BIGINT PRIMARY KEY, 
        key_list text, 
        val_list text)""")

    insert_query = """INSERT INTO osm_filter_table VALUES (%s, %s, %s)"""

    for value in result_dict:
        osm_id = value
        key_str = ";".join(result_dict[value][0])
        val_str = ";".join(result_dict[value][1])
        cur.execute(insert_query,[osm_id, str(key_str), str(val_str)])
    conn.commit()
    cur.close()
    conn.close()


def check_filter(cur, osm_id, filter_key, filter_value):
    cur.execute('''SELECT CASE WHEN COUNT(1) > 0 THEN 1 ELSE 0 END AS num
    FROM planet_osm_point p, planet_osm_polygon r
    WHERE r.osm_id = {}
    AND p.{} = '{}'
    AND ST_INTERSECTS(r.way, p.way);'''.format(osm_id, filter_key, filter_value))
    return cur.fetchone()


if __name__ == '__main__':
    results = check_osm_columns()
    fill_table(results)