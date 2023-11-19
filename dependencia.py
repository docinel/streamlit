import streamlit as st
import streamlit_authenticator as stauth
import re
from deta import Deta

DETA_KEY = 'e06njc5frug_uZ4w5WteUzrTktc9Wid6hSa5m2H7aPJk'

deta = Deta(DETA_KEY)

db = deta.Base('StreamlitAuth')


def insert_user(email, username, password):
    # date_joined = datetime.datetime.now()

    return db.put({'email': email, 'username': username, 'password': password})

# insert_user("docinel@gmail.com", "docinel", "123456")


def fetch_all_users():
    res = db.fetch()
    return res.items


# print(fetch_all_users())  
def get_user_by_email():
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


# print(get_user_by_email())

def get_user_by_username():
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames

# print(get_user_by_username())


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
if(re.search(regex,email)):
    return True
else:
    return False

def validate_username(username):
    regex = '^[a-zA-Z0-9]+$'
    if(re.search(regex,username)):
        return True
    else:
        return False


def sign_up():
    with st.form("sign_up", clear_on_submit=True):
        st.subheader(":green[Sign Up]") 
        email = st.text_input(":blue[Email]", placeholder="Enter your email")
        username = st.text_input(":blue[Username]", placeholder="Enter your username")
        password1 = st.text_input(":blue[Password]", type="password", placeholder="Enter your password")
        password2 = st.text_input(":blue[Confirm Password]", type="password", placeholder="Confirm your password")
        
        if email:
           if validate_email(email):
               if email not in get_user_by_email():
                   if validate_username(username):
                       if username not in get_user_by_username():
                           if len(username) >= 2:
                               if len(password1) >= 6:
                                   if password1 == password2:
                                       # Add User to DB
                                       hashed_password = stauth.Hasher([password2]).generate()
                                       insert_user(email, username, hashed_password[0])
                                       st.success('Account created successfully!!')
                                       st.balloons()
                                   else:
                                       st.warning('Passwords Do Not Match')
                               else:
                                   st.warning('Password is too Short')
                           else:
                               st.warning('Username Too short')
                       else:
                           st.warning('Username Already Exists')
                   else:
                       st.warning('Invalid Username')
               else:
                   st.warning('Email Already exists!!')
           else:
               st.warning('Invalid Email')
        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            st.form_submit_button('Sign Up')
