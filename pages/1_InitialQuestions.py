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
    with st.expander("What is a RAG-System?"):
        col_expl, col_video = st.columns([6, 4])
        with col_expl:
            st.markdown("**RAG**, which stands for **Retrieval-Augmented Generation**, is an AI framework designed to enhance the responses of large language models (LLMs) by incorporating real-time information from external databases or knowledge bases. This approach helps to ground the model's responses in accurate and current information, making them more reliable and contextually relevant. ")
            st.markdown("""
                #### How Does It Work? :
                - **Retrieval**: When you ask a question or make a request, the RAG system first searches through a vast external database to find relevant information. This process is similar to how you might use a search engine to find data on a particular topic. 
                - **Augmentation**: The information retrieved in the first step is then used to 'augment' the knowledge base of the LLM. Essentially, the model integrates this fetched data with its pre-existing knowledge. 
                - **Generation**: With an updated set of information, the LLM then generates a response that not only reflects its built-in knowledge but also includes and references the newly retrieved data.
                """
                )

        with col_video:
            st.image("media/rag_gif.gif")
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


