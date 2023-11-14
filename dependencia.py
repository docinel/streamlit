import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'e06njc5frug_uZ4w5WteUzrTktc9Wid6hSa5m2H7aPJk'

deta = Deta(DETA_KEY)

db = deta.Base('StreamlitAuth')

def insert_user(email, username, password):
    
    date_joined = datetime.datetime.now()

    return db.put({'email': email, 'username': username, 'password': password})

insert_user("docinel@gmail.com", "docinel", "123456")

def fetch_all_users():
    res = db.fetch()
    return res.items

def sign_uop():
    with st.form("sign_up", clear_on_submit=True):
        st.subheader(":green[Sign Up]") 
        email = st.text_input("Email", placeholder="Enter your email")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        submit = st.form_submit_button(label="Sign Up")
    # st.subheader("Sign Up", clear)
    # name = st.text_input("Name")
    # email = st.text_input("Email")
    # password = st.text_input("Password", type="password")
    # confirm_password = st.text_input("Confirm Password", type="password")
    # if st.button("Sign Up"):
    #     if password == confirm_password:
    #         st.success("You have successfully created a valid Account")
    #         st.balloons()
    #     else:
    #         st.error("Passwords do not match")