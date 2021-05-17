#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


class Habit(object):
    def __init__(self, name: str, days: int, created_date: datetime, next_task: datetime):
        self.name = name
        self.days = days
        self.created_date = created_date
        self.next_task = next_task

    def _calculate_next_date_for_task(self, start_date):
        period = timedelta(days=self.days)
        buffer = timedelta(hours=20)  # 20 hours buffer to do the task after end of period
        return start_date + period + buffer

    def confirm_task(self, connection):
        cursor = connection.cursor()
        time_now = datetime.now()
        next_task_date = self._calculate_next_date_for_task(time_now)
        habit_id = self.get_habit_id(connection)
        # Set entries in database
        cursor.execute("UPDATE Habit SET next_task=? WHERE id=?", (next_task_date, habit_id,))
        cursor.execute("INSERT INTO Entries VALUES (?,?,?)", (None, datetime.now(), habit_id))
        cursor.close()
        connection.commit()
        # Set entries in Habit
        self.next_task = next_task_date

    def create_habit_in_database(self, connection):
        # Check if habit with the same name already exists
        if self.get_habit_id(connection):
            return False
        # Build connection and insert habit
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Habit VALUES (?,?,?,?,?)", (None, self.name, self.days, self.created_date, self.next_task))
        cursor.close()
        connection.commit()

    def create_task_entry_in_database(self, connection):
        cursor = connection.cursor()
        date = datetime.now()
        habit_id = self.get_habit_id(connection)
        cursor.execute("INSERT INTO Entries VALUES (?,?)", (date, habit_id,))
        cursor.close()
        connection.commit()

    def get_habit_id(self, connection):
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM Habit WHERE name=?', (self.name,))
        habit_id = cursor.fetchone()
        if habit_id:
            habit_id = habit_id[0]
        cursor.close()
        connection.commit()
        return habit_id

    def task_due(self):
        now = datetime.now()
        if self.next_task <= now:
            return True
        else:
            return False

    def get_all_entries(self, connection):
        cursor = connection.cursor()
        habit_entries = cursor.execute('SELECT * FROM Entries WHERE habit_id=?', (self.get_habit_id(),))
        habit_entries = habit_entries.fetchall()
        cursor.close()
        # Order entries by time
        habit_entries.sort(key=lambda x: x[0], reverse=False)
        return habit_entries

    def get_overall_longest_streak(self, connection):
        longest_streak = 0
        current_streak = 0
        current_time = None
        habit_id = self.get_habit_id()
        habit_entries = self.get_all_entries()
        for habit_entry in habit_entries:
            tracking_time = habit_entry[1]
            # set initial time
            if not current_time:
                current_time = tracking_time
            # Check if current streak is the biggest
            if current_streak > longest_streak:
                longest_streak = current_streak

    def get_current_streak(self, connection):
        current_streak = 0