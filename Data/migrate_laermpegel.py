#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import importlib.util
import helpers
import json


def get_laerm(conn):
    with open ('Lärm_Pegel_LDEN.txt', 'r') as file:
        read_input_lden = json.load(file)
        read_input_lden = pandas.DataFrame.from_dict(read_input_lden, orient='index')
    with open ('Lärm_Schwellenwertüberschreitung_Strasse.txt', 'r') as file:
        read_input_schwelle = json.load(file)
        read_input_schwelle = pandas.DataFrame.from_dict(read_input_schwelle, orient='index')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS "laermpegel";')
    cur.execute("""CREATE TABLE "laermpegel" 
                (id SERIAL PRIMARY KEY, 
                objectid INTEGER,
                pegel VARCHAR,
                text VARCHAR,
                shape_length VARCHAR,
                shape_area VARCHAR,
                dezibel INTEGER,
                rings GEOMETRY)""")
    col_names = ['objectid', 'pegel', 'text', 'Shape_Length', 'Shape_Area', 'dezibel', 'rings']
    for elem in read_input_lden[0]['features']:
        values = [elem['attributes']['OBJECTID']]
        values.append(elem['attributes']['PEGEL'])
        values.append(elem['attributes']['TEXT'])
        values.append(elem['attributes']['SHAPE_Length'])
        values.append(elem['attributes']['SHAPE_Area'])
        values.append(elem['attributes']['DBA'])
        geometry = elem['geometry']['rings'][0]
        endstring = helpers.build_linestring(geometry)
        values.append(endstring)
        helpers.insert_geo_into('laermpegel', cur, col_names, values)
    conn.commit()
    print('[+] Committed all changes')
    return 'Lärmpegel mit '+str(len(read_input_lden[0]['features']))+' Datensätzen erfolgreich eingefügt'
