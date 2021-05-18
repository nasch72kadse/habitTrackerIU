#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from utils import isint
from Habit import Habit
from datetime import datetime


def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('clear')
    print("\t*****************************************************")
    print("\t***  Greetings! - Welcome to the Habit Tracker :) ***")
    print("\t*****************************************************")


def get_main_user_choice():
    # Let users know what they can do.
    print("\n[1] Create a new habit")
    print("[2] Delete a habit")
    print("[3] Analyze")
    print("[4] Confirm a task")
    return input("What would you like to do?")


def evaluate_main_user_choice(user_input, connection, habit_collection):
    if user_input == "1":
        create_new_habit(connection)
    elif user_input == "2":
        delete_habit(connection, habit_collection)
    elif user_input == "3":
        pass
    elif user_input == "4":
        pass
    else:
        return False


def get_analyze_choice(connection, habit_collection):
    # Let users know what they can do.
    print("\n[1] Show all open tasks")
    print("[2] Show all habits with a defined period")
    print("[3] Show the longest streak for a given habit")
    print("[4] Show the current longest streak")
    print("[5] Show all tracked habits")
    return input("What would you like to do?")


def evaluate_analyze_choice(user_input, connection, habit_collection):
    if user_input == "1":
        open_tasks = habit_collection.get_open_tasks()
        print(open_tasks)
    elif user_input == "2":
        period = get_valid_habit_period()
        habits_with_period = habit_collection.get_habits_with_period(period)
        print(habits_with_period)
    elif user_input == "3":
        habit_name = get_valid_habit_name()
        habit_with_longest_streak = habit_collection.get_longest_streak_for_habit(habit_name)
        print(habit_with_longest_streak)
    elif user_input == "4":
        habit_with_current_longest_streak = habit_collection.get_current_longest_streak()
        print(habit_with_current_longest_streak)
    elif user_input == "5":
        tracked_habits = habit_collection.get_tracked_habits()
        print(tracked_habits)
    else:
        return False


def create_new_habit(connection):
    habit_name = get_valid_habit_name()
    habit_days = get_valid_habit_period()
    created_date = datetime.now()
    new_habit = Habit(habit_name, habit_days, created_date)
    new_habit.create_habit_in_database(connection)
    print("Congrats! You created a new habit!")


def delete_habit(connection, habit_collection):
    habit_name = get_valid_habit_name()
    habit = habit_in_habit_collection(habit_name, habit_collection)
    if habit:
        habit.delete_habit_in_database()
        print("Deleted habit successfully")
        return True
    new_habit_name = input("Habit could not be found, enter a valid name or type \"exit\" to exit this mode")
    if new_habit_name == "exit":
        return False
    else:
        delete_habit(connection, habit_collection)


def get_valid_habit_name():
    habit_name = input("Please enter a valid habit name:")
    if habit_name != "" and len(habit_name) < 90:
        return habit_name
    else:
        return get_valid_habit_name()


def get_valid_habit_period():
    habit_period = input("Please enter a valid habit period:")
    if isint(habit_period):
        return habit_period
    else:
        return get_valid_habit_period()


def habit_in_habit_collection(habit_name, habit_collection):
    for habit in habit_collection:
        if habit.name == habit_name:
            return habit
    return False
