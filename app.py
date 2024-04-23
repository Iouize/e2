import streamlit as st
import streamlit_authenticator as stauth
# from streamlit_authenticator import Authenticate
import streamlit_option_menu
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

import yaml
from yaml.loader import SafeLoader

from utils import train, test, plot_distrib_target, plot_numerical_features, plot_categorical_features, plot_count_plot_by_target, plot_kde_by_target
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
        st.write("Dataframe :")
        st.dataframe(data=train, height=200)
        st.write(f"La taille du dataset est de {train.shape}")

        st.subheader("Distribution de la target: outcome")
        target_fig = plot_distrib_target(train, 'outcome')
        st.pyplot(target_fig)


    if selected == "Data Viz":
        st.header("Visualisation des données")

        tab1, tab2 = st.tabs(["Train vs Test", "Distributions des features"])

        with tab1:

            tab1.subheader("Différence de distribution des valeurs numériques entre train et test")
            distrib_num_features = plot_numerical_features(train, test)
            tab1.pyplot(distrib_num_features)

            tab1.subheader("Différence de distribution des valeurs catégorielles entre train et test")
            distrib_cat_features = plot_categorical_features(train, test)
            tab1.pyplot(distrib_cat_features)

        with tab2:
            tab2.subheader("Distribution des valeurs catégorielles par outcome")
            cat_features = test.select_dtypes(include=['object']).columns.to_list()
            for feature in cat_features:
                fig = plot_count_plot_by_target(train, feature, 'outcome')
                tab2.plotly_chart(fig, use_container_width=True)

            tab2.subheader("Distribution des valeurs numériques par outcome")
            num_features = train.select_dtypes(include=['int64', 'float64']).columns.to_list()
            for feature in num_features:
                fig = plot_kde_by_target(train, feature, 'outcome')
                tab2.pyplot(fig, use_container_width=True)

    if selected == "Prediction":
        st.header("Prédiction")


elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st .session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
