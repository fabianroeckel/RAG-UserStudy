from utils import *
from streamlit_modal import Modal
import PyPDF2
from time import sleep

def display_chat_content():
    st.session_state.messages = []
    st.session_state.messages.append({"role": "user", "content": get_question_and_response(st.session_state.sessionID)[0]})
    st.session_state.messages.append({"role": "assistant", "content": get_question_and_response(st.session_state.sessionID)[1]})


with st.sidebar:
    st.progress(random.randint(1, 100))

    st.write(pd.read_csv(f'./data/raw_answers/UserStudy/UserStudy_{st.session_state.sessionID}.csv'))



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
            file_path = st.session_state["source_link"]
            file = open(file_path, 'rb')
            pdfReader = PyPDF2.PdfReader(file)
            if pdfReader.is_encrypted:
                pdfReader.decrypt('')

            displayPDF(file_path, 685)

    question = get_question_and_response(st.session_state.sessionID)[0]
    st.header(question)
    st.text("You can use the chat interface to interact with your financial Co-Pilot to answer this task.")

    st.markdown("---")

col_chat, col_questionaire = st.columns([6, 4])

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
            source1, source2, source3, source4, spacer = st.columns([2, 2, 2, 2, 2])
            with source1:
                open_modal = st.button(get_source_links(st.session_state.sessionID)[1][0])
                #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                if open_modal:
                    st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][0]
                    modal.open()
            with source2:
                open_modal = st.button(get_source_links(st.session_state.sessionID)[1][1])
                #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                if open_modal:
                    st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][1]
                    modal.open()
            if len(get_source_links(st.session_state.sessionID)[1]) >2:
                with source3:
                    open_modal = st.button(get_source_links(st.session_state.sessionID)[1][2])
                   #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                    if open_modal:
                        st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][2]
                        modal.open()
            if len(get_source_links(st.session_state.sessionID)[1]) > 3:
                with source4:
                    open_modal = st.button(get_source_links(st.session_state.sessionID)[1][3])
                    #st.session_state["source_link"] = "data/source_documents/0_single_documents/Q2/2022 Q3 AAPL.pdf"
                    if open_modal:
                        st.session_state["source_link"] = get_source_links(st.session_state.sessionID)[0][3]
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
        decision = st.radio("Which company had the best quarter?", get_question_and_response(st.session_state.sessionID)[2], horizontal=False)

        # Radio button to select whether there is an error
        detect_error = st.radio("Did you detect an error in the response?", ("No", "Yes"), index=0, horizontal=True,)
        error_content = st.text_input("Paste the content of the error inside this text field")
        if st.form_submit_button():
            timeSpentPerTask = store_and_compute_time_difference()
            print("Time spent")
            print(timeSpentPerTask["time_difference"])
            update_questionaire(trust, decision)
