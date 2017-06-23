#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import importlib.util
import helpers
import json
def get_lkw(conn):
    with open ('LKW-Verbotszonen.txt', 'r') as file:
        read_input = json.load(file)
    read_input = pandas.DataFrame.from_dict(read_input, orient='index')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS "lkw-verbotszonen";')
    cur.execute("""CREATE TABLE "lkw-verbotszonen" 
                (id SERIAL PRIMARY KEY, 
                bereich VARCHAR,
                shape_leng VARCHAR,
                shape_length VARCHAR,
                shape_area VARCHAR,
                rings GEOMETRY)""")
    col_names = ['Bereich', 'SHAPE_Leng', 'Shape_Length','Shape_Area', 'rings']
    for elem in read_input[0]['features']:
        values = [elem['attributes']['Bereich']]
        values.append(elem['attributes']['SHAPE_Leng'])
        values.append(elem['attributes']['Shape_Length'])
        values.append(elem['attributes']['Shape_Area'])
        geometry = elem['geometry']['rings'][0]
        endstring = helpers.build_linestring(geometry)
        values.append(endstring)
        helpers.insert_geo_into('"lkw-verbotszonen"', cur, col_names, values)
    conn.commit()
    print('[+] Committed all changes')
    return 'LKW-Verbotszonen mit '+str(len(read_input[0]['features']))+' Datensätzen erfolgreich eingefügt'