import streamlit as st
from datetime import datetime
import database

st.title("Task Friction Tracker")

# Add tasks here
with st.form("Add Tasks:"):
    task_name = st.text_input("Task Name")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        database.add_task(task_name)
        st.write(f"Task '{task_name}' added.")

database.initialize_db()
tasks = database.show_tasks()
task_name_to_id = {task[1]: task[0] for task in tasks}
st.write("Task List:")
selected_task_name = st.selectbox("Select a task", options=[task[1] for task in tasks])

selected_task_id = task_name_to_id[selected_task_name]

# Log task completion time here
# TODO: List the following limits of form entry in ReadMe
   # 1. Time cannot be set to precise minute. Round estimated completion time to nearest 5 minutes.
   # 2. Actual completion time cannot be before planned completion time.
   # 3. Hours are in 24-hour format.
   # 4. Both planned and actual completion times must be provided and cannot be in the past.

# Set planned completion time here
planned_date = st.date_input("Planned date")
planned_time = st.time_input("Planned time")
planned_datetime = datetime.combine(planned_date, planned_time)
planned_display = planned_datetime.strftime("%I:%M %p")
st.write("Planned time:", planned_display)

# Set actual completion time here
actual_date = st.date_input("Actual date")
actual_time = st.time_input("Actual time")
actual_datetime = datetime.combine(actual_date, actual_time)
actual_display = actual_datetime.strftime("%I:%M %p")
st.write(f"Actual completion time:", actual_display)

with st.form("Log Task Completion Time:"):
    completed = st.checkbox("Completed")
    submitted = st.form_submit_button("Log Completion Time")

    if submitted:
        database.log_completion_time(task_id=selected_task_id, planned_time=planned_datetime, actual_time=actual_datetime, is_complete=completed)
        st.write("Task completion time logged.")

# Debug code to show logged tasks
def display_logged_tasks():
    logs = database.show_task_logs()
    st.write("Logged Task Completions:")
    for log in logs:
        st.write(log)

display_logged_tasks()