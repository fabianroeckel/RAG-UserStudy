from utils import *
from streamlit_modal import Modal
import PyPDF2
from time import sleep
from datetime import datetime
from pdf2image import convert_from_path, convert_from_bytes
import boto3
from module import *


try:
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
        modal = Fabi_Modal(title=st.session_state["source_name"],
            key="demo-modal",
            # Optional
            padding=20,  # default value
            max_width=1000  # default value
        )
        if modal.is_open():

            with modal.container():
                file_path = st.session_state["source_link"]
                with st.container(height=800):
                    displayPDF(file_path, 900)


        question, response, decision_options, task, expander_title, expander_text, correctResponse = get_question_and_response(st.session_state.sessionID)

        st.progress(st.session_state.progress, f"Study Progress: {st.session_state.progress}% Complete")
        st.title("Complete your task on the right using the information provided in the chat interface")
        st.markdown("On the left side, you will find the chat with your RAG, designed to assist you in answering the question on the right. The red icon and text box display the question submitted to the RAG system. The yellow icon indicates the system's response, including all the source documents used to generate the answer.")
        if st.session_state["sampled_study_type"] != "NoSources":
            st.markdown("By clicking on the source documents, all relevant passages will be highlighted in yellow for easy reference.")
        with st.expander(expander_title):
            st.markdown(expander_text)

        st.markdown("---")

    col_chat, col_questionaire = st.columns([6, 4])

    with col_chat:
        with st.container(height=750, border=True):
            st.subheader('Chat Interface')

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
                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Source: {st.session_state['source_name']} opened")
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
                        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                    f"{datetime}: Source: {st.session_state['source_name']} opened")
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
                        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                    f"{datetime}: Source: {st.session_state['source_name']} opened")
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
                            log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                        f"{datetime}: Source: {st.session_state['source_name']} opened")
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
                            log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                        f"{datetime}: Source: {st.session_state['source_name']} opened")
                            modal.open()

    with col_questionaire:
        with st.form("user form", clear_on_submit=True):
            st.subheader('Your Task')
            st.markdown("Answer the questions below, based on the questions and answer given on the left.")
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
            trust = st.radio('**I trust the accuracy and reliability of the answer provided by this system.**',
                                     options=['1. Strongly Disagree',
                                                '2. Disagree',
                                                '3. Somewhat Disagree',
                                                '4. Neither Disagree nor Agree',
                                                '5. Somewhat Agree',
                                                '6. Agree',
                                                '7. Strongly Agree'],
                                     horizontal=False, index=None)
            st.markdown('----')
            # Radio button to select whether there is an error
            error = st.radio("**Did you detect an error in the response?**", ("Dummy", "No", "Yes"), index=0, horizontal=False)
            error_text = st.text_input("**If you detect an error, paste the content of the error inside this text field**")
            if st.form_submit_button():
                if int(decision[0]) < 1 or error == "Dummy" or trust is None :
                    st.error("You need to answer all the questions (Decision, Trust and Error-Detection!)")
                if (int(decision[0]) > 0 and error != "Dummy" ) and trust is not None:
                    st.session_state.progress += 8
                    timeSpentPerTask = store_and_compute_time_difference("timestamp")
                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt", f"{datetime}: Time spent on this taks: {timeSpentPerTask['time_difference']}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Decision correct(Y/N): {decision[0]} with the correct response being: {correctResponse}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Selected trust {trust}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Selected error {error}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: ErrorText: {error_text}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Clicks on source1 {st.session_state['source_clicks1']}, source2 {st.session_state['source_clicks2']}, source3 {st.session_state['source_clicks3']}, source4 {st.session_state['source_clicks4']}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Watch time on source1 {st.session_state['source_watch_time1']}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Watch time on source1 {st.session_state['source_watch_time2']}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Watch time on source1 {st.session_state['source_watch_time3']}")

                    log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                                f"{datetime}: Watch time on source1 {st.session_state['source_watch_time4']}")

                    update_questionaire(trust,
                                        decision[0],
                                        error,
                                        correctResponse,
                                        error_text,
                                        timeSpentPerTask["time_difference"],
                                        st.session_state["source_clicks1"],
                                        st.session_state["source_clicks2"],
                                        st.session_state["source_clicks3"],
                                        st.session_state["source_clicks4"],
                                        st.session_state["source_watch_time1"],
                                        st.session_state["source_watch_time2"],
                                        st.session_state["source_watch_time3"],
                                        st.session_state["source_watch_time4"])

except (KeyError, AttributeError) as e:
    print('I got a KeyError - reason "%s"' % str(e))
    switch_page("streamlit_app")