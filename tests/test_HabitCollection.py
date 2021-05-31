from habittracker.commands import create_new_habit, delete_habit, valid_habit_name, habit_in_habit_collection
import unittest
from habittracker.utils import connect_to_database, get_all_habits
from habittracker.Habit import Habit
from habittracker.HabitCollection import HabitCollection
from datetime import datetime, timedelta


class HabitCollectionTest(unittest.TestCase):

    # Act and assert
    def test_get_habit_by_name(self, searched_habit):
        test_habit_1 = Habit("test_habit_create", 4, datetime.now())
        test_habit_2 = Habit("Call mum", 4, datetime.now())
        test_habit_3 = Habit("Call mum", 5, datetime.now())
        test_habit_4 = Habit("Wash car", 7, datetime.now())
        habit_collection = HabitCollection([test_habit_1, test_habit_2])
        self.assertEqual(habit_collection._get_habit_by_name(test_habit_1), test_habit_1)
        self.assertEqual(habit_collection._get_habit_by_name(test_habit_2), test_habit_2)
        self.assertEqual(habit_collection._get_habit_by_name(test_habit_3), False)
        self.assertEqual(habit_collection._get_habit_by_name(test_habit_4), False)

    def test_get_open_tasks(self):
        # Arrange
        connection = connect_to_database("testing.db")
        habit_list = get_all_habits(connection)
        habit_collection = HabitCollection(habit_list)
        open_tasks_1 = """Workout
Wash dishes
Change bedding
Call mum"""
        open_tasks_2 = """Workout
Wash dishes
Change bedding
Call mum
test_habit_open"""
        open_tasks_3 = """Workout
Wash dishes
Change bedding
test_habit_open"""
        # Assert 1
        self.assertEqual(habit_collection.get_open_tasks(), open_tasks_1)
        # Arrange for 2
        create_new_habit(connection, "test_habit_open", 1, datetime.now() - timedelta(days=2))
        habit_list = get_all_habits(connection)
        habit_collection = HabitCollection(habit_list)
        # Assert for 2
        self.assertEqual(habit_collection.get_open_tasks(), open_tasks_2)
        # Arrange for 3
        call_mum_habit = habit_collection._get_habit_by_name("Call mum")
        call_mum_habit.confirm_task(connection)
        # Assert for 3
        self.assertEqual(habit_collection.get_open_tasks(), open_tasks_3)

    def test_get_habits_with_period(self, period: int):
        pass

    def test_get_longest_streak_for_habit(self, habit_name: str, connection):
        pass

    def test_get_current_longest_streak(self, connection):
        pass

    def test_get_tracked_habits(self):
        pass
