import streamlit as st
import database

st.title("Task Friction Tracker")
database.initialize_db()
st.write("Task List:")
st.write(database.show_tasks())