import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('pomodoro.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            start_time TEXT,
                            end_time TEXT,
                            duration INTEGER,
                            completed BOOLEAN)''')
        self.conn.commit()

    def add_task(self, task_name):
        self.c.execute("INSERT INTO tasks (name, start_time, completed) VALUES (?, ?, ?)", 
                       (task_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), False))
        task_id = self.c.lastrowid
        self.conn.commit()
        return task_id

    def update_task(self, task_id, duration):
        self.c.execute("UPDATE tasks SET end_time = ?, duration = ?, completed = ? WHERE id = ?", 
                       (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), duration, True, task_id))
        self.conn.commit()

    def get_history(self):
        self.c.execute("SELECT * FROM tasks WHERE completed = ?", (True,))
        rows = self.c.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
