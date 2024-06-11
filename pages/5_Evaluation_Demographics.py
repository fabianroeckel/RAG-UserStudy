import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
import boto3
from datetime import datetime





try:
    def final_evaluation_per_user_demographics(age,prolificID, gender, education, proficiency):
        file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
        df = pd.read_csv(file_path)
        row = 0

        #ProlificID required for payment
        df.loc[row, 'prolificID'] = prolificID

        df.loc[row, 'Age'] = age
        # GENDER
        gender_mapping = {'Male': 0, 'Female': 1, 'Other': 2}
        df.loc[row, 'Gender'] = gender_mapping[gender]

        # EDUCATION
        education_mapping = {'High School': 0, "Bachelor's Degree": 1, "Masters's Degree": 2, "PhD": 3, "Other": 4}
        df.loc[row, 'Education'] = education_mapping[education]

        # LANGUAGE
        language_mapping = {'BasicUser(A1-A2)': 0, 'IndependentUser(B1-B2)': 1, 'ProficientUser(C1-C2)': 2,
                            'Native Speaker': 3}
        df.loc[row, "LanguageLevel"] = language_mapping[proficiency]
        df.to_csv(file_path, index=False)



    def language_level():
        st.title('Language Level')
        proficiency = st.selectbox('How would you rate your proficiency with the English language of the system?',
                                   ['BasicUser(A1-A2)', 'IndependentUser(B1-B2)', 'ProficientUser(C1-C2)',
                                    'Native Speaker'], index=None)

        return proficiency

    def prolific_id():
        prolific_id = st.text_input(label="What is your ProlificID?")
        return prolific_id

    def demographic_questions():
        st.title('Demographic Information')
        age = st.number_input('What is your age?', min_value=18, max_value=120, value=None)
        gender = st.selectbox('What is your gender?', ['Male', 'Female', 'Other'], index=None)
        education = st.selectbox('What is your level of education?',
                                 ['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Other'], index=None)

        return age, gender, education

    st.progress(90, f"Study Progress: 90% Complete")
    st.title("Final Evaluation and Feedback")
    st.subheader('Please answer the following questions to provide feedback on your experience.')

    age, gender, education = demographic_questions()
    prolific_id = prolific_id()
    st.markdown("##")
    proficiency = language_level()

    if st.button("Next set of questions"):
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime.now()}: The prolificID of the user is: {prolific_id}")

        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: The age of the user is: {age}")

        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: The gender of the user is: {gender}")

        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: The education level is {education}")

        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: The language profiency is {proficiency}")

        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: All tasks completed")

        #age, gender, education, proficiency,
        if age is None or gender is None or education is None or prolific_id is None or proficiency is None:
            st.error("You need to answer the questions!")
        else:
            final_evaluation_per_user_demographics(age, prolific_id, gender, education,proficiency)
            switch_page("Evaluation_TAMandMore")

except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("Evaluation_TAMandMore")
