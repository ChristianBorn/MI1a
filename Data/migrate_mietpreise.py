#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import importlib.util
import helpers
def get_mietpreise(conn):
    with open('mietpreisdaten_wohnungsboerse.csv', 'r') as file:
        read_input = pandas.read_csv(file, sep=';', encoding='utf-8')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS "durchschnittliche mietpreise";')
    cur.execute("""CREATE TABLE "durchschnittliche mietpreise"
        (id SERIAL PRIMARY KEY, 
        stadtteil VARCHAR, 
        mietpreis DECIMAL)""")
    for row in read_input.itertuples():
        #print('-Inserting row: \n--'+str(row[1:]))
        input_values = [row[1]]
        input_values.append(row[2].replace(',','.').replace(' €',''))
        print(input_values)
        helpers.insert_into('"durchschnittliche mietpreise"', cur, list(read_input.columns), input_values)
    conn.commit()
    print('[+] Committed all changes')
    return 'Mietpreise erfolgreich eingefügt'