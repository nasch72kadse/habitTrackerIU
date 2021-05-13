#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HabitCollection(object):
    def __init__(self, habits=None):
        if habits is None:
            habits = []
        self.habits = habits

    def get_open_tasks(self):
        pass

    def get_habits_with_period(self, period: int):
        pass

    def get_longest_streak_for_habit(self, habbit_name: str):
        pass

    def get_current_longest_streak(self):
        pass

    def get_tracked_habits(self):
        pass
