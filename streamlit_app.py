import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
import streamlit_js_eval
import httpagentparser

def check_for_browser():
    browser = httpagentparser.detect(streamlit_js_eval.get_user_agent())["browser"]["name"]
    return browser

def main():
    browser = check_for_browser()
    if browser == "Firefox":
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
                st.session_state['sessionID'] = sessionID

            if 'question_number' not in st.session_state:
                st.session_state["question_number"] = 0

            if 'sampled_study_type' not in st.session_state:
                sampled_study_type = getSampledStudyType()
                sampled_study_type = "SingleSource"
                st.session_state["sampled_study_type"] = sampled_study_type
                generateNewCSFFiles(sessionID, sampled_study_type)

            if "source_name" not in st.session_state:
                st.session_state["source_name"] = ""

            if "source_clicks1" not in st.session_state:
                st.session_state["source_clicks1"] = 0
                st.session_state["source_clicks2"] = 0
                st.session_state["source_clicks3"] = 0
                st.session_state["source_clicks4"] = 0
                st.session_state["total_source_clicks"] = 0

            if "source_watch_time1_datetime" not in st.session_state:
                st.session_state["last_clicked_source"] = 0
                st.session_state["source_watch_time1_datetime"] = 0
                st.session_state["source_watch_time2_datetime"] = 0
                st.session_state["source_watch_time3_datetime"] = 0
                st.session_state["source_watch_time4_datetime"] = 0

                st.session_state["source_watch_time1"] = 0
                st.session_state["source_watch_time2"] = 0
                st.session_state["source_watch_time3"] = 0
                st.session_state["source_watch_time4"] = 0
                st.session_state["total_watch_time"] = 0

            if "task_completion_time" not in st.session_state:
                st.session_state["task_completion_time"] =  0

            switch_page("consentToParticipate")
    else:
        st.title('Welcome to the Human-Computer Interaction Study')
        st.markdown("""
                ###### Conducted by [Your Institution or Research Group]

                Welcome to our online experiment exploring the interaction with RAG-systems.

                **Instructions:**
                
                Unfortunately, it seems you're using a browser other than Firefox, which is required for this study. To proceed, please follow these instructions:
                
                1. Download and install Firefox browser from the official website: [Firefox Download Page](https://www.mozilla.org/en-US/firefox/new/)
                2. Once Firefox is installed, please close your current browser and open the study link again using Firefox.
                3. You will then be able to participate in the study.
                
                Please ensure you're using Firefox as instructed to ensure the validity of the study results.

                Thank you for your participation! Let's get started and contribute to advancements in HCI research.

                ---
                """)
        with st.expander("Start Experiment: usually not displayed only for testing"):
            if st.button('Start Experiment'):
                if 'sessionID' not in st.session_state:
                    sessionID = getSessionID()
                    st.session_state['sessionID'] = sessionID

                if 'question_number' not in st.session_state:
                    st.session_state["question_number"] = 0

                if 'sampled_study_type' not in st.session_state:
                    sampled_study_type = getSampledStudyType()
                    sampled_study_type = "SingleSource"
                    st.session_state["sampled_study_type"] = sampled_study_type
                    generateNewCSFFiles(sessionID, sampled_study_type)

                if "source_name" not in st.session_state:
                    st.session_state["source_name"] = ""

                if "source_clicks1" not in st.session_state:
                    st.session_state["source_clicks1"] = 0
                    st.session_state["source_clicks2"] = 0
                    st.session_state["source_clicks3"] = 0
                    st.session_state["source_clicks4"] = 0
                    st.session_state["total_source_clicks"] = 0

                if "source_watch_time1_datetime" not in st.session_state:
                    st.session_state["last_clicked_source"] = 0
                    st.session_state["source_watch_time1_datetime"] = 0
                    st.session_state["source_watch_time2_datetime"] = 0
                    st.session_state["source_watch_time3_datetime"] = 0
                    st.session_state["source_watch_time4_datetime"] = 0

                    st.session_state["source_watch_time1"] = 0
                    st.session_state["source_watch_time2"] = 0
                    st.session_state["source_watch_time3"] = 0
                    st.session_state["source_watch_time4"] = 0
                    st.session_state["total_watch_time"] = 0

                if "task_completion_time" not in st.session_state:
                    st.session_state["task_completion_time"] = 0

                switch_page("consentToParticipate")
st.set_page_config(layout="wide")
main()
