#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import connect_to_database, close_connection_to_database, init_sqlite_table, check_file_existing, get_all_habits
from commands import get_main_user_choice, display_title_bar, evaluate_main_user_choice
from HabitCollection import HabitCollection

database_name = "habits.db"

# Start program
display_title_bar()

# Initialize database when database doesn't exist
if not check_file_existing(database_name):
    init_sqlite_table()

# Get DB connection
connection = connect_to_database()

# Get all habits and transform it into a habit collection
habit_list = get_all_habits()
habit_collection = HabitCollection(habit_list)

# Start program
display_title_bar()
while True:
    user_choice = get_main_user_choice()
    evaluate_main_user_choice(user_choice)


