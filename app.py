import streamlit as st
import database

st.title("Task Friction Tracker")
database.initialize_db()
st.write("Task List:")
st.selectbox("Select a task to view details", options=[task[1] for task in database.show_tasks()])
# st.write(database.show_tasks())

# Add tasks here
with st.form("Add Tasks:"):
    task_name = st.text_input("Task Name")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        database.add_task(task_name)
        st.write(f"Task '{task_name}' added.")