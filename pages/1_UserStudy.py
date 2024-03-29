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

def display_chat_content():
    st.session_state.messages = []
    st.session_state.messages.append({"role": "user", "content": getQuestionAndResponse(st.session_state.sessionID)[0]})
    st.session_state.messages.append({"role": "assistant", "content": getQuestionAndResponse(st.session_state.sessionID)[1]})
    print("Start display content")

##LAYOUT
with st.sidebar:
    st.text("Progress")

    st.progress(random.randint(1,100))

    st.write(pd.read_csv(f'./data/raw_answers/UserStudy/UserStudy_{st.session_state.sessionID}.csv'))

    st.write("Correct Responses")
    st.write(pd.read_csv("data/RAG_Dataset-Correct_Responses.csv"))

    st.write("Evident Baseless Information")
    st.write(pd.read_csv("data/RAG_Dataset-Evident_Baseless_Information.csv"))

    st.write("Evident Conflict")
    st.write(pd.read_csv("data/RAG_Dataset-Evident_Conflict.csv"))


with st.container():
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


    question = getQuestionAndResponse(st.session_state.sessionID)[0]
    st.header(question)
    st.text("You can use the chat interface to interact with your financial Co-Pilot to answer this task.")

    st.markdown("---")

col_chat, col_questionaire = st.columns([6,4])

with col_chat:
    with st.container(height=600, border=True):

        display_chat_content()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])




        if st.session_state.sampled_study_type == "SingleSource":
            open_modal = st.button("Source1")
            if open_modal:
                modal.open()

        if st.session_state.sampled_study_type == "MultiSource":
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
            update_questionaire(trust, decision)