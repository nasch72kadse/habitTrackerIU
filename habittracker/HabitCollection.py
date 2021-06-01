#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


class HabitCollection(object):
    def __init__(self, habits=None):
        if habits is None:
            habits = []
        self.habits = habits

    def _get_habit_by_name(self, searched_habit):
        """
        Search habit by name
        :param searched_habit: name of habit
        :return: return habit or False
        """
        for habit in self.habits:
            if habit.name == searched_habit:
                return habit
        return False

    def get_open_tasks(self):
        """
        Get all open tasks
        :return: String of open tasks separated by \n
        """
        task_string = ""
        current_time = datetime.now()
        for habit in self.habits:
            if current_time >= habit.next_task:
                task_string += habit.name + "\n"
        return task_string.strip("\n")

    def get_habits_with_period(self, period: int):
        """
        Get habits with a specified period
        :param period: period as int
        :return: habits as string separated by \n
        """
        habits_with_period_string = ""
        for habit in self.habits:
            if habit.days == period:
                habits_with_period_string += habit.name + "\n"
        return habits_with_period_string.strip("\n")

    def get_longest_streak_for_habit(self, habit_name: str, connection):
        """
        Get overall longest streak for a given habit
        :param habit_name: habit name
        :param connection: connection object
        :return: longest streak as int
        """
        habit = self._get_habit_by_name(habit_name)
        if habit:
            longest_streak = habit.get_overall_longest_streak(connection)
            return longest_streak
        else:
            return False

    def get_current_longest_streak(self, connection):
        """
        Get current longest streak from all habits as strings
        :param connection: connection object
        :return: habit name, longest streak as int
        """
        longest_streak = 0
        habit_name = "No habit"
        for habit in self.habits:
            habit_streak = habit.get_current_streak(connection)
            if habit_streak >= longest_streak:
                longest_streak = habit_streak
                habit_name = habit.name
        return habit_name, longest_streak

    def get_tracked_habits(self):
        """
        Get all habits separated by \n
        :return: habit string separated by \n
        """
        habit_string = ""
        for habit in self.habits:
            habit_string += habit.name + "\n"
        return habit_string.strip("\n")
