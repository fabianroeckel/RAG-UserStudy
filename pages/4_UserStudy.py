from utils import *
from streamlit_modal import Modal
import PyPDF2
from time import sleep
from datetime import datetime
from pdf2image import convert_from_path, convert_from_bytes
import boto3
from loguru import logger


try:
    logname = f"data/raw_answers/Logs/logs_{st.session_state['sessionID']}.log"
    logger.add(logname)

    def display_chat_content():
        st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response})

    def display_chat_input_field():
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

    with st.container():
        modal = Modal(title=st.session_state["source_name"],
            key="demo-modal",
            # Optional
            padding=20,  # default value
            max_width=1000  # default value
        )
        if modal.is_open():
            with modal.container():
                file_path = st.session_state["source_link"]
                file = open(file_path, 'rb')
                pdfReader = PyPDF2.PdfReader(file)
                if pdfReader.is_encrypted:
                    pdfReader.decrypt('')

                displayPDF(file_path, 900)

        question, response, decision_options, task, expander_title, expander_text = get_question_and_response(st.session_state.sessionID)

        st.progress(st.session_state.progress, f"Study Progress: {st.session_state.progress}% Complete")
        st.title(task)
        st.markdown("On the left side, you will find the chat with your RAG system, designed to assist you in answering the question above. The red icon and text box display the question submitted to the RAG system. The yellow icon indicates the system's response, including all the source documents used to generate the answer. By clicking on the source documents, all relevant passages will be highlighted in yellow for easy reference.")
        with st.expander(expander_title):
            st.markdown(expander_text)

        st.markdown("---")

    col_chat, col_questionaire = st.columns([6, 4])

    with col_chat:
        with st.container(height=750, border=True):

            display_chat_content()

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            st.markdown("---")
            if st.session_state.sampled_study_type == "SingleSource":
                open_modal = st.button(str(f"[1] {str(get_source_links(st.session_state.sessionID)[1][0])}"))
                if open_modal:
                    st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][0]
                    st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][0]
                    st.session_state["source_clicks1"] += 1
                    st.session_state["source_watch_time1_datetime"] = datetime.now()
                    st.session_state["last_clicked_source"] = 1
                    logger.info(f"Source: {st.session_state['source_name']} opened")
                    modal.open()

            if st.session_state.sampled_study_type == "MultiSource":
                source1, source2, source3, source4, spacer = st.columns([2, 2, 2, 2, 2])
                with source1:
                    open_modal = st.button(str(f"[1] {str(get_source_links(st.session_state.sessionID)[1][0])}"))
                    if open_modal:
                        st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][0]
                        st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][0]
                        st.session_state["source_clicks1"] += 1
                        st.session_state["source_watch_time1_datetime"] = datetime.now()
                        st.session_state["last_clicked_source"] = 1
                        logger.info(f"Source: {st.session_state['source_name']} opened")
                        modal.open()
                with source2:
                    open_modal = st.button(str(f"[2] {str(get_source_links(st.session_state.sessionID)[1][1])}"))
                    if open_modal:
                        st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][1]
                        st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][1]
                        st.session_state["source_clicks2"] += 1
                        st.session_state["total_source_clicks"] += 1
                        st.session_state["source_watch_time2_datetime"] = datetime.now()
                        st.session_state["last_clicked_source"] = 2
                        logger.info(f"Source: {st.session_state['source_name']} opened")
                        modal.open()
                if len(get_source_links(st.session_state.sessionID)[1]) >2:
                    with source3:
                        open_modal = st.button(str(f"[3] {str(get_source_links(st.session_state.sessionID)[1][2])}"))
                        if open_modal:
                            st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][2]
                            st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][2]
                            st.session_state["source_clicks3"] += 1
                            st.session_state["total_source_clicks"] += 1
                            st.session_state["source_watch_time3_datetime"] = datetime.now()
                            st.session_state["last_clicked_source"] = 3
                            logger.info(f"Source: {st.session_state['source_name']} opened")
                            modal.open()
                if len(get_source_links(st.session_state.sessionID)[1]) > 3:
                    with source4:
                        open_modal = st.button(str(f"[4] {str(get_source_links(st.session_state.sessionID)[1][3])}"))
                        if open_modal:
                            st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][3]
                            st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][3]
                            st.session_state["source_clicks4"] += 1
                            st.session_state["total_source_clicks"] += 1
                            st.session_state["source_watch_time4_datetime"] = datetime.now()
                            st.session_state["last_clicked_source"] = 4
                            logger.info(f"Source: {st.session_state['source_name']} opened")
                            modal.open()

    with col_questionaire:
        with st.form("user form", clear_on_submit=True):
            st.subheader('Please answer these questions below')
            st.markdown("Based on the question, answer and sources given on the left.")
            st.markdown("----")
            decision = st.radio(f'**{task}**', decision_options,index=0, horizontal=False)

            st.markdown(
                """
            <style>
                div[role=radiogroup] label:first-of-type {
                    visibility: hidden;
                    height: 0px;
                }
            </style>
            """,
                unsafe_allow_html=True,
            )
            st.markdown('----')
            trust = st.select_slider('**I trust the accuracy and reliability of the answer provided by this system.**',
                                     options=['1. Strongly Disagree',
                                                '2. Disagree',
                                                '3. Somewhat Disagree',
                                                '4. Neither Disagree nor Agree',
                                                '5. Somewhat Agree',
                                                '6. Agree',
                                                '7. Strongly Agree'],
                                     value='4. Neither Disagree nor Agree')
            st.markdown('----')
            # Radio button to select whether there is an error
            error = st.radio("**Did you detect an error in the response?**", ("Dummy", "No", "Yes"), index=0, horizontal=False)
            error_text = st.text_input("**If you detect an error, paste the content of the error inside this text field**")
            if st.form_submit_button():
                st.session_state.progress += 5
                timeSpentPerTask = store_and_compute_time_difference("timestamp")
                logger.info(f"Time spent on this taks: {timeSpentPerTask['time_difference']}")
                logger.info(f"Selected trust {trust}")
                logger.info(f"Selected error {error}")
                logger.info(f"Selected error {error_text}")
                logger.info(f"Selected error {error_text}")
                logger.info(f"Clicks on source1 {st.session_state['source_clicks1']}")
                logger.info(f"Clicks on source2 {st.session_state['source_clicks2']}")
                logger.info(f"Clicks on source3 {st.session_state['source_clicks3']}")
                logger.info(f"Clicks on source4 {st.session_state['source_clicks4']}")
                logger.info(f"Watch time on source1 {st.session_state['source_watch_time1']}")
                logger.info(f"Watch time on source2 {st.session_state['source_watch_time2']}")
                logger.info(f"Watch time on source3 {st.session_state['source_watch_time3']}")
                logger.info(f"Watch time on source4 {st.session_state['source_watch_time4']}")
                update_questionaire(trust,
                                    decision,
                                    error,
                                    error_text,
                                    timeSpentPerTask["time_difference"],
                                    st.session_state["source_clicks1"],
                                    st.session_state["source_clicks2"],
                                    st.session_state["source_clicks3"],
                                    st.session_state["source_clicks4"],
                                    st.session_state["source_watch_time1"],
                                    st.session_state["source_watch_time2"],
                                    st.session_state["source_watch_time3"],
                                    st.session_state["source_watch_time4"]
                                    )
except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")