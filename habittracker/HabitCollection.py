#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class HabitCollection(object):
    def __init__(self, habits=None):
        if habits is None:
            habits = []
        self.habits = habits

    def _get_habit_by_name(self, searched_habit):
        for habit in self.habits:
            if habit.name == searched_habit:
                return habit
        return False

    def get_open_tasks(self):
        task_string = ""
        current_time = datetime.now()
        for habit in self.habits:
            if current_time >= habit.next_task:
                task_string += habit.name + "\n"
        return task_string

    def get_habits_with_period(self, period: int):
        habits_with_period_string = ""
        for habit in self.habits:
            if habit.days == period:
                habits_with_period_string += habit.name
        return habits_with_period_string

    def get_longest_streak_for_habit(self, habit_name: str, connection):
        habit = self._get_habit_by_name(habit_name)
        longest_streak = habit.get_overall_longest_streak(connection)
        return longest_streak

    def get_current_longest_streak(self, connection):
        longest_streak = 0
        habit_name = "No habit"
        for habit in self.habits:
            habit_streak = habit.get_current_streak(connection)
            if habit_streak >= longest_streak:
                longest_streak = habit_streak
                habit_name = habit.name
        return habit_name, longest_streak

    def get_tracked_habits(self):
        habit_string = ""
        for habit in self.habits:
            habit_string += habit.name + "\n"
        return habit_string
