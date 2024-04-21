import streamlit as st
import streamlit_authenticator as stauth
# from streamlit_authenticator import Authenticate
import streamlit_option_menu
from streamlit_option_menu import option_menu

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# name, authenticaton_status, username = authenticator.login()
authenticator.login()


if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f"Bonjour *{st.session_state['name']}*")
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st .session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")


with st.sidebar:
    # if st.button("Home"):
    #     st.switch_page("app.py")
    # if st.button("Data Viz"):
    #     st.switch_page("pages/viz.py")
    # if st.button("Prediction"):
    #     st.switch_page("pages/pred.py")
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home", "Data Viz", "Prediction"],
        icons = ["house", "gear", "activity"],
        menu_icon = "cast",
        default_index = 0,
        # orientation = "horizontal",
    )

if selected == "Home":
    st.header("Page d'accueil")

if selected == "Data Viz":
    st.subheader(f"**You have selected {selected}**")

if selected == "Prediction":
    st.subheader(f"**You have selected {selected}**")
