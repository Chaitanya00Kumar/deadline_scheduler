import sqlite3 as sq
import os
import uuid
from datetime import datetime


db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workblocks.db")
conn = sq.connect(db_path)
cursor = conn.cursor()

#if __name__ == "__main__":
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workblocks (
        id INTEGER PRIMARY KEY,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        mins INTEGER NOT NULL
    )
""")

def insert_workblock(start_time, end_time)->None:

    mins = int((end_time - start_time).total_seconds() / 60)
    start_time = start_time.isoformat()
    end_time = end_time.isoformat()

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO workblocks (start_time, end_time, mins)
        VALUES (?, ?, ?)
    """, (start_time, end_time, mins))
    conn.commit()

def load_wbs() -> list:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, start_time, end_time, mins
            FROM workblocks
        """)
        rows = cursor.fetchall()

        workblocks = []

#         work_blocks = [
#     (datetime(2026,8,14,16,30), datetime(2026,8,14,19,0)),   # 4:30pm-7pm
#     (datetime(2026,8,14,21,0), datetime(2026,8,14,22,0)),   # 9pm-10pm
# ]
        for row in rows:
            wb_id, start_time, end_time, mins = row
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            workblocks.append((wb_id, start_time, end_time, mins))
        return workblocks

def close_base() -> None:
    conn.close()

conn.commit()