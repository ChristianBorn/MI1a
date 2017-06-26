#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import importlib.util
import helpers


def get_beschaeftigte(conn):
    with open('2014_Beschaeftigte_Stadtteil.csv', 'r') as file:
        read_input = pandas.read_csv(file, sep=';', encoding='utf-8')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS beschaeftigte;')
    cur.execute("""CREATE TABLE beschaeftigte 
    (id SERIAL PRIMARY KEY, 
    nr INTEGER,
    stadtteil VARCHAR, 
    beschaeftigte INTEGER, 
    quote DECIMAL, 
    arbeitslose INTEGER,
    arbeitslosenquote DECIMAL,
    jugendarbeitslosenquote DECIMAL)""")
    for row in read_input.itertuples():
        #print('-Inserting row: \n--'+str(row[1:]))
        #Liste mit den einzufügenden Werten bauen
        input_values = [row[1]]
        input_values.append(row[2])
        input_values.append(row[3])
        input_values.append(row[4].replace(',','.'))
        input_values.append(row[5])
        input_values.append(row[6].replace(',', '.'))
        input_values.append(row[7].replace(',', '.'))
        #Liste mit Werten in die Tabelle einfügen
        helpers.insert_into('beschaeftigte', cur, list(read_input.columns), input_values)
    conn.commit()
    print('[+] Committed all changes')
    return 'Beschäftigte mit '+str(read_input.shape[0])+' Datensätzen erfolgreich eingefügt'