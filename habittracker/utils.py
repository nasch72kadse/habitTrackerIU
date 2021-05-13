#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3


def connect_to_database():
    con = sqlite3.connect('habit.db')
    return con


def close_connection_to_database(connection):
    connection.commit()
    connection.close()


def init_sqlite_table(database_name):
    # Create connection
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    # Execute SQL query
    sql = "CREATE TABLE user(" \
          "chat_id INTEGER PRIMARY KEY, " \
          "username TEXT, " \
          "password TEXT, " \
          "state TEXT)"
    cursor.execute(sql)
    connection.commit()
    # Close connection
    connection.close()


def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('clear')
    print("\t**********************************************")
    print("\t***  Greeter - Hello old and new friends!  ***")
    print("\t**********************************************")


def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Create a new habit")
    print("[2] Delete a habit")
    print("[3] Analyze")
    print("[4] Confirm a task")

    return input("What would you like to do? ")