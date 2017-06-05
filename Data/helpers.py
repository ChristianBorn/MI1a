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
    print('-Inserting values with query:\n--'+str(cur.query))