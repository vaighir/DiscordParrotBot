#!/usr/bin/env python3

import os
import mysql.connector

username = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
hostname = os.environ['MYSQL_HOSTNAME']
db_port = os.environ['MYSQL_PORT']
db = os.environ['MYSQL_DATABASE']
real_messages_table = os.environ['REAL_MESSAGES_TABLE']
dictionary_table = os.environ['DICTIONARY_TABLE']


def connect():
    """"Connect to database using data from environment variables"""
    mydb = mysql.connector.connect(
        host=hostname, user=username, passwd=password, port=db_port,
        database=db, auth_plugin='caching_sha2_password')
    cursor = mydb.cursor(prepared=True)
    return mydb, cursor


def write_message(author, message, channel, server):
    mydb, cursor = connect()
    stmt = "INSERT INTO " + real_messages_table + " (author, message, channel, server) values (%s, %s, %s, %s)"
    cursor.execute(stmt, (author, message, channel, server))
    mydb.commit()
    cursor.close()
    mydb.close()


def load_messages(author, server):
    mydb, cursor = connect()
    stmt = "SELECT message FROM " + real_messages_table + " WHERE author = %s and server = %s"
    cursor.execute(stmt, (author, server))
    posts = cursor.fetchall()
    cursor.close()
    mydb.close()
    return posts


def delete_messages_from_server(server):
    mydb, cursor = connect()
    stmt = "DELETE FROM " + real_messages_table + " WHERE server = %s"
    cursor.execute(stmt, (server,))
    mydb.commit()
    cursor.close()
    mydb.close()


def write_dictionary(key, dictionary):
    delete_dictionary(key)
    mydb, cursor = connect()
    stmt = "INSERT INTO " + dictionary_table + " (author, dictionary) values (%s, %s)"
    cursor.execute(stmt, (key, dictionary))
    mydb.commit()
    cursor.close()
    mydb.close()


def load_dictionary(key):
    mydb, cursor = connect()
    stmt = "SELECT dictionary FROM " + dictionary_table + " WHERE author = %s"
    cursor.execute(stmt, (key,))
    posts = cursor.fetchall()
    cursor.close()
    mydb.close()
    return posts


def delete_dictionary(key):
    mydb, cursor = connect()
    stmt = "DELETE FROM " + dictionary_table + " WHERE author = %s"
    cursor.execute(stmt, (key,))
    mydb.commit()
    cursor.close()
    mydb.close()