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

    def final_evaluation_per_user(EaseOfReading, FinalTrust, WillingnessToUse,
                                  CognitiveLoad, Usefulness1, Usefulness2, EaseOfUse1, EaseOfUse2, BI1, BI2):
        likert_mapping = {'1. Strongly Disagree': 1,
                          '2. Disagree': 2,
                          '3. Somewhat Disagree': 3,
                          '4. Neither Disagree nor Agree': 4,
                          '5. Somewhat Agree': 5,
                          '6. Agree': 6,
                          '7. Strongly Agree': 7}

        file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
        df = pd.read_csv(file_path)
        row = 0
        df.loc[row, 'EaseOfReading'] = likert_mapping[EaseOfReading]
        df.loc[row, 'FinalTrust'] = likert_mapping[FinalTrust]
        df.loc[row, 'WillingnessToUse'] = likert_mapping[WillingnessToUse]
        df.loc[row, 'CognitiveLoad'] = likert_mapping[CognitiveLoad]
        df.loc[row, 'Usefulness1'] = likert_mapping[Usefulness1]
        df.loc[row, 'Usefulness2'] = likert_mapping[Usefulness2]
        df.loc[row, 'EaseOfUse1'] = likert_mapping[EaseOfUse1]
        df.loc[row, 'EaseOfUse2'] = likert_mapping[EaseOfUse2]
        df.loc[row, 'BI1'] = likert_mapping[BI1]
        df.loc[row, 'BI2'] = likert_mapping[BI2]
        df.to_csv(file_path, index=False)


    def willingness_to_use_model():
        st.title('Willingness to use')
        st.subheader('I would use this RAG model for future tasks similar to the one tested.')
        willingness = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.markdown("##")
        return willingness


    def skepticism_towards_ai_content():
        st.title('Skepticism towards AI')
        st.subheader( 'I am skeptical about the reliability of content generated by AI like RAG.')
        skepticism = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="skepticism_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.markdown("##")
        return skepticism

    def cognitive_load():
        st.title('Cognitive Load')
        st.subheader('Using the RAG system was mentally demanding.')
        cognitive_load = st.select_slider(
             'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="cognitive_load_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.markdown("##")
        return cognitive_load


    def perceived_usefulness():
        st.title('Perceived Usefulness of the RAG System')
        st.subheader('Using the RAG system helped me accomplish tasks more quickly.')
        usefulness1 = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="pu_1_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.subheader("The RAG system made it easier to perform tasks that are similar to the ones tested.")
        usefulness2 = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="pu_2_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.markdown("##")
        return usefulness1, usefulness2


    def perceived_ease_of_use():
        st.title('Perceived Ease-of-Use of the RAG System')
        st.subheader("I found the RAG system easy to use.")
        ease_of_use1 = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="poe_1_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.subheader("Interacting with the RAG system was clear and understandable.")
        ease_of_use2 = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="poe_2_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.markdown("##")
        return ease_of_use1, ease_of_use2

    def ease_of_reading():
        st.title('Ease of reading')
        st.subheader('The text generated by the RAG system was easy to read and understand.')
        reading_ease = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="ease_of_reading_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )
        st.markdown("##")
        return reading_ease

    def user_feedback():
        st.title('User Feedback on RAG Service')

        st.subheader("The information from the PDFs was helpful for correctly answering the questions.")
        helpfulness = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="helpfulness_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )

        st.subheader('I trust the generated answers due to the provided sources.')
        trust = st.select_slider(
            'Select an option between 1. Strongly Disagree and 7. Strongly Agree',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            key="trust_slider",
            value='4. Neither Disagree nor Agree'  # Default selection
        )

        st.markdown("##")
        return helpfulness, trust


    st.progress(95, f"Study Progress: 95% Complete")
    st.title("Final Evaluation and Feedback")
    st.subheader('Please answer the following questions to provide feedback on your experience. After completing, press the "Finish the study" button to save your results at the end of the page.')

    FinalTrust = skepticism_towards_ai_content()
    WillingnessToUse = willingness_to_use_model()
    CognitiveLoad = cognitive_load()
    Usefulness1, Usefulness2 = perceived_usefulness()
    EaseOfUse1, EaseOfUse2 = perceived_ease_of_use()
    EaseOfReading = ease_of_reading()
    if streamlit.session_state.sampled_study_type == "NoSources":
        BI1 = 0
        BI2 = 0
    BI1, BI2 = user_feedback()()

    if st.button("Finish the study"):
        #age, gender, education, proficiency,
        logger.info(f"EaseofReading: {EaseOfReading}")
        logger.info(f"FinalTrust: {FinalTrust}")
        logger.info(f"WillingnessToUse: {WillingnessToUse}")
        logger.info(f"CognitiveLoad: {CognitiveLoad}")
        logger.info(f"Usefulness1: {Usefulness1}")
        logger.info(f"Usefulness2: {Usefulness2}")
        logger.info(f"EaseOfUse1: {EaseOfUse1}")
        logger.info(f"EaseOfUse2: {EaseOfUse2}")
        logger.info(f"BI1: {BI1}")
        logger.info(f"BI2: {BI2}")

        final_evaluation_per_user(EaseOfReading, FinalTrust, WillingnessToUse, CognitiveLoad, Usefulness1, Usefulness2,
                                  EaseOfUse1, EaseOfUse2, BI1, BI2)

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
        file_path = f'./data/raw_answers/UserStudy/UserStudy_{st.session_state.sessionID}.csv'
        object_key = f'UserStudy_{st.session_state.sessionID}.csv'
        s3.upload_file(file_path, bucket_name, object_key)

        file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
        object_key = f'GeneralQuestions{st.session_state.sessionID}.csv'
        s3.upload_file(file_path, bucket_name, object_key)

        file_path = f"./data/raw_answers/Logs/logs_{st.session_state.sessionID}.log"
        object_key = f'logs_{st.session_state.sessionID}.log'
        s3.upload_file(file_path, bucket_name, object_key)
        logger.info("Study finished")
        switch_page("thankyou")

except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")
