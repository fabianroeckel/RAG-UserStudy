import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.header("What is your job in this study?")





if st.button('Start with the Experiment'):
    switch_page("Userstudy")