import streamlit as st
import streamlit_authenticator as stauth
# from streamlit_authenticator import Authenticate
import streamlit_option_menu
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

import yaml
from yaml.loader import SafeLoader

from data_app import train, test

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
        authenticator.logout()

    if selected == "Home":
        st.header("Page d'accueil")
        st.write("Projet basé sur la compétition Kaggle [Predict Health Outcomes of Horses](https://www.kaggle.com/competitions/playground-series-s3e22)")
        st.write("Notebook d'origine : [notebook](https://www.kaggle.com/code/yoshifumimiya/s3e22-randomforest-ver-1)")

    if selected == "Data Viz":
        st.header("Visualisation des données")
        st.write("Dataframe :")
        st.dataframe(data=train, height=200)
        st.write(f"La taille du dataset est de {train.shape}")

        st.subheader("Distribution de la target: outcome")
        fig, ax = plt.subplots()
        ax.pie(
            train["outcome"].value_counts(),
            autopct='%.1f%%',
        )
        ax.legend(train["outcome"].value_counts().index.tolist(), loc='upper left', bbox_to_anchor=(1, 1))

        st.pyplot(fig)

    if selected == "Prediction":
        st.header("Prédiction")




elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st .session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
