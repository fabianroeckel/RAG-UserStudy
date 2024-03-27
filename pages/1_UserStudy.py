# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st
import random
from streamlit_float import *
import textwrap
from utils import *
from streamlit_pdf_viewer import pdf_viewer
from streamlit_modal import Modal
import PyPDF2

page_number = st.session_state.question_number
def chat_content(role, content):
    st.session_state['messages'].append({"role": role, "content": content})

def display_chat_content():
    st.session_state.messages.append({"role": "user", "content": getQuestion(st.session_state.sessionID, page_number)})
    st.session_state.messages.append({"role": "assistant", "content": getResponse(st.session_state.sessionID, page_number)})
    print(page_number)
##LAYOUT
with st.sidebar:
    st.text("Progress")

    st.progress(random.randint(1,100))


with st.container():
    st.write(st.session_state.sessionID)
    st.title("Your Finance-Co Pilot powered by ChatGPT4")
    modal = Modal(
        "Source Name",
        key="demo-modal",

        # Optional
        padding=20,  # default value
        max_width=700  # default value
    )

    if modal.is_open():
        with modal.container():
            file_path = "data/v1/docs/2023 Q3 NVDA.pdf"
            file = open(file_path, 'rb')
            pdfReader = PyPDF2.PdfReader(file)
            totalPages = len(pdfReader.pages)
            pdf_viewer(file_path,pages_to_render=list(range(totalPages)))

    with st.expander("Task Introduction and General Instructions"):
        st.text(textwrap.fill("general instructions and scenario here - Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.", width=300))
        st.checkbox("I have read the general instructions")
        st.radio("ATTENTION QUESTION", ("Yes", "No"))
    col_a, col_b, col_c = st.columns([3,3,3])

    with st.expander("Data Preview"):
        with col_a:
            st.write(pd.read_csv('./data/RAG_Dataset.csv'))
        with col_b:
            st.write(pd.read_csv(f'./data/raw_answers/UserStudy/UserStudy_{st.session_state.sessionID}.csv'))
        with col_c:
            st.write(pd.read_csv(f'./data/raw_answers/UserGeneral/GeneralQuestions{st.session_state.sessionID}.csv'))

    question = getQuestion(st.session_state.sessionID, page_number)
    st.header(question)
    st.text("You can use the chat interface to interact with your financial Co-Pilot to answer this task.")

    st.markdown("---")

col_chat, col_questionaire = st.columns([6,4])

with col_chat:
    with st.container(height=600, border=True):
        if "messages" not in st.session_state:
            st.session_state.messages = []
            display_chat_content()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        source1, source2, source3, source4, spacer = st.columns([2,2,2,2,2])
        with source1:
            open_modal = st.button("Source1")
            if open_modal:
                modal.open()
        with source2:
            open_modal = st.button("Source2")
            if open_modal:
                modal.open()
        with source3:
            open_modal = st.button("Source3")
            if open_modal:
                modal.open()

    with st.container():
        if prompt := st.chat_input("How can i help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # with st.chat_message("user"):
            #    st.markdown(prompt)

            # with st.chat_message("assistant"):
            #   message_placeholder = st.empty()
            full_response = "Based on the information provided, please use your best judgment to address the task at hand."
            #    message_placeholder.markdown(full_response + "")
            st.session_state.messages.append({"role": "assistant", "content": full_response})


with col_questionaire:
    with st.form("user form"):

        st.title('Questionnaire')
        trust = st.select_slider('To what extent do you trust the accuracy of the response?',
                                         options=['Not at all', 'Slightly', 'Moderately', 'Very much', 'Completely'])
        decision = st.radio("Which company had the best quarter?", ('Nvidia', 'Apple', 'Intel', 'Amazon'))

        if st.form_submit_button():
            update_questionaire(trust, decision, st.session_state.sessionID, page_number)