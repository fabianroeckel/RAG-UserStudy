import streamlit
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
import boto3
from loguru import logger
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive





try:
    logname = f"data/raw_answers/Logs/logs_{st.session_state['sessionID']}.log"
    logger.add(logname)

    def pre_study_feedback():
        st.subheader("Your Feedback for our Study")
        improvement_ideas = st.text_input(label="If you have any concerns or improvement suggestions about the study design please enter them here:")

        questionnaire_length = st.selectbox(label="What is your opinion on the length of the questionnaire?", options=("About right", "Too long", "Too short"))

        questionnaire_clarity = st.selectbox("What is your opinion on the clarity of the questions?", options=("Poor", "Satisfactory", "Good", "Very Good", "Excellent"))

        questionnaire_structure = st.selectbox(label="What is your opinion on the structure and format of the questionnaire?", options=("Poor", "Satisfactory", "Good", "Very Good", "Excellent"))

        return improvement_ideas, questionnaire_length, questionnaire_clarity, questionnaire_structure

    def store_inputs(improvement_ideas, questionnaire_length, questionnaire_clarity, questionnaire_structure):
        fileNameGeneralQuestions = f"./data/raw_answers/PreStudy/PreStudy{st.session_state.sessionID}.csv"
        with open(fileNameGeneralQuestions, mode='w', newline='') as file:
            writer = csv.writer(file)
            ##add header
            writer.writerow(
                ['userID', "improvement_ideas", 'questionnaire_length', 'questionnaire_clarity', 'questionnaire_structure'])
            writer.writerow([st.session_state.sessionID, improvement_ideas, questionnaire_length, questionnaire_clarity, questionnaire_structure])



    st.progress(99, f"Study Progress: 95% Complete")
    st.title("Final Evaluation and Feedback")
    st.subheader('Please answer the following questions to provide feedback on your experience. After completing, press the "Finish the study" button to save your results at the end of the page.')

    improvement_ideas, questionnaire_length, questionnaire_clarity, questionnaire_structure = pre_study_feedback()
    store_inputs(improvement_ideas, questionnaire_length, questionnaire_clarity, questionnaire_structure)



    if st.button("Finish the study"):
        # Check if Streamlit secrets are available
        if "AWS_ACCESS_KEY_ID" in st.secrets and "AWS_SECRET_ACCESS_KEY" in st.secrets:
            aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
        else:
            # If Streamlit secrets are not available, manually load environment variables from .env file
            with open('.env') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    os.environ[key] = value

            # Retrieve AWS credentials from environment variables
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        # Initialize an S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Upload a CSV file
        bucket_name = 'rag-studyresults'
        file_path = f"./data/raw_answers/PreStudy/PreStudy{st.session_state.sessionID}.csv"
        object_key = f'PreStudy{st.session_state.sessionID}.csv'
        s3.upload_file(file_path, bucket_name, object_key)
        switch_page("thankyou")

except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")
