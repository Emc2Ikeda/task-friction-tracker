import streamlit as st
import database as database

st.title("Hello, Streamlit!")
st.write("Welcome to your first Streamlit app.")
database.initialize_db()