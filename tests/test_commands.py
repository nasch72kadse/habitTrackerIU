from habittracker.commands import create_new_habit, delete_habit, valid_habit_name, habit_in_habit_collection
import unittest
from habittracker.utils import connect_to_database, get_all_habits, close_connection_to_database
from habittracker.Habit import Habit
from habittracker.HabitCollection import HabitCollection
from datetime import datetime


class CommandsTest(unittest.TestCase):
    # Act and assert
    def test_create_new_habit(self):
        connection = connect_to_database("testing.db")
        self.assertEqual(create_new_habit(connection, "Call mum", 5), False)
        self.assertEqual(create_new_habit(connection, "Call dad", 5), True)
        close_connection_to_database(connection)

    def test_delete_habit(self):
        connection = connect_to_database("testing.db")
        habit_list = get_all_habits(connection)
        habit_collection = HabitCollection(habit_list)
        self.assertEqual(delete_habit(connection, habit_collection, "Call son"), False)
        self.assertEqual(delete_habit(connection, habit_collection, "Call dad"), True)
        close_connection_to_database(connection)

    def test_valid_habit_name(self):
        self.assertEqual(valid_habit_name(""), False)
        self.assertEqual(valid_habit_name("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut l"), False)
        self.assertEqual(valid_habit_name("Wash car"), True)

    def test_habit_in_habit_collection(self):
        new_habit = Habit("number_one", 1, datetime.now())
        new_habit_2 = Habit("number_two", 2, datetime.now())
        habit_collection = HabitCollection([new_habit, new_habit_2])
        self.assertEqual(habit_in_habit_collection("Call son", habit_collection), False)
        self.assertEqual(habit_in_habit_collection("number_one", habit_collection), new_habit)
        self.assertEqual(habit_in_habit_collection("number_two", habit_collection), new_habit_2)