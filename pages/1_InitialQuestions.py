import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
from datetime import datetime


def demographic_questions():
    st.title('Demographic Information')
    age = st.number_input('What is your age?', min_value=18, max_value=120)
    gender = st.selectbox('What is your gender?', ['Male', 'Female', 'Other'])
    education = st.selectbox('What is your level of education?',
                             ['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Other'])

    return age, gender, education


def similar_systems_experience():
    st.title('Experience with RAG Systems')
    rag_experience = st.selectbox('Have you ever used a RAG system before?', ['Yes', 'No'])
    system_usage_frequency = st.selectbox('How often do you use similar applications or systems?',
                                          ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never'])

    return rag_experience, system_usage_frequency


def language_level():
    st.title('Language Level')
    proficiency = st.selectbox('How would you rate your proficiency with the language of the system?',
                               ['Beginner', 'Intermediate', 'Advanced', 'Native Speaker'])

    return proficiency






st.write(st.session_state.sessionID)
st.header('Welcome to the Experiment!')
st.write('Please provide some demographic information before starting the experiment.')

age, gender, educations = demographic_questions()
rag_experience, system_usage_frequency = similar_systems_experience()
proficiency = language_level()
general_questions_completed = False

st.write('Thank you for providing the information. You may proceed with the experiment now.')
if st.button('Start with the Experiment'):
    if "timestamp" not in st.session_state:
        st.session_state["timestamp"] = datetime.now()
    switch_page("userstudy")


