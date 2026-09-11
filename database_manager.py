import sqlite3 as sq
import os
import uuid
from datetime import datetime


db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scheduler.db")
conn = sq.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        higher_id TEXT,
        parent_task_name TEXT,
        task_name TEXT NOT NULL,
        deadline TEXT NOT NULL,
        mins_dedicated INTEGER NOT NULL,
        overflowed INTEGER NOT NULL DEFAULT 0,
        completed INTEGER NOT NULL DEFAULT 0,
        completed_at TEXT
    )
""")

def insert_task(conn, higher_id, parent_task_name, task_name, deadline, mins_dedicated):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (higher_id, parent_task_name, task_name, deadline, mins_dedicated, overflowed, completed)
        VALUES (?, ?, ?, ?, ?, 0, 0)
    """, (higher_id, parent_task_name, task_name, deadline.isoformat(), mins_dedicated))
    conn.commit()

def load_tasks(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, higher_id, task_name, mins_dedicated, deadline
        FROM tasks
        WHERE overflowed = 0 AND completed = 0
    """)
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        task_id, higher_id, task_name, mins_dedicated, deadline_str = row
        deadline = datetime.fromisoformat(deadline_str)
        tasks.append((task_name, mins_dedicated, deadline, task_id, higher_id))
    return tasks

def mark_completed(conn, task_id, completed_datestamp):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET completed, completed_at = 1, ?
        WHERE id = ?
    """, (completed_datestamp, task_id))
    conn.commit()

def mark_overflow(conn, task_id):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET overflowed = 1
        WHERE id = ?
    """, (task_id,))
    conn.commit()

def remove_task(conn, task_id):
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))
    conn.commit()

conn.commit()
conn.close()