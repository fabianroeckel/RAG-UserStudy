import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from utils import *

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
try:
    st.progress(20, f"Study Progress: 20% Complete")
    st.header("Understanding Your Task in This Study")
    st.markdown("----")

    ## Step 1
    col_text, col_image = st.columns([3, 7])
    with col_image:
        if st.session_state["sampled_study_type"] == "MultiSource":
            st.image("media/Explanations/Explanations/MultiSource/Folie1.jpeg")
        if st.session_state["sampled_study_type"] == "NoSources":
            st.image("media/Explanations/Explanations/NoSource/Folie7.jpeg")
        if st.session_state["sampled_study_type"] == "SingleSource":
            st.image("media/Explanations/Explanations/SingleSource/Folie13.jpeg")


    with col_text:
        st.subheader("Step 1: Introduction to our RAG System")
        st.write("Welcome to the study! You'll be using a Retrieval Augmented Generation (RAG) system designed specifically for financial tasks. To the right is a screenshot of your workspace. It consists of the chat interface and the space for your answers.")

    ## Step 2
    col_text, col_image = st.columns([3, 7])
    with col_image:
        if st.session_state["sampled_study_type"] == "MultiSource":
            st.image("media/Explanations/Explanations/MultiSource/Folie2.jpeg")
        if st.session_state["sampled_study_type"] == "NoSources":
            st.image("media/Explanations/Explanations/NoSource/Folie8.jpeg")
        if st.session_state["sampled_study_type"] == "SingleSource":
            st.image("media/Explanations/Explanations/SingleSource/Folie14.jpeg")

    with col_text:
        st.subheader("Step 2: Identifying the Task")
        st.write("You can see your assignment highlighted in orange on the right. Try to make the correct decision based on the information in the chat interface (left).")

    ## Step 3
    col_text, col_image = st.columns([3, 7])
    with col_image:
        if st.session_state["sampled_study_type"] == "MultiSource":
            st.image("media/Explanations/Explanations/MultiSource/Folie3.jpeg")
        if st.session_state["sampled_study_type"] == "NoSources":
            st.image("media/Explanations/Explanations/NoSource/Folie9.jpeg")
        if st.session_state["sampled_study_type"] == "SingleSource":
            st.image("media/Explanations/Explanations/SingleSource/Folie15.jpeg")

    with col_text:
        st.subheader("Step 3: Understanding Financial Terms")
        st.write("If you encounter any unfamiliar financial terms during the task, additional information is available within the RAG system. Simply look for the box below the title highlighted in orange, and further explanations will be provided to assist you.")

    ## Step 4
    col_text, col_image = st.columns([3, 7])
    with col_image:
        if st.session_state["sampled_study_type"] == "MultiSource":
            st.image("media/Explanations/Explanations/MultiSource/Folie4.jpeg")
        if st.session_state["sampled_study_type"] == "NoSources":
            st.image("media/Explanations/Explanations/NoSource/Folie10.jpeg")
        if st.session_state["sampled_study_type"] == "SingleSource":
            st.image("media/Explanations/Explanations/SingleSource/Folie16.jpeg")

    with col_text:
        st.subheader("Step 4: Accessing Information")
        st.write("All necessary information related to the financial task is displayed within the RAG system. If you need additional context or want to verify the information, you can access the resources provided. You can see the question asked above next to the small red icon. And the answer given by the system next to the orange icon.")

    ## Step 5
    if st.session_state["sampled_study_type"] == "NoSources":
        print("Nosources")
    else:
        col_text, col_image = st.columns([3, 7])
        with col_image:
            if st.session_state["sampled_study_type"] == "MultiSource":
                st.image("media/Explanations/Explanations/MultiSource/Folie5.jpeg")
            if st.session_state["sampled_study_type"] == "NoSources":
                st.image("media/Explanations/Explanations/NoSource/Folie11.jpeg")
            if st.session_state["sampled_study_type"] == "SingleSource":
                st.image("media/Explanations/Explanations/SingleSource/Folie17.jpeg")

        with col_text:
            st.subheader("Step 5: Review Responses")
            st.write("You may or may not have the option to check the PDFs file with the related information. To ensure the accuracy of the information provided by the RAG system, you can navigate through the attached PDF(s). Relevant sections within the PDF(s) are highlighted in yellow, making it easier for you to verify the correctness of the responses.")

    ## Step 6
    col_text, col_image = st.columns([3, 7])
    with col_image:
        if st.session_state["sampled_study_type"] == "MultiSource":
            st.image("media/Explanations/Explanations/MultiSource/Folie6.jpeg")
        if st.session_state["sampled_study_type"] == "NoSources":
            st.image("media/Explanations/Explanations/NoSource/Folie12.jpeg")
        if st.session_state["sampled_study_type"] == "SingleSource":
            st.image("media/Explanations/Explanations/SingleSource/Folie18.jpeg")

    with col_text:
        if st.session_state["sampled_study_type"] == "NoSources":
            number = 5
        else:
            number = 6
        st.subheader(f"Step {number}: Responding and Feedback")
        st.write("After reviewing the information and verifying its accuracy, proceed to answer the questions related to the financial task. You'll find these questions on the right side within the RAG system interface. Feel free to indicate your confidence level in the responses or report any errors you may have identified.")

    st.divider()
    attention_check_answer = st.radio(
        "Which color is used to highlight relevant information in the source documents?",
        ('Blue', 'Yellow', 'Green', 'Red'), horizontal=True, index=None
    )
    attentioncheck1 = st.checkbox("I hereby confirm that I have read the explanations carefully and I am ready to start the experiment.")

    if st.button('I Understand! Let\'s start the Experiment'):
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt", f"{datetime.now()}: Introduction to study completed and User study starts")

        if attentioncheck1:
            st.session_state.progress = 20
            if "timestamp" not in st.session_state:
                st.session_state["timestamp"] = datetime.now()
            switch_page("Userstudy")
        else:
            st.error("Make sure to read the explanations carefully and confirm it by ticking the checkbox above.")
except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")