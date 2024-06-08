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
        willingness = st.radio(
            '',
            options=[
                '1. Strongly Disagree',
                '2. Disagree',
                '3. Somewhat Disagree',
                '4. Neither Disagree nor Agree',
                '5. Somewhat Agree',
                '6. Agree',
                '7. Strongly Agree'
            ],
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown("##")
        st.divider()
        return willingness


    def skepticism_towards_ai_content():
        st.subheader('I have doubts about the ability of AI to generate fully reliable and accurate content.')
        skepticism = st.radio(
            '',
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
            index=None,
            horizontal=True
            # Default selection
        )
        st.markdown('##')
        st.divider()
        return skepticism


    def cognitive_load():
        st.title('Cognitive Load')
        st.subheader('Using the RAG system was mentally demanding.')
        cognitive_load = st.radio(
             '',
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
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown("##")
        st.divider()
        return cognitive_load


    def perceived_usefulness():
        st.title('Perceived Usefulness of the RAG System')
        st.subheader('Using the RAG system helped me accomplish tasks more quickly.')
        usefulness1 = st.radio(
            '',
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
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown('####')
        st.subheader("Using the RAG system made it easier to perform the tasks.")
        usefulness2 = st.radio(
            '',
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
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown("##")
        st.divider()
        return usefulness1, usefulness2


    def perceived_ease_of_use():
        st.title('Perceived Ease-of-Use of the RAG System')
        st.subheader("I found the RAG system easy to use.")
        ease_of_use1 = st.radio(
            '',
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
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown('####')
        st.subheader("Interacting with the RAG system was clear and understandable.")
        ease_of_use2 = st.radio(
            '',
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
            index=None,
            horizontal=True # Default selection
        )
        st.markdown("##")
        st.divider()
        return ease_of_use1, ease_of_use2

    def ease_of_reading():
        st.title('Ease of reading')
        st.subheader('The text generated by the RAG system was easy to read and understand.')
        reading_ease = st.radio(
            '',
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
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown("##")
        st.divider()
        return reading_ease


    def pre_study_feedback():
        st.subheader("Your Feedback for our Study")
        st.write("If you have any concerns or improvement suggestions about the study design please enter them here:")
        improvement_ideas = st.text_input()

        st.write("What is your opinion on the length of the questionnaire?")
        questionnaire_length = st.selectbox(options=("About right", "Too long", "Too short"))

        st.write("What is your opinion on the clarity of the questions?")
        questionnaire_clarity = st.selectbox(options=("Poor", "Satisfactory", "Good", "Very Good", "Excellent"))

        st.write("What is your opinion on the structure and format of the questionnaire?")
        questionnaire_structure = st.selectbox(options=("Poor", "Satisfactory", "Good", "Very Good", "Excellent"))

        fileNameGeneralQuestions = f"./data/raw_answers/PreStudy/PreStudy{st.session_state.sessionID}.csv"
        with open(fileNameGeneralQuestions, mode='w', newline='') as file:
            writer = csv.writer(file)
            ##add header
            writer.writerow(
                ['userID', "improvement_ideas", 'questionnaire_length', 'questionnaire_clarity', 'questionnaire_structure'])
            writer.writerow([st.session_state.sessionID, improvement_ideas, questionnaire_length, questionnaire_clarity, questionnaire_structure])


    def user_feedback():
        st.title('User Feedback on RAG Service')

        st.subheader("The information from the PDFs was helpful for correctly answering the questions.")
        helpfulness = st.radio(
            '',
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
            index=None,
            horizontal=True  # Default selection
        )
        st.markdown('####')
        st.subheader('I trust the generated answers due to the provided sources.')
        trust = st.radio(
            '',
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
            index=None,
            horizontal=True  # Default selection
        )

        st.markdown("##")
        st.divider()
        return helpfulness, trust


    st.progress(95, f"Study Progress: 95% Complete")
    st.title("Final Evaluation and Feedback")
    st.subheader('Please answer the following questions to provide feedback on your experience. After completing, press the "Finish the study" button to save your results at the end of the page.')
    st.divider()
    st.markdown('####')
    FinalTrust = skepticism_towards_ai_content()
    WillingnessToUse = willingness_to_use_model()
    CognitiveLoad = cognitive_load()
    Usefulness1, Usefulness2 = perceived_usefulness()
    EaseOfUse1, EaseOfUse2 = perceived_ease_of_use()
    EaseOfReading = ease_of_reading()
    if streamlit.session_state.sampled_study_type == "NoSources":
        BI1 = 0
        BI2 = 0
    BI1, BI2 = user_feedback()

    if st.button("Next"):
        if EaseOfReading is None or FinalTrust is None or WillingnessToUse is None or CognitiveLoad is None or Usefulness1 is None or Usefulness2 is None or EaseOfUse1 is None or EaseOfUse2 is None or BI1 is None or BI2 is None:
            st.error("You need to answer the questions!")


        else:
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
            file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
            object_key = f'GeneralQuestions{st.session_state.sessionID}.csv'
            s3.upload_file(file_path, bucket_name, object_key)

            file_path = f"./data/raw_answers/Logs/logs_{st.session_state.sessionID}.log"
            object_key = f'logs_{st.session_state.sessionID}.log'
            s3.upload_file(file_path, bucket_name, object_key)
            logger.info("Study finished")
            switch_page("PreStudyFeedback")

except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")
