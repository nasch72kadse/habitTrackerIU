from habittracker import utils
from habittracker.Habit import Habit
from datetime import datetime, timedelta
import os


def prepare():
    # Prepare connection and set startup parameters
    db_name = "testing.db"
    connection = prepare_connection(db_name)
    start_datetime = datetime.strptime("2021-01-01 12:00:00.76", "%Y-%m-%d %H:%M:%S.%f")
    end_datetime = start_datetime + timedelta(days=28)  # Only create example data for 4 weeks
    # Create data examples
    create_habit_examples(connection, start_datetime)
    habit_collection = utils.get_all_habits(connection)
    create_habit_entries(connection, habit_collection, end_datetime)


def prepare_connection(db_name):
    """
    :param db_name: name of the database
    :return: connection object
    Removes existing database and initialize a new one
    """
    if utils.check_file_existing(db_name):
        os.remove(db_name)
    utils.init_sqlite_table(db_name)
    connection = utils.connect_to_database(db_name)
    return connection


def create_habit_examples(connection, start_datetime):
    # Prepare examples
    habit_1 = Habit("Workout", 3, start_datetime)
    habit_2 = Habit("Learn", 1, start_datetime)
    habit_3 = Habit("Wash dishes", 2, start_datetime)
    habit_4 = Habit("Change bedding", 7, start_datetime)
    habit_5 = Habit("Call mum", 4, start_datetime)
    habit_1.create_habit_in_database(connection)
    habit_2.create_habit_in_database(connection)
    habit_3.create_habit_in_database(connection)
    habit_4.create_habit_in_database(connection)
    habit_5.create_habit_in_database(connection)


def create_habit_entries(connection, habits, end_datetime):
    for habit in habits:
        # While the next confirmation for habit is smaller than 4 weeks from the start date, continue confirming
        while habit.next_task < end_datetime:
            next_time = habit.next_task
            habit.confirm_task(connection, entry_time=next_time)

prepare()