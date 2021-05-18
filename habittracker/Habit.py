#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


class Habit(object):
    def __init__(self, name: str, days: int, created_date: datetime, next_task=None):
        self.name = name
        self.days = days
        self.created_date = created_date
        self.next_task = next_task
        if not self.next_task:
            self.next_task = self._calculate_next_date_for_task(self.created_date)

    def _calculate_next_date_for_task(self, start_date):
        period = timedelta(days=self.days)
        buffer = timedelta(hours=20)  # 20 hours buffer to do the task after end of period
        return start_date + period + buffer

    def _calculate_last_date_for_task(self, start_date):
        period = timedelta(days=self.days)
        buffer = timedelta(hours=20)  # 20 hours buffer to do the task after end of period
        return start_date - period - buffer

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

    def delete_habit_in_database(self, connection):
        habit_id = self.get_habit_id(connection)
        if habit_id:
            return False
        # Build connection and insert habit
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Habit WHERE id=?", (habit_id,))
        cursor.execute("DELETE FROM Entries WHERE habit_id=?", (habit_id,))
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
        habit_entries = self.get_all_entries(connection)
        for habit_entry in habit_entries:
            tracking_time = habit_entry[1]
            # set initial time
            if not current_time:
                current_time = tracking_time
                continue
            # Now check for streak
            deadline = self._calculate_next_date_for_task(current_time)
            if tracking_time > deadline:
                current_streak = 0
            else:
                current_streak += 1
            # Check if current streak is the biggest
            if current_streak > longest_streak:
                longest_streak = current_streak
        return longest_streak

    def get_current_streak(self, connection):
        current_streak = 0
        habit_entries = self.get_all_entries(connection)
        # Sort entries in reverse to get the newest
        habit_entries.sort(key=lambda x: x[0], reverse=True)
        current_time = datetime.now()
        for habit_entry in habit_entries:
            tracking_time = habit_entry[1]
            deadline = self._calculate_last_date_for_task(current_time)
            if deadline > tracking_time:
                current_streak += 1
            else:
                break
        return current_streak
