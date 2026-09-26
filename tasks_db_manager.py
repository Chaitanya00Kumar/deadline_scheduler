import sqlite3 as sq
import os
import uuid
from datetime import datetime


db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scheduler.db")
conn = sq.connect(db_path)
cursor = conn.cursor()

#if __name__ == "__main__":
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
        workblock_id INTEGER NOT NULL,
        completed_at TEXT
    )
""")

def insert_task(higher_id, parent_task_name, task_name, deadline, mins_dedicated)->int:

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (higher_id, parent_task_name, task_name, deadline, mins_dedicated, overflowed, completed, completed_at, workblock_id)
        VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0)
    """, (higher_id, parent_task_name, task_name, deadline.isoformat(), mins_dedicated))
    conn.commit()
    lastid = cursor.lastrowid
    #conn.close()
    return lastid

def load_tasks()-> list:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, higher_id, task_name, mins_dedicated, deadline, parent_task_name
            FROM tasks
            WHERE overflowed = 0 AND completed = 0
        """)
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task_id, higher_id, task_name, mins_dedicated, deadline_str, parent_task_name = row
            deadline = datetime.fromisoformat(deadline_str)
            tasks.append((task_name, mins_dedicated, deadline, task_id, higher_id, parent_task_name))
            #(task_name, min_dedicated, deadline, task_id, higher_id, parent_task_name)
            #conn.close()
        return tasks

def mark_completed(task_id, completed_datestamp)->None:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET completed = 1, completed_at = ?
            WHERE id = ?
        """, (completed_datestamp, task_id))
        conn.commit()
        #conn.close()

def assign_workblock(task_id, workblock_id)->None:
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET workblock_id = ?
        WHERE id = ?
        """, (workblock_id, task_id))
    conn.commit()

def mark_overflow(task_id)->None:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET overflowed = 1
            WHERE id = ?
        """, (task_id,))
        conn.commit()
        #conn.close()

def remove_task(task_id)->None:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM tasks
            WHERE id = ?
        """, (task_id,))
        conn.commit()
        #conn.close()

def close_base() -> None:
    conn.close()

conn.commit()
#conn.close()