#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib.util
import psycopg2
from psycopg2 import extensions
import numpy as np
import migrate_beschaeftigte
import migrate_mietpreise
import migrate_durchschnittsalter
import migrate_lkw
import migrate_laermpegel

def main():
    conn = connect_to_db()
    #erstelle die Tabelle "Beschaeftigte" und füge die Datensätze dort ein
    meldungen = [migrate_beschaeftigte.get_beschaeftigte(conn)]
    #erstelle die Tabelle "Mietpreise" und füge die Datensätze dort ein
    meldungen.append(migrate_mietpreise.get_mietpreise(conn))
    #erstelle die Tabelle "Durchschnittsalter" und füge die Datensätze dort ein
    meldungen.append(migrate_durchschnittsalter.get_durchschnittsalter(conn))
    #Erstelle die Tabelle "lkw-verbotszonen" und füge die Datensätze ein
    meldungen.append(migrate_lkw.get_lkw(conn))
    #Erstelle die Tabelle "lärmpegel" und füge Datensätze ein
    meldungen.append(migrate_laermpegel.get_laerm(conn))
    conn.close()
    for elem in meldungen:
        print('[+] '+elem)
    print('\n[+] Data Migration finished without error')
def to_float(x):
  """psycopg2 interpolation to float"""
  return extensions.AsIs('%f' % float(x))
def to_int(x):
  """psycopg2 interpolation to int"""
  return extensions.AsIs('%d' % int(x))
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
    #Mapping von Numpy Datentypen auf Postgres Datentypen
    extensions.register_adapter(np.int64, to_float)
    extensions.register_adapter(np.integer, to_int)
    return conn





if __name__ == '__main__':
    main()