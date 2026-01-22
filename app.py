import streamlit as st
from datetime import datetime
import database

st.title("Task Friction Tracker")
# Initialize the database
database.initialize_db()

# Add tasks here
with st.form("Add Tasks:"):
    task_name = st.text_input("Task Name")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        database.add_task(task_name)
        st.write(f"Task '{task_name}' added.")

# If the database is empty, prompt user to add tasks to prevent downstream errors.
tasks = database.show_tasks()
if not tasks:
    st.warning("No tasks found. Please add tasks to begin tracking.")
    st.stop()

task_name_to_id = {task[1]: task[0] for task in tasks}
st.write("Task List:")
selected_task_name = st.selectbox("Select a task", options=[task[1] for task in tasks])

selected_task_id = task_name_to_id[selected_task_name]

# Show task logs for the selected task
st.write(f"Logs for task: {selected_task_name}")
task_logs = database.show_task_logs_for_task(selected_task_id)
st.write(task_logs)

# Calculate and display completion rate
total_logs = len(task_logs)
completed_logs_sum = sum(1 for log in task_logs if log[4])
completed_task_logs = [log for log in task_logs if log[4]]
completion_rate = (completed_logs_sum / total_logs * 100) if total_logs > 0 else 0
st.write(f"Completion Rate: {completion_rate:.2f}%")

# Calculate and display average delay
if completed_task_logs:
    total_delay = 0
    for log in completed_task_logs:
        planned_time = database.parse_datetime(log[2])
        actual_time = database.parse_datetime(log[3])
        if planned_time and actual_time:
            delay = (actual_time - planned_time).total_seconds()
            total_delay += delay
    average_delay_seconds = total_delay / len(completed_task_logs)
    average_delay_minutes = average_delay_seconds / 60
    st.write(f"Average Delay: {average_delay_minutes:.2f} minutes")
else:
    st.write("Average Delay: N/A (no completed tasks)")

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

now = datetime.now()

with st.form("Log Task Completion Time:"):
    completed = st.checkbox("Completed")
    submitted = st.form_submit_button("Log Completion Time")
    # Check if entered time is valid. Stop submission and display error if invalid.
    if submitted:
        if planned_datetime < now:
            st.error("Planned completion time cannot be in the past.")
            st.stop()
        
        if completed and actual_datetime > now:
            st.error("Actual completion time cannot be in the future.")
            st.stop()
        
        # Eliminate actual time if task is not completed
        if not completed:
            actual_datetime = None
            st.write("Task not completed; actual time not logged.")

        database.log_completion_time(task_id=selected_task_id, planned_time=planned_datetime, actual_time=actual_datetime, is_complete=completed)
        st.write("Task completion time logged.")

# Debug code to show logged tasks
def display_logged_tasks():
    logs = database.show_task_logs()
    st.write("Logged Task Completions:")
    for log in logs:
        st.write(log)

display_logged_tasks()