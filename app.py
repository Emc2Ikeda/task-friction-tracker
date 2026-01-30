import streamlit as st
from datetime import datetime
import database
from insights import get_completion_rate, get_average_delay, show_friction_classification

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

completion_rate = get_completion_rate(selected_task_id)
st.write(f"Completion Rate: {completion_rate*100:.2f}%")

# Calculate and display average delay
average_delay_minutes = get_average_delay(selected_task_id)
if average_delay_minutes is not None:
    st.write(f"Average Delay: {average_delay_minutes:.2f} minutes")
else:
    st.write("Average Delay: N/A (no completed tasks)")

# Log task completion time here

# Set planned completion time here
planned_date = st.date_input("Planned date")
planned_time = st.time_input("Planned time")
planned_datetime = datetime.combine(planned_date, planned_time)
planned_display = planned_datetime.strftime("%I:%M %p")
st.write("Planned time:", planned_display)

# Predict whether the planned task is likely to be completed on time based on historical data.
if st.button("Predict task friction"):
    prediction = show_friction_classification(task_id=selected_task_id)
    st.write("AI Prediction:")
    st.write(prediction)

# Set actual completion time here
actual_date = st.date_input("Actual date")
actual_time = st.time_input("Actual time")
actual_datetime = datetime.combine(actual_date, actual_time)
actual_display = actual_datetime.strftime("%I:%M %p")
st.write(f"Actual completion time:", actual_display)

now = datetime.now()

# Predict whether the planned task is likely to be completed on time based on historical data.
if st.button("Predict task friction"):
    prediction = predict_task_completion(task_id=selected_task_id, planned_time=planned_datetime)
    st.write("AI Prediction:")
    st.write(prediction)

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