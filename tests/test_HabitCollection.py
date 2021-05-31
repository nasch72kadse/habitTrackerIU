from habittracker.commands import create_new_habit, delete_habit, valid_habit_name, habit_in_habit_collection
import unittest
from habittracker.utils import connect_to_database, get_all_habits
from habittracker.Habit import Habit
from habittracker.HabitCollection import HabitCollection
from datetime import datetime


class HabitTest(unittest.TestCase):

    # Act and assert
    def test_get_habit_by_name(self, searched_habit):
        pass
    def test_get_open_tasks(self):
        pass
    def test_get_habits_with_period(self, period: int):
        pass
    def test_get_longest_streak_for_habit(self, habit_name: str, connection):
        pass
    def test_get_current_longest_streak(self, connection):
        pass
    def test_get_tracked_habits(self):
        pass