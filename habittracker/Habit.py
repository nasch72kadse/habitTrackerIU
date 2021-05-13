#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class Habit(object):
    def __init__(self, name: str, days: int, streak: int, highest_streak: int, created_date: datetime, next_task: datetime):
        self.name = name
        self.days = days
        self.streak = streak
        self.highest_streak = highest_streak
        self.created_date = created_date
        self.next_task = next_task

    def _calculate_next_date_for_task(self, date: datetime):
        pass

    def confirm_task(self):
        pass
