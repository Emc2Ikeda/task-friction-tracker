import streamlit as st
import sqlite3

def connect_db(db_name='data/task_database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

# Creates task_logs and tasks tables if they do not exist
def create_tables(cursor):
    # Tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL
    )
    """)

    # Task logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        planned_completion_time TEXT,
        actual_completion_time TEXT,
        completed BOOLEAN,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    )
    """)

def initialize_db():
    conn, cursor = connect_db()
    create_tables(cursor)
    conn.commit()
    st.write("Database initialized and tables created if they did not exist.")
    return conn, cursor
 
if __name__ == "__main__":
    initialize_db()