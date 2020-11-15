#!/usr/bin/env python3

import os
import mysql.connector

username = os.environ['USER']
password = os.environ['PASSWORD']
hostname = os.environ['HOSTNAME']
dbport = os.environ['DBPORT']
db = os.environ['DB']
save_messages_to_table = os.environ['REAL_MESSAGES_TABLE']


def connect():
    """"Connect to database using data from environment variables"""
    mydb = mysql.connector.connect(
        host=hostname, user=username, passwd=password, port=dbport,
        database=db, auth_plugin='caching_sha2_password')
    cursor = mydb.cursor(prepared=True)
    return mydb, cursor


def write_message(author, message, channel, server):
    mydb, cursor = connect()
    stmt = "INSERT INTO " + save_messages_to_table + " (author, message, channel, server) values (%s, %s, %s, %s)"
    cursor.execute(stmt, (author, message, channel, server))
    mydb.commit()
    cursor.close()
    mydb.close()