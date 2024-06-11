import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
from datetime import datetime


def inital_questions_update_finance(selected_companies, familiarity_dict, sec_10_documents, knowledgecheck_finance):
    file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
    df = pd.read_csv(file_path)
    row = 0
    if not selected_companies:
        df.loc[row, 'CompaniesKnowledege'] = str(selected_companies)
    df.loc[row, 'financial_literacy'] = familiarity_dict
    df.loc[row, 'sec_10_documents'] = sec_10_documents
    df.loc[row, "KnowledgeCheckFinance"] = knowledgecheck_finance

    df.to_csv(file_path, index=False)


def financial_knowledge_questions():
    st.subheader("Financial Knowledge Assessment")

    # Question 1
    companies_options = ["Amazon", "Microsoft", "Nvidia", "Intel", "Apple", "I do not know any of these companies"]
    st.subheader("Do you know the following companies and vaguely what they do? If yes, select them")
    selected_companies = st.multiselect("Select companies:", companies_options)
    st.divider()
    # Question 2
    st.subheader("I understand key financial terms and can accurately interpret financial reports and data.")
    financial_literacy = st.radio(
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
        key="financial_literacy_slider",
        index=None,
        horizontal=True
    )
    st.divider()
    # Question 3
    st.subheader("Have you previously worked with or read quarterly financial reports?")
    sec_10_documents = st.radio("", ["Yes", "No"], index=None, horizontal=True)
    st.divider()
    return selected_companies, financial_literacy, sec_10_documents






try:
    st.progress(15, f"Study Progress: 15% Complete")
    st.title('Pre-Study Questionaire: Financial Knowledge')
    selected_companies, financial_literacy, sec_10_documents = financial_knowledge_questions()
    st.markdown("##")
    # The question

    st.subheader("""You are reviewing a company's quarterly reports and come across the section on 'Management's Discussion and Analysis of Financial Condition and Results of Operations' (MD&A)?
    """)
    # Radio button for user to select an answer
    knowledgecheck_finance = st.radio("Which of the following best describes the purpose of the MD&A section?", [
        "A. To provide an analysis of the company's financial performance from the perspective of management, including trends, risks, and future plans.",
        "B. To list all of the company's financial transactions in detail over the fiscal year.",
        "C. To provide the company's audited financial statements, including the balance sheet, income statement, and cash flow statement.",
        "D. I do not know and can not answer this question."
    ], index=None)

    general_questions_completed = False

    st.write('Thank you for providing the information. You may proceed with the experiment now.')
    if st.button('Next'):
        likert_mapping = {'1. Strongly Disagree': 1,
                          '2. Disagree': 2,
                          '3. Somewhat Disagree': 3,
                          '4. Neither Disagree nor Agree': 4,
                          '5. Somewhat Agree': 5,
                          '6. Agree': 6,
                          '7. Strongly Agree': 7}
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: Selected companies {selected_companies}")
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: Answer to Knowledge Check SEC-10 {knowledgecheck_finance}")
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: financial_literacy {likert_mapping[financial_literacy]}")
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: sec_10_documents {sec_10_documents}")
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.now()}: Experiment started {datetime.now()}")


        sec_mapping = {"Yes": 1, "No": 0}
        if financial_literacy is None or sec_10_documents is None or knowledgecheck_finance is None or not selected_companies:
            st.error("You need to answer the questions!")

        if financial_literacy is not None and sec_10_documents is not None and knowledgecheck_finance is not None and bool(selected_companies):
            inital_questions_update_finance(selected_companies, likert_mapping[financial_literacy], sec_mapping[sec_10_documents], knowledgecheck_finance)
            switch_page("introductionToStudy")
except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")


