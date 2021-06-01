import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
import unittest
from habittracker.utils import connect_to_database, close_connection_to_database
from habittracker.Habit import Habit
from datetime import datetime


class HabitTest(unittest.TestCase):
    def test_create_habit_in_database(self):
        connection = connect_to_database("testing.db")
        test_habit_1 = Habit("test_habit_create", 4, datetime.now())
        test_habit_2 = Habit("Call mum", 4, datetime.now())
        self.assertEqual(test_habit_1.create_habit_in_database(connection), True)
        self.assertEqual(test_habit_2.create_habit_in_database(connection), False)
        # Cleanup
        test_habit_1.delete_habit_in_database(connection)
        close_connection_to_database(connection)

    def test_confirm_task(self):
        connection = connect_to_database("testing.db")
        # First test case = new habit
        # Create values
        test_habit_1 = Habit("test_habit_ct", 4, datetime.now())
        test_habit_1.create_habit_in_database(connection)
        # Test
        first_value = test_habit_1.get_current_streak(connection)
        test_habit_1.confirm_task(connection)
        self.assertEqual(test_habit_1.get_current_streak(connection), first_value + 1)
        test_habit_1.confirm_task(connection)
        self.assertEqual(test_habit_1.get_current_streak(connection), first_value + 2)
        # Second test case = existing habit
        test_habit_2 = Habit("Learn", 1, datetime.now())
        first_value = test_habit_2.get_current_streak(connection)
        test_habit_2.confirm_task(connection)
        self.assertEqual(test_habit_2.get_current_streak(connection), first_value + 1)
        test_habit_2.confirm_task(connection)
        self.assertEqual(test_habit_2.get_current_streak(connection), first_value + 2)
        # Cleanup
        test_habit_1.delete_habit_in_database(connection)
        close_connection_to_database(connection)

    def test_delete_habit_in_database(self):
        connection = connect_to_database("testing.db")
        test_habit_1 = Habit("test_habit_delete", 4, datetime.now())
        test_habit_1.create_habit_in_database(connection)
        test_habit_2 = Habit("Call sister", 4, datetime.now())
        # Assert
        self.assertEqual(test_habit_1.delete_habit_in_database(connection), True)
        self.assertEqual(test_habit_2.delete_habit_in_database(connection), False)
        close_connection_to_database(connection)

    def test_get_overall_longest_streak(self):
        connection = connect_to_database("testing.db")
        test_habit_1 = Habit("Workout", 4, datetime.now())
        test_habit_2 = Habit("Wash dishes", 4, datetime.now())
        test_habit_3 = Habit("test_habit_3", 4, datetime.now())
        self.assertEqual(test_habit_1.get_overall_longest_streak(connection), 9)
        self.assertEqual(test_habit_2.get_overall_longest_streak(connection), 13)
        self.assertEqual(test_habit_3.get_overall_longest_streak(connection), 0)
        close_connection_to_database(connection)

    def test_get_current_streak(self):
        connection = connect_to_database("testing.db")
        test_habit_1 = Habit("Workout", 4, datetime.now())
        test_habit_2 = Habit("Wash dishes", 4, datetime.now())
        test_habit_3 = Habit("test_habit_3", 4, datetime.now())
        self.assertEqual(test_habit_1.get_overall_longest_streak(connection), 9)
        self.assertEqual(test_habit_2.get_overall_longest_streak(connection), 13)
        self.assertEqual(test_habit_3.get_overall_longest_streak(connection), 0)
        close_connection_to_database(connection)
