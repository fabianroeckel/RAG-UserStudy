from utils import *
from streamlit_modal import Modal
import PyPDF2
from time import sleep
from datetime import datetime
from pdf2image import convert_from_path, convert_from_bytes
import boto3


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
        st.title(task)
        st.markdown("On the left side is the Chat with your RAG system which should help you to answer the question above. The red icon and tex box displays the question to the RAG-system. Behind the :orange[yellow icon is the answer given] from System. With all the source documents used to generate the content of the answer. "
                    "You can click the source documents and all the :orange[relevant passages are highlighted in yellow].")
        with st.expander(expander_title):
            st.markdown(expander_text)

        st.markdown("---")

    col_chat, col_questionaire = st.columns([6, 4])

    with col_chat:
        with st.container(height=600, border=True):

            display_chat_content()

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            st.markdown("---")
            if st.session_state.sampled_study_type == "SingleSource":
                open_modal = st.button(get_source_links(st.session_state.sessionID)[1][0])
                if open_modal:
                    st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][0]
                    st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][0]
                    st.session_state["source_clicks1"] += 1
                    st.session_state["source_watch_time1_datetime"] = datetime.now()
                    st.session_state["last_clicked_source"] = 1
                    modal.open()

            if st.session_state.sampled_study_type == "MultiSource":
                source1, source2, source3, source4, spacer = st.columns([2, 2, 2, 2, 2])
                with source1:
                    open_modal = st.button(get_source_links(st.session_state.sessionID)[1][0])
                    #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                    if open_modal:
                        st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][0]
                        st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][0]
                        st.session_state["source_clicks1"] += 1
                        st.session_state["source_watch_time1_datetime"] = datetime.now()
                        st.session_state["last_clicked_source"] = 1

                        modal.open()
                with source2:
                    open_modal = st.button(get_source_links(st.session_state.sessionID)[1][1])
                    #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                    if open_modal:
                        st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][1]
                        st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][1]
                        st.session_state["source_clicks2"] += 1
                        st.session_state["total_source_clicks"] += 1
                        st.session_state["source_watch_time2_datetime"] = datetime.now()
                        st.session_state["last_clicked_source"] = 2
                        modal.open()
                if len(get_source_links(st.session_state.sessionID)[1]) >2:
                    with source3:
                        open_modal = st.button(get_source_links(st.session_state.sessionID)[1][2])
                       #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                        if open_modal:
                            st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][2]
                            st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][2]
                            st.session_state["source_clicks3"] += 1
                            st.session_state["total_source_clicks"] += 1
                            st.session_state["source_watch_time3_datetime"] = datetime.now()
                            st.session_state["last_clicked_source"] = 3
                            modal.open()
                if len(get_source_links(st.session_state.sessionID)[1]) > 3:
                    with source4:
                        open_modal = st.button(get_source_links(st.session_state.sessionID)[1][3])
                        #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                        if open_modal:
                            st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][3]
                            st.session_state["source_name"] = get_source_links(st.session_state.sessionID)[1][3]
                            st.session_state["source_clicks4"] += 1
                            st.session_state["total_source_clicks"] += 1
                            st.session_state["source_watch_time4_datetime"] = datetime.now()
                            st.session_state["last_clicked_source"] = 4
                            modal.open()

    with col_questionaire:
        with st.form("user form", clear_on_submit=True):
            st.subheader('Please answer these questions below')
            st.markdown("Based on the question, answer and sources given on the left.")
            st.markdown("----")
            decision = st.radio(f'**{task}**', decision_options,index=0, horizontal=False)
            st.markdown('----')
            trust = st.select_slider('**I trust the accuracy and reliability of the answer provided by this system.**',
                                     options=['1. Strongly Disagree',
                                                '2. Disagree',
                                                '3. Somewhat Disagree',
                                                '4. Neither Disagree nor Agree',
                                                '5. Somewhat Agree',
                                                '6. Agree',
                                                '7. Strongly Agree'])
            st.markdown('----')
            # Radio button to select whether there is an error
            error = st.radio("**Did you detect an error in the response?**", ("No", "Yes"), index=0, horizontal=True)
            error_text = st.text_input("**If you detect an error, paste the content of the error inside this text field**")
            if st.form_submit_button():
                timeSpentPerTask = store_and_compute_time_difference("timestamp")
                print("Time spent")
                print(timeSpentPerTask["time_difference"])
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