#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import importlib.util
import helpers
def get_durchschnittsalter(conn):
    with open('2014_Durchschnittsalter_Stadtteil.csv', 'r') as file:
        read_input = pandas.read_csv(file, sep=';', encoding='utf-8')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS durchschnittsalter;')
    cur.execute("""CREATE TABLE durchschnittsalter 
            (id SERIAL PRIMARY KEY, 
            nr INTEGER,
            stadtteil VARCHAR,
            durchschnittsalter DECIMAL)""")
    for row in read_input.itertuples():
        print('-Inserting row: \n--'+str(row[1:4]))
        #Liste mit den einzufügenden Werten bauen
        input_values = [row[1]]
        input_values.append(row[2])
        input_values.append(row[3].replace(',','.'))
        #Liste mit Werten in die Tabelle einfügen
        helpers.insert_into('durchschnittsalter', cur, list(read_input.columns[:3]), input_values)
    conn.commit()
    print('[+] Committed all changes')
    return 'Durchschnittsalter mit '+str(read_input.shape[0])+' Datensätzen erfolgreich eingefügt'