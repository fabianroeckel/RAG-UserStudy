import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page

def main():
    st.title('Welcome to the Human-Computer Interaction Study')
    st.markdown("""
    ###### Conducted by [Your Institution or Research Group]

    Welcome to our online experiment exploring the interaction with RAG-systems.

    **Instructions:**
    - Please provide accurate responses to the questions presented in each section.
    - Take your time to understand each question before responding.
    - Your responses will remain confidential and will only be used for research purposes.

    **Estimated Time:**
    The experiment is expected to take approximately [insert estimated time] minutes to complete.

    Thank you for your participation! Let's get started and contribute to advancements in HCI research.

    ---
    """)

    if st.button('Start Experiment'):
        if 'sessionID' not in st.session_state:
            sessionID = getSessionID()
            sampled_study_type = getSampledStudyType()
            sampled_study_type = "SingleSource"
            generateNewCSFFiles(sessionID,sampled_study_type)
            st.session_state['sessionID'] = sessionID

        if 'question_number' not in st.session_state:
            st.session_state["question_number"] = 0

        if 'sampled_study_type' not in st.session_state:
            st.session_state["sampled_study_type"] = sampled_study_type

        switch_page("initialquestions")

st.set_page_config(layout="wide")
main()
