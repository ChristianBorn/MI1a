#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import helpers

def get_landtagswahl(conn):
    with open('Landtagswahl_NRW3711.csv', 'r') as file:
        read_input = pandas.read_csv(file, sep=';', encoding='utf-8')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS landtagswahl;')
    cur.execute("""CREATE TABLE landtagswahl 
    (id SERIAL PRIMARY KEY, 
    stadtteil VARCHAR, 
    "gesamt_spd" DECIMAL, 
    "gesamt_cdu" DECIMAL, 
    "gesamt_gruene" DECIMAL, 
    "gesamt_fdp" DECIMAL,
    "gesamt_piraten" DECIMAL, 
    "gesamt_die_linke" DECIMAL, 
    "gesamt_npd" DECIMAL, 
    "gesamt_afd" DECIMAL)""")
    col_names = ['stadtteil', 'gesamt_spd', 'gesamt_cdu', 'gesamt_gruene', 'gesamt_fdp', 'gesamt_piraten', 'gesamt_die_linke', 'gesamt_npd', 'gesamt_afd']
    for row in read_input.itertuples():
        #print('-Inserting row: \n--'+str(row[1:]))
        #Liste mit den einzufügenden Werten bauen
        input_values = [row[2]]
        input_values.append(row[18].replace(',', '.'))
        input_values.append(row[23].replace(',', '.'))
        input_values.append(row[28].replace(',', '.'))
        input_values.append(row[33].replace(',','.'))
        input_values.append(row[38].replace(',', '.'))
        input_values.append(row[43].replace(',', '.'))
        input_values.append(row[48].replace(',', '.'))
        input_values.append(row[85].replace(',', '.'))
        #Liste mit Werten in die Tabelle einfügen
        helpers.insert_into('landtagswahl', cur, col_names, input_values)
    conn.commit()
    print('[+] Committed all changes')
    return 'Landtagswahldaten mit '+str(read_input.shape[0])+' Datensätzen erfolgreich eingefügt'