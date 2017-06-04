#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
def get_beschaeftigte(conn):
    with open('2014_Beschaeftigte_Stadtteil.csv', 'r') as file:
        read_input = pandas.read_csv(file, sep=';', encoding='utf-8')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS beschäftigte;')
    cur.execute("""CREATE TABLE beschäftigte 
    (id SERIAL PRIMARY KEY, 
    nr INTEGER,
    stadtteil VARCHAR, 
    beschaeftigte INTEGER, 
    quote DECIMAL, 
    arbeitslose INTEGER,
    arbeitslosenquote DECIMAL,
    jugendarbeitslosenquote DECIMAL)""")
    sql_statement = u"""INSERT INTO beschäftigte
    (nr,
    stadtteil,
    beschaeftigte,
    quote,
    arbeitslose,
    arbeitslosenquote,
    jugendarbeitslosenquote)
    VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    for row in read_input.itertuples():
        print('-Inserting row: \n--'+str(row[1:]))
        cur.execute(sql_statement, (row[1],
                                    row[2],
                                    row[3],
                                    row[4].replace(',','.'),
                                    row[5],
                                    row[6].replace(',','.'),
                                    row[7].replace(',','.')))
    conn.commit()
    print('[+] Committed all changes')