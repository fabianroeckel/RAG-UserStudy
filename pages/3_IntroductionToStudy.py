import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from loguru import logger
from datetime import datetime

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
try:
    st.progress(20, f"Study Progress: 15% Complete")
    st.header("Understanding Your Task in This Study")
    st.markdown("----")

    ## Step 1
    col_text, col_image = st.columns([3, 7])
    with col_image:
        st.image("media/Explanations/slides/Folie1.jpeg")

    with col_text:
        st.subheader("Step 1: Introduction to RAG System")
        st.write("Welcome to the study! You'll be using a Retrieval Augmented Generation (RAG) system designed specifically for financial tasks. A screenshot of your workspace is on the left side of the interface, where you'll interact with the system.")

    ## Step 2
    col_text, col_image = st.columns([3, 7])
    with col_image:
        st.image("media/Explanations/slides/Folie2.jpeg")

    with col_text:
        st.subheader("Step 2: Identifying the Task")
        st.write("You can identify your task highlighted in orange within the RAG system. This task is presented both as a title at the top of the interface and on the right side, where you'll input your answer.")

    ## Step 3
    col_text, col_image = st.columns([3, 7])
    with col_image:
        st.image("media/Explanations/slides/Folie3.jpeg")

    with col_text:
        st.subheader("Step 3: Understanding Financial Terms")
        st.write("If you encounter any unfamiliar financial terms during the task, additional information is available within the RAG system. Simply look for the box below the title highlighted in orange, and further explanations will be provided to assist you.")

    ## Step 4
    col_text, col_image = st.columns([3, 7])
    with col_image:
        st.image("media/Explanations/slides/Folie4.jpeg")

    with col_text:
        st.subheader("Step 4: Accessing Information")
        st.write("All necessary information related to the financial task is displayed on the left side within the RAG system. If you require additional context or wish to verify the information, you can access the sources provided.")

    ## Step 5
    col_text, col_image = st.columns([3, 7])
    with col_image:
        st.image("media/Explanations/slides/Folie5.jpeg")

    with col_text:
        st.subheader("Step 5: Verifying Accuracy")
        st.write("You may have the option to check the PDFs file with the related information. To ensure the accuracy of the information provided by the RAG system, you can navigate through the attached PDF(s). Relevant sections within the PDF(s) are highlighted in yellow, making it easier for you to verify the correctness of the responses.")

    ## Step 6
    col_text, col_image = st.columns([3, 7])
    with col_image:
        st.image("media/Explanations/slides/Folie6.jpeg")

    with col_text:
        st.subheader("Step 6: Responding and Feedback")
        st.write("After reviewing the information and verifying its accuracy, proceed to answer the questions related to the financial task. You'll find these questions on the right side within the RAG system interface. Feel free to indicate your confidence level in the responses or report any errors you may have identified.")

    if st.button('I Understand! Let\'s Start the Experiment'):
        st.session_state.progress = 20
        if "timestamp" not in st.session_state:
            st.session_state["timestamp"] = datetime.now()
        logger.info(f"Introduction to study completed and User study starts")
        switch_page("Userstudy")
except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")