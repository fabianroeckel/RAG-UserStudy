import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages, Page
from loguru import logger


def main():
    st.progress(0, text=f"Study Progress: 0% Complete")
    hide_pages("streamlit_app.py")
    hide_pages("pages/0_ConsentToParticipate.py")
    hide_pages("pages/1_InitialQuestions.py")
    hide_pages("pages/3_IntroductionToStudy.py")
    hide_pages("pages/4_UserStudy.py")
    hide_pages("pages/6_Evaluation_TAMandMore.py")
    hide_pages("pages/7_ThankYou.py")
    st.title('Welcome to our study and thank you for taking part!')
    st.markdown("""
    ###### Conducted by KSRI – Karlsruhe Digital Service Research & Innovation Hub in cooperation with the University of Bayreuth
    In this study you will be provided with 8 Q&A tasks that are answered by a Generative Artificial Intelligence (GenAI) system, that can either be correct or incorrect. You will be asked to answer each question, with the help of an GenAI and mark incorrect answers by the GenAI.
    The findings will help to inform our understanding of how people behave and make decisions when collaborating with GenAI. With your participation in the study, you make a meaningful contribution to an important research project. Be assured - your time is well invested!

    Keep in mind your payment will partly depend on your performance on these tasks. **For each correct answer you will get 10 pennies**.
    In the following, we will first give you an introduction into the used GenAI and the content of the documents (financial reports), and ask some questions before and after the experiment.

    **Instructions:**
    - Please provide accurate responses to the questions presented in each section.
    - Take your time to understand each question before responding.
    - Your responses will remain confidential and will only be used for research purposes.
    - The payment is only possible when you complete the study. If you decide to stop/cancel your voluntary participation by closing the browser window, we will have to exclude you from all payments.
    -  The study and your responses are anonymous.
    - There are some attention checks throughout the study. Failure to pass the attention checks will lead to eliminating your questionnaire from the study and, therefore, no payment.
    - We reserve the right to also exclude questionnaires with random or otherwise non-serious responses.
    - You can only take the survey once.
    - Please use a desktop or laptop to respond to this survey to ensure optimal visual functionality.
    - Please do not use your browser's back or refresh button while filling out the survey.
    - If you have any questions about the survey, please email us at following email address: study-feedback@ksri.kit.edu

    **Estimated Time:**
    The experiment is expected to take approximately 20-30 minutes to complete.

    Thank you for your participation! Let's get started and contribute to advancements in HCI research.

    ---
    """)

    attention_check1 = st.checkbox("I hereby confirm that I am using a Laptop or Desktop to complete the study.")
    attention_check2 = st.checkbox(
        "I hereby confirm that I have read and understood the information above and that I voluntarily consent to participate in this study.")
    attention_check3 = st.checkbox("I hereby confirm that I will not use any other resources for this study.")

    input_field = st.text_input(
        "This is an attention check. Please type in your answer in lower case letters. What color is grass?")
    logger.info(f"Attention check: {input_field}")

    if st.button('Start Experiment'):
        if not attention_check1 and not attention_check2 and not attention_check3:
            st.error(
                "Make sure to read all the necessary information and agree with the statements above by ticking the box.")
        if attention_check1 and attention_check2 and attention_check3:
            if 'sessionID' not in st.session_state:
                sessionID = getSessionID()
                st.session_state['sessionID'] = sessionID
                logname = f"data/raw_answers/Logs/logs_{st.session_state['sessionID']}.log"
                logger.add(logname)
                logger.info(f"New userID created {sessionID}")

            if 'question_number' not in st.session_state:
                st.session_state["question_number"] = 0

            sampled_study_type = "NoSources"
            st.session_state["sampled_study_type"] = sampled_study_type
            logger.info(f"Assigned studytype {sampled_study_type}")
            generateNewCSFFiles(st.session_state['sessionID'], sampled_study_type)

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