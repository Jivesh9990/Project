import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import Setting

def open_db():
    engine = create_engine('sqlite:///db.sqlite3') # load the database
    Session = sessionmaker(bind=engine)
    return Session()



st.title("Welcome to Project")
options = ['instructions','settings','run program']
choice = st.selectbox("choose option",options)
if choice =='instructions':
    st.subheader('view instructions')
if choice =='settings':
    st.subheader('view settings')
if choice =='run program':
    st.subheader('run program')