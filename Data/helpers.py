#!/usr/bin/python
# -*- coding: utf-8 -*-


def insert_into(table_name, cur, col_names=[], values=[]):
    col_brackets = []
    val_brackets = []
    sql_statement = 'INSERT INTO %s ' %table_name
    for col in col_names:
        col_brackets.append(col.lower())
    col_brackets = '(' + ','.join(col_brackets) + ')'
    sql_statement = sql_statement+col_brackets
    sql_statement = sql_statement+' VALUES '
    for i in range(len(values)):
        val_brackets.append('%s')
    val_brackets = '('+','.join(val_brackets)+')'
    sql_statement = sql_statement+val_brackets
    cur.execute(sql_statement, values)
    #print('-Inserting values with query:\n--'+str(cur.query))


def insert_geo_into(table_name, cur, col_names=[], values=[], shape='poly'):
    col_brackets = []
    val_brackets = []
    sql_statement = 'INSERT INTO %s ' % table_name
    for col in col_names:
        col_brackets.append(col.lower())
    col_brackets = '(' + ','.join(col_brackets) + ')'
    sql_statement = sql_statement + col_brackets
    sql_statement = sql_statement + ' VALUES '
    for i in range(len(values)-1):
        val_brackets.append('%s')
    if shape == 'poly':
        val_brackets.append('ST_MakePolygon(ST_GeomFromText(%s,4326))')
    elif shape == 'path':
        val_brackets.append('ST_GeomFromText(%s,4326)')
    val_brackets = '(' + ','.join(val_brackets) + ')'
    sql_statement = sql_statement + val_brackets
    cur.execute(sql_statement, values)
    #print('-Inserting values with query:\n--' + str(cur.query))


def build_linestring(coords):
    coords_list = []
    for coord in coords:
        coords_list.append(str(coord).replace('[', '').replace(']', '').replace(',', ''))
    linestring = str(coords_list).replace('[', '').replace(']', '').replace('\'', '')
    linestring = 'LINESTRING(' + linestring + ')'
    return linestring
