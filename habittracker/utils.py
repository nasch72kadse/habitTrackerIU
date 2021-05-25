#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
from .Habit import Habit
import datetime


def isint(value):
    """
    Check if value can be converted to int
    :param value: input value
    :return: True/False
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def connect_to_database(database_name):
    """
    Get connection object by database name
    :param database_name: database name
    :return: connection object
    """
    connection = sqlite3.connect(database_name)
    return connection


def close_connection_to_database(connection):
    """
    Commit and close connection
    :param connection: connection object
    :return:
    """
    connection.commit()
    connection.close()


def init_sqlite_table(database_name):
    """
    Create database and initialize all tables
    :param database_name: name of database
    :return:
    """
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


def check_file_existing(file_name):
    """
    Check if file exists
    :param file_name: name of file
    :return: True/False
    """
    file_exists = os.path.isfile(file_name)
    return file_exists


def get_all_habits(connection):
    """
    Get all habits as list
    :param connection: connection list
    :return: habits as list
    """
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
    """
    Get all habit data by SQL query
    :param connection: connection object
    :return: List of habits unformatted
    """
    cursor = connection.cursor()
    habits = cursor.execute('SELECT * FROM Habit', ())
    habits = habits.fetchall()
    cursor.close()
    return habits


def parse_sqlite_date(sqlite_date):
    """
    Parse string from SQLite database to datetime
    :param sqlite_date: datetime from database
    :return: datetime object
    """
    new_date = datetime.datetime.strptime(sqlite_date, "%Y-%m-%d %H:%M:%S.%f")
    return new_date
