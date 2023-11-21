import streamlit as st
import streamlit_authenticator as stauth
from loginauth import sign_up, fetch_all_users

st.set_page_config(page_title="Sign Up", page_icon=":green_book:", initial_sidebar_state="collapsed")

try:
    users = fetch_all_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {
        'usernames': {}
    }

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {
            'email': emails[index],
            'password': passwords[index]
        }

    authenticator = stauth.Authenticate(credentials, 'myapp', 'abcdef', cookie_expiry_days=4)

    email, authentication_status, username = authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            if authentication_status:
                st.subheader('This is home page')
                st.markdown("""
                Created by:
                            - [Rodrigo Docinel](https://github.com/rodrigodocinel)                
""")
                st.sidebar(f"Welcome {username}")
                authenticator.logout('Logout', 'sidebar')
            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')

    else:
        with info:
            st.warning('Please feed in your credentials')

except Exception as e:
    st.error(e)
    st.error('Refresh Page')
