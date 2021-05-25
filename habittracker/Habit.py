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
        """
        Calculate the next deadline for a task
        :param start_date: date to calculate from
        :return: deadline date for a task in the future
        """
        period = timedelta(days=self.days)
        return start_date + period

    def _calculate_next_date_for_task_with_buffer(self, start_date):
        """
        Calculate the next deadline for a task with a buffer
        :param start_date: date to calculate from
        :return: deadline date for a task in the future
        """
        period = timedelta(days=self.days)
        buffer = timedelta(hours=20)  # 20 hours buffer to do the task after end of period
        return start_date + period + buffer

    def _calculate_last_date_for_task_with_buffer(self, start_date):
        """
        Calculate the last deadline for a task
        :param start_date: date to calculate from
        :return: The last deadline for a task in the past
        """
        period = timedelta(days=self.days)
        buffer = timedelta(hours=20)  # 20 hours buffer to do the task after end of period
        return start_date - period - buffer

    def confirm_task(self, connection, entry_time=None):
        """
        Confirm a task for a habit
        :param connection: connection object
        :param entry_time: Optional date to calculate from
        :return:
        """
        cursor = connection.cursor()
        # Check if custom entry time has been defined
        if entry_time:
            time_now = entry_time
        else:
            time_now = datetime.now()
        next_task_date = self._calculate_next_date_for_task(time_now)
        habit_id = self.get_habit_id(connection)
        # Set entries in database
        cursor.execute("UPDATE Habit SET next_task=? WHERE id=?", (next_task_date, habit_id,))
        cursor.execute("INSERT INTO Entries VALUES (?,?,?)", (None, entry_time, habit_id))
        cursor.close()
        connection.commit()
        # Set entries in Habit
        self.next_task = next_task_date

    def create_habit_in_database(self, connection):
        """
        Create habit entry in database
        :param connection: connection object
        :return:
        """
        # Check if habit with the same name already exists
        if self.get_habit_id(connection):
            return False
        # Build connection and insert habit
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Habit VALUES (?,?,?,?,?)",
                       (None, self.name, self.days, self.created_date, self.next_task))
        cursor.close()
        connection.commit()

    def delete_habit_in_database(self, connection):
        """
        Delete habit in database
        :param connection: connection object
        :return:
        """
        habit_id = self.get_habit_id(connection)
        if habit_id:
            return False
        # Build connection and insert habit
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Habit WHERE id=?", (habit_id,))
        cursor.execute("DELETE FROM Entries WHERE habit_id=?", (habit_id,))
        cursor.close()
        connection.commit()

    def get_habit_id(self, connection):
        """
        Get habit id in database
        :param connection: connection object
        :return: habit id from database
        """
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM Habit WHERE name=?', (self.name,))
        habit_id = cursor.fetchone()
        if habit_id:
            habit_id = habit_id[0]
        cursor.close()
        connection.commit()
        return habit_id

    def get_all_entries(self, connection):
        """
        Get all entries for habit
        :param connection: connection object
        :return: entries as list
        """
        cursor = connection.cursor()
        habit_entries = cursor.execute('SELECT * FROM Entries WHERE habit_id=?', (self.get_habit_id(connection),))
        habit_entries = habit_entries.fetchall()
        cursor.close()
        # Order entries by time
        habit_entries.sort(key=lambda x: x[0], reverse=False)
        return habit_entries

    def get_overall_longest_streak(self, connection):
        """
        Calculate the overall longest streak for current habit
        :param connection: connection object
        :return: amount of days as int
        """
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
            deadline = self._calculate_next_date_for_task_with_buffer(current_time)
            if tracking_time >= deadline:
                current_streak = 0
            else:
                current_streak += 1
            # Check if current streak is the biggest
            if current_streak > longest_streak:
                longest_streak = current_streak
        return longest_streak

    def get_current_streak(self, connection):
        """
        Get current streak as int
        :param connection: connection object
        :return: streak as int
        """
        current_streak = 0
        habit_entries = self.get_all_entries(connection)
        # Sort entries in reverse to get the newest
        habit_entries.sort(key=lambda x: x[0], reverse=True)
        current_time = datetime.now()
        for habit_entry in habit_entries:
            tracking_time = habit_entry[1]
            deadline = self._calculate_last_date_for_task_with_buffer(current_time)
            if deadline >= tracking_time:
                current_streak += 1
            else:
                break
        return current_streak
