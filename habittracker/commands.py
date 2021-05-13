#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('clear')
    print("\t*****************************************************")
    print("\t***  Greetings! - Welcome to the Habit Tracker :) ***")
    print("\t*****************************************************")


def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Create a new habit")
    print("[2] Delete a habit")
    print("[3] Analyze")
    print("[4] Confirm a task")

    return input("What would you like to do? ")


def evaluate_user_choice(user_input):
    if user_input == "1":
        pass
    elif user_input == "2":
        pass
    elif user_input == "3":
        pass
    elif user_input == "4":
        pass
    else:
        return False