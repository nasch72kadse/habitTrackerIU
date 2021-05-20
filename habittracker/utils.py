#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
from Habit import Habit
import datetime


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


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
    habit_data_list = get_all_habit_data(connection)
    habit_list = []
    for habit_data in habit_data_list:
        habit_name = habit_data[1]
        habit_days = habit_data[2]
        habit_created = habit_data[3]
        habit_next_task = habit_data[4]
        habit = Habit(habit_name, habit_days, parse_sqlite_date(habit_created), parse_sqlite_date(habit_next_task))
        habit_list.append(habit)
    return habit_list


def get_all_habit_data(connection):
    cursor = connection.cursor()
    habits = cursor.execute('SELECT * FROM Habit', ())
    habits = habits.fetchall()
    cursor.close()
    return habits


def parse_sqlite_date(sqlite_date):
    new_date = datetime.datetime.strptime(sqlite_date, "%Y-%m-%d %H:%M:%S.%f")
    return new_date
