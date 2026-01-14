import sqlite3

def connect_db(db_name='data/task_database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

# TODO: Check if data type for planned and completed time is appropriate
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
    return conn, cursor

##########################################
#### CRUD operations for tasks table #####
##########################################

# Create a new task
def add_task(task_name):
    conn, cursor = connect_db()
    try:    
        cursor.execute(
            "INSERT INTO tasks (task_name) VALUES (?)",
            (task_name,)
        )
        conn.commit()
    finally:
        conn.close()

# Read all tasks
def show_tasks():
    conn, cursor = connect_db()
    try:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    finally:
        conn.close()
    return tasks

##########################################
#### CRUD operations for tasks log #######
##########################################
def log_completion_time(task_id, planned_time, actual_time, is_complete):
    conn, cursor = connect_db()

    # Convert datetimes to TEXT
    planned_str = planned_time.isoformat() if planned_time else None
    actual_str = actual_time.isoformat() if actual_time else None

    try:
        cursor.execute("""
            INSERT INTO task_logs (
                task_id, 
                planned_completion_time,
                actual_completion_time, 
                completed
            ) VALUES (?, ?, ?, ?)
        """, (task_id, planned_str, actual_str, is_complete))

        conn.commit()
    finally:
        conn.close()

def show_task_logs():
    conn, cursor = connect_db()
    try:
        cursor.execute("SELECT * FROM task_logs")
        logs = cursor.fetchall()
    finally:
        conn.close()
    return logs