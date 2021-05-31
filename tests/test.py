#!/usr/bin/env python
# -*- coding: utf-8 -*-
from habittracker.utils import connect_to_database, init_sqlite_table, check_file_existing
from habittracker.commands import get_main_user_choice, display_title_bar, evaluate_main_user_choice

database_name = "testing.db"

# Start program
display_title_bar()

# Initialize database when database doesn't exist
if not check_file_existing(database_name):
    init_sqlite_table(database_name)

# Get DB connection
connection = connect_to_database(database_name)

# Start program
display_title_bar()
while True:
    user_choice = get_main_user_choice()
    evaluate_main_user_choice(user_choice, connection)
