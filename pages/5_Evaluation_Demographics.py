import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
import boto3
from loguru import logger





try:
    logname = f"data/raw_answers/Logs/logs_{st.session_state['sessionID']}.log"
    logger.add(logname)

    def final_evaluation_per_user_demographics(age, gender, education, proficiency):
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
                                    'Native Speaker'])

        return proficiency


    def demographic_questions():
        st.title('Demographic Information')
        age = st.number_input('What is your age?', min_value=18, max_value=120)
        gender = st.selectbox('What is your gender?', ['Male', 'Female', 'Other'])
        education = st.selectbox('What is your level of education?',
                                 ['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Other'])

        return age, gender, education
    logger.info("Alle Tasks completed")

    st.progress(90, f"Study Progress: 90% Complete")
    st.title("Final Evaluation and Feedback")
    st.subheader('Please answer the following questions to provide feedback on your experience. After completing, press the "Finish the study" button to save your results at the end of the page.')

    age, gender, education = demographic_questions()
    st.markdown("##")
    proficiency = language_level()

    if st.button("Next set of questions"):
        #age, gender, education, proficiency,
        final_evaluation_per_user_demographics(age, gender, education,proficiency)
        logger.info(f"The age of the user is: {age}")
        logger.info(f"The gender of the user is: {gender}")
        logger.info(f"The education level is {education}")
        logger.info(f"The language profiency is {proficiency}")
        switch_page("Evaluation_TAMandMore")

except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("Evaluation_TAMandMore")
