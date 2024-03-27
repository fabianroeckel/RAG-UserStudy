import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")
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
        if 'key' not in st.session_state:
            sessionID = getSessionID()
            sessionID = getCachedSessionID()
            generateNewCSFFiles(sessionID)
            st.session_state['sessionID'] = sessionID
            st.session_state["question_number"] = 0
            st.write(st.session_state.sessionID)
        switch_page("initialquestions")
main()
