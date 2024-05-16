import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx
from datetime import datetime


def inital_questions_update(rag_experience, system_usage_frequency,
                            skepticism, selected_companies, familiarity_dict, sec_10_documents):
    print()
    file_path = f"./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv"
    df = pd.read_csv(file_path)
    row = 0
    # AGE
    df.loc[row, 'RAG-PreviousExperience'] = rag_experience
    df.loc[row, 'RAG-Usage'] = system_usage_frequency
    df.loc[row, 'InitialTrust'] = skepticism
    df.loc[row, 'CompaniesKnowledege'] = str(selected_companies)
    df.loc[row, 'financial_literacy'] = familiarity_dict
    df.loc[row, 'sec_10_documents'] = sec_10_documents

    df.to_csv(file_path, index=False)
    print(df)
    print(df.head())


def similar_systems_experience():
    st.title('Experience with RAG Systems')
    with st.expander("What is a RAG-System?", expanded=True):
        col_expl, col_video = st.columns([6, 4])
        with col_expl:
            st.markdown("**RAG**, which stands for **Retrieval-Augmented Generation**, is an AI framework designed to enhance the responses of large language models (LLMs) by incorporating real-time information from external databases or knowledge bases. This approach helps to ground the model's responses in accurate and current information, making them more reliable and contextually relevant. ")
            st.markdown("""
                #### How Does It Work? :
                - **Retrieval**: When you ask a question or make a request, the RAG system first searches through a vast external database to find relevant information. This process is similar to how you might use a search engine to find data on a particular topic. 
                - **Augmentation**: The information retrieved in the first step is then used to 'augment' the knowledge base of the LLM. Essentially, the model integrates this fetched data with its pre-existing knowledge. 
                - **Generation**: With an updated set of information, the LLM then generates a response that not only reflects its built-in knowledge but also includes and references the newly retrieved data.
                """
                )
            st.markdown("Example applications that you can use are [Perplexity.ai](https://www.perplexity.ai/) or [FinTool](https://www.fintool.com/)")

        with col_video:
            st.image("media/rag_gif.gif")

    retrieval_augmentation_generation = st.radio(
        "How does a Retrieval augmented generation system work?",
        options=[
            "a) It searches for relevant information, augments it, and generates a response.",
            "b) It generates a response without retrieving any external data.",
            "c) It integrates retrieved data but does not generate a response.",
            "d) It retrieves information, but does not integrate it with existing knowledge."
        ],
        key="rag_system_question",
        index=0  # Default selection
    )

    rag_experience = st.selectbox('Have you ever used a RAG system before?', ['Yes', 'No'])
    system_usage_frequency = st.selectbox('How often do you use similar applications or systems?',
                                          ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never'])

    rag_experience_mapping = {'No': 0, 'Yes': 1}
    system_usage_mapping = {'Daily': 1, 'Weekly': 2, 'Monthly': 3, 'Rarely': 4, 'Never': 0}

    return rag_experience_mapping[rag_experience], system_usage_mapping[system_usage_frequency]

def perceived_usefulness():
    st.subheader("Using a RAG in my job would enable me to accomplish tasks more quickly.'")
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
        value='Neither agree nor disagree'  # Default selection
    )
    likert_mapping = {'1. Strongly Disagree': 1,
            '2. Disagree' : 2,
            '3. Somewhat Disagree': 3,
            '4. Neither Disagree nor Agree': 4,
            '5. Somewhat Agree': 5,
            '6. Agree': 6,
            '7. Strongly Agree': 7}
    return likert_mapping[usefulness1]


def skepticism_towards_ai_content():
    st.title('Skepticism towards AI')
    st.subheader('I am skeptical about the reliability of content generated by AI like RAG.')
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
    likert_mapping = {'1. Strongly Disagree': 1,
                      '2. Disagree': 2,
                      '3. Somewhat Disagree': 3,
                      '4. Neither Disagree nor Agree': 4,
                      '5. Somewhat Agree': 5,
                      '6. Agree': 6,
                      '7. Strongly Agree': 7}
    st.markdown("##")
    return likert_mapping[skepticism]

def financial_knowledge_questions():
    st.title("Financial Knowledge Assessment")

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
        value='4. Neither Disagree nor Agree'  # Default selection
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
    st.header('Welcome to the Experiment!')
    st.write('Please provide some demographic information before starting the experiment.')

    rag_experience, system_usage_frequency = similar_systems_experience()
    st.markdown("##")
    skepticism = skepticism_towards_ai_content()
    st.markdown("##")
    selected_companies, familiarity_dict, sec_10_documents = financial_knowledge_questions()
    st.markdown("##")
    general_questions_completed = False

    st.write('Thank you for providing the information. You may proceed with the experiment now.')
    if st.button('Start with the Experiment'):
        if "timestamp" not in st.session_state:
            st.session_state["timestamp"] = datetime.now()

        inital_questions_update(rag_experience, system_usage_frequency, skepticism,
                                selected_companies, familiarity_dict, sec_10_documents)
        switch_page("introductionToStudy")
except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")


