import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
from datetime import datetime
from loguru import logger


def inital_questions_update_finance(selected_companies, familiarity_dict, sec_10_documents):
    file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
    df = pd.read_csv(file_path)
    row = 0
    if not selected_companies:
        df.loc[row, 'CompaniesKnowledege'] = str(selected_companies)
    df.loc[row, 'financial_literacy'] = familiarity_dict
    df.loc[row, 'sec_10_documents'] = sec_10_documents

    df.to_csv(file_path, index=False)


def financial_knowledge_questions():
    st.subheader("Financial Knowledge Assessment")

    # Question 1
    companies_options = ["Amazon", "Microsoft", "Nvidia", "Intel", "Apple"]
    st.subheader("Do you know the following companies and vaguely what they do? If yes, select them" )
    selected_companies = st.multiselect("Select companies:", companies_options)
    # Question 2
    st.subheader("I understand key financial terms and can accurately interpret financial reports and data.")
    financial_literacy = st.select_slider(
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
        key="financial_literacy_slider",
        value='4. Neither Disagree nor Agree'
    )
    likert_mapping = {'1. Strongly Disagree': 1,
                      '2. Disagree': 2,
                      '3. Somewhat Disagree': 3,
                      '4. Neither Disagree nor Agree': 4,
                      '5. Somewhat Agree': 5,
                      '6. Agree': 6,
                      '7. Strongly Agree': 7}


    # Question 3
    st.subheader("Have you previously worked with or read SEC-10 documents?")
    sec_10_documents = st.radio("Select one:", ["Yes", "No"])

    sec_mapping = {"Yes":1, "No":0}

    return selected_companies, likert_mapping[financial_literacy], sec_mapping[sec_10_documents]






try:
    logname = f"data/raw_answers/Logs/logs_{st.session_state['sessionID']}.log"
    logger.add(logname)
    st.progress(15, f"Study Progress: 15% Complete")
    st.title('Pre-Study Questionaire: Financial Knowledge')
    selected_companies, familiarity_dict, sec_10_documents = financial_knowledge_questions()
    st.markdown("##")
    # The question

    st.subheader("""You are reviewing a company's SEC 10-K filing and come across the section on 'Management's Discussion and Analysis of Financial Condition and Results of Operations' (MD&A). 
    Which of the following best describes the purpose of the MD&A section?
    """)

    # Radio button for user to select an answer
    answer = st.radio("Select the correct option", [
        "A. To provide an analysis of the company's financial performance from the perspective of management, including trends, risks, and future plans.",
        "B. To list all of the company's financial transactions in detail over the fiscal year.",
        "C. To provide the company's audited financial statements, including the balance sheet, income statement, and cash flow statement.",
        "D. I do not know and can not answer this question."
    ])
    logger.info(f"Answer to Knowledge Check SEC-10 {answer}")
    general_questions_completed = False

    st.write('Thank you for providing the information. You may proceed with the experiment now.')
    if st.button('Start with the Experiment'):
        logger.info(f"Experiment started {datetime.now()}")
        inital_questions_update_finance(selected_companies, familiarity_dict, sec_10_documents)
        logger.info(f"Initial questions selected companies {selected_companies}")
        logger.info(f"Initial questions financial_literacy {familiarity_dict}")
        logger.info(f"Initial questions sec_10_documents {sec_10_documents}")
        switch_page("introductionToStudy")
except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")


