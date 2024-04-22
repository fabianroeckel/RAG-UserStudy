import random
import uuid
import csv
import os
import pandas as pd
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from datetime import datetime

FOOTER_ROWS = 300
WHITE_VALUE = 255


def get_question_and_response(session_id):
    pd.set_option('display.max_colwidth', None)
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{session_id}.csv"
    user_df = pd.read_csv(user_file)

    question_id = user_df.iloc[st.session_state.question_number]["QuestionID"]
    question_type = user_df.iloc[st.session_state.question_number]["shuffled_questiontypes"]

    df = pd.read_csv("./data/RAG_Dataset.csv")
    if question_type == "Correct":
        study_dataset_df = df[df['Type'] == 'Correct']

    if question_type == "EvidentBaselessInformation":
        study_dataset_df = df[df['Type'] == 'BaselessInformation']

    if question_type == "EvidentConflict":
        study_dataset_df = df[df['Type'] == 'EvidentConflict']

    question = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Question"].values[0]
    response = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Response"].values[0]
    decision_options = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["DecisionOptions"].values[0]
    decision_options = decision_options[1:-1].split(', ')
    return question, response, decision_options


def get_sampled_question_ids():
    # Generate a list of 20 question IDs (for demonstration purpose, you can replace this with your actual logic)
    return random.sample(range(1, 31), 20)

def getSampledStudyType():
    study_type = random.sample(range(1, 3), 1)
    studyType_mapping = {
        1: "NoSources",
        2: "SingleSource",
        3: "MultiSource",
    }
    return studyType_mapping.get(study_type[0])


def getShuffledOrderOfQuestions():
    # Create a list with the desired distribution
    question_type = ["Correct"] * 10 + ["EvidentConflict"] * 5 + ["EvidentBaselessInformation"] * 5

    # Shuffle the list to get a random order
    random.shuffle(question_type)

    # Return the first element of the shuffled list
    return question_type


def getSourceLinks():


    return ""
def generateUserId():
    return str(uuid.uuid4())

def getSessionID():
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_id

@st.cache_data
def getCachedSessionID():
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_id



def generateNewCSFFiles (sessionID, sampled_studyType):
    # Initialize file counter
    filenameUserStudy = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    # Create a CSV file and write headers
    with open(filenameUserStudy, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userID', 'studyType','shuffled_questiontypes', 'QuestionID', 'Choice', 'Trust', 'Interaction'])

        # Get sampled question IDs
        sampled_question_ids = get_sampled_question_ids()

        ## indicates if a question is linked to correct or incorrect answer (Evident conflict or hallucination)
        shuffled_questiontypes = getShuffledOrderOfQuestions()

        # Write 20 rows to the CSV file
        for i in range(0,len(sampled_question_ids)):
            # Assuming 'Choice', 'Trust', 'Interaction' are placeholders and you need to fill them accordingly
            # You can modify this part according to your actual data generation logic
            choice = "SomeChoice"
            trust = "SomeTrust"
            interaction = 0
            writer.writerow([sessionID,sampled_studyType,shuffled_questiontypes[i], sampled_question_ids[i], choice, trust, interaction])

    fileNameGeneralQuestions = f"./data/raw_answers/UserGeneral/GeneralQuestions{sessionID}.csv"
    with open(fileNameGeneralQuestions, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userID', 'PreviousExperienceLLM', 'PreviousExperienceRAG'])



    print(f"CSV file '{filenameUserStudy}' and '{fileNameGeneralQuestions}' have been generated successfully.")


def update_questionaire(trust, choice):
    # Map likert scale options to numerical values
    trust_mapping = {'Not at all': 1, 'Slightly': 2, 'Moderately': 3, 'Very much': 4, 'Completely': 5}
    trust_numeric = trust_mapping[trust]

    # Load the CSV file
    file_path = f'./data/raw_answers/UserStudy/UserStudy_{st.session_state.sessionID}.csv'
    df = pd.read_csv(file_path)

    # Update the corresponding row in the DataFrame
    row = st.session_state.question_number  # Specify the row index you want to update
    #df.iloc[row]['Trust'] = trust_numeric
    #df.iloc[row]['Choice'] = choice

    # Write the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    st.session_state.question_number = st.session_state.question_number + 1
    if st.session_state.question_number == 19:
        switch_page("evaluation")
    else:
        st.rerun()


def displayPDF(file_path, ui_width):
    print("displayPDF")
    print(file_path)
    # Read file as bytes:
    with open(file_path, "rb") as file:
        bytes_data = file.read()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

def store_and_compute_time_difference():
    # Check if the 'timestamp' exists in the session state
    if 'timestamp' not in st.session_state:
        # Store the current timestamp
        st.session_state['timestamp'] = datetime.now()
        return {'current_timestamp': st.session_state['timestamp'], 'previous_timestamp': None, 'time_difference': None}
    else:
        # Compute the difference between now and the stored timestamp
        current_time = datetime.now()
        time_difference = (current_time - st.session_state['timestamp']).total_seconds()

        # Prepare the return data
        return_data = {
            'current_timestamp': current_time,
            'previous_timestamp': st.session_state['timestamp'],
            'time_difference': time_difference
        }

        # Update the stored timestamp to the current time
        st.session_state['timestamp'] = current_time

        return return_data


def get_source_links(sessionID):
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    user_df = pd.read_csv(user_file)
    studyType = st.session_state["sampled_study_type"]

    question_id = user_df.iloc[st.session_state.question_number]["QuestionID"]

    if studyType == "SingleSource":
        folder_path = f"data/source_documents/1_combined_documents/Q{question_id}"
        files = os.listdir(folder_path)
        if len(files) > 0:
            document_name = files[0]
            document_path = os.path.join(folder_path, document_name)
            return folder_path, document_path, document_name

    if studyType == "MultiSource":
        folder_path = f"data/source_documents/0_single_documents/Q{question_id}"
        files = os.listdir(folder_path)
        document_paths = [os.path.join(folder_path, file) for file in files]
        return document_paths, files



