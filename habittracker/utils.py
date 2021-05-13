#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
from datetime import datetime


def connect_to_database(database_name):
    connection = sqlite3.connect(database_name)
    return connection


def close_connection_to_database(connection):
    connection.commit()
    connection.close()


def init_sqlite_table(database_name):
    # Create connection
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    # Execute SQL query
    sql_habit = "CREATE TABLE Habit(" \
                "id INTEGER PRIMARY KEY, " \
                "name varchar(45), " \
                "days INTEGER, " \
                "created_date Date, " \
                "next_task Date" \
                ")"
    sql_entries = "CREATE TABLE Entries(" \
                  "id INTEGER PRIMARY KEY, " \
                  "done_time Date, " \
                  "habit_id INTEGER , " \
                  "FOREIGN KEY (habit_id) REFERENCES Habit(id)" \
                  ")"
    cursor.execute(sql_habit)
    cursor.execute(sql_entries)
    connection.commit()
    # Close connection
    cursor.close()
    connection.close()


def check_file_existing(database_name):
    file_exists = os.path.isfile(database_name)
    return file_exists


def get_all_habits(connection):
    cursor = connection.cursor()
    sql = ""
    cursor.close()