import random
import uuid
import csv
import os
import pandas as pd
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from pdf2image import convert_from_path, pdfinfo_from_path

FOOTER_ROWS = 300
WHITE_VALUE = 255


def get_question_and_response(session_id):




    pd.set_option('display.max_colwidth', None)
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{session_id}.csv"
    user_df = pd.read_csv(user_file)

    question_id = user_df.iloc[st.session_state.question_number]["QuestionID"]
    question_type = user_df.iloc[st.session_state.question_number]["shuffled_questiontypes"]

    df = pd.read_csv("data/RAG_Dataset.csv")
    if question_type == "Correct":
        study_dataset_df = df[df['Type'] == 'Correct']

    if question_type == "EvidentBaselessInformation":
        study_dataset_df = df[df['Type'] == 'BaselessInformation']

    if question_type == "EvidentConflict":
        study_dataset_df = df[df['Type'] == 'EvidentConflict']

    if question_type == "AttentionCheck":
        study_dataset_df = df[df['Type'] == 'AttentionCheck']



    question = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Question"].values[0]

    response = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Response"].values[0]

    if st.session_state.sampled_study_type == "SingleSource":
        response = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Response-Single"].values[0]
    if st.session_state.sampled_study_type == "NoSources":
        response = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Response-Single"].values[0]

    expander_title = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["ExpanderTitle"].values[0]
    expander_text = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["ExpanderText"].values[0]
    task = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Task"].values[0]
    decision_options = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["DecisionOptions"].values[0]
    decision_options = decision_options.split(';')
    return question, response, decision_options, task, expander_title, expander_text


def get_sampled_question_ids():
    # Generate a list of 20 question IDs (for demonstration purpose, you can replace this with your actual logic)
    return random.sample(range(1, 22), 12)

def getSampledStudyType():
    study_type = random.sample(range(1, 4), 1)
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
        writer.writerow(['userID', 'studyType','shuffled_questiontypes', 'QuestionID', 'Choice', 'Trust', 'TaskCompletionTime', "ClicksSource1", "ClicksSource2", "ClicksSource3", "ClicksSource4","TotalClicks", "ViewTimeSource1", "ViewTimeSource2", "ViewTimeSource3", "ViewTimeSource4", "TotalViewTime"])

        # Get sampled question IDs
        sampled_question_ids = get_sampled_question_ids()

        ## indicates if a question is linked to correct or incorrect answer (Evident conflict or hallucination)
        shuffled_questiontypes = getShuffledOrderOfQuestions()

        # Write 20 rows to the CSV file
        for i in range(0,len(sampled_question_ids)+1):
            # Assuming 'Choice', 'Trust', 'Interaction' are placeholders and you need to fill them accordingly
            # You can modify this part according to your actual data generation logic
            if i < 7:
                writer.writerow([sessionID,sampled_studyType,shuffled_questiontypes[i], sampled_question_ids[i], "SomeChoice", "SomeTrust", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            if i == 7:
                writer.writerow([sessionID, sampled_studyType, "AttentionCheck", 21, "SomeChoice", "SomeTrust", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            if i > 7:
                writer.writerow([sessionID, sampled_studyType, shuffled_questiontypes[i-1], sampled_question_ids[i-1], "SomeChoice",
                     "SomeTrust", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    fileNameGeneralQuestions = f"./data/raw_answers/UserGeneral/GeneralQuestions{sessionID}.csv"
    with open(fileNameGeneralQuestions, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userID', 'PreviousExperienceLLM', 'PreviousExperienceRAG'])



    print(f"CSV file '{filenameUserStudy}' and '{fileNameGeneralQuestions}' have been generated successfully.")


def update_questionaire(trust, choice, task_completion_time,
                        ClicksSource1, ClicksSource2, ClicksSource3, ClicksSource4,
                        ViewTimeSource1, ViewTimeSource2, ViewTimeSource3, ViewTimeSource4):

    # Map likert scale options to numerical values
    trust_mapping = {'Not at all': 1, 'Slightly': 2, 'Somewhat': 3, 'Moderately': 4, 'Very much': 5, 'Quite a lot': 6,
                     'Completely': 7}
    trust_numeric = trust_mapping[trust]

    # Load the CSV file
    file_path = f'./data/raw_answers/UserStudy/UserStudy_{st.session_state.sessionID}.csv'
    df = pd.read_csv(file_path)

    # Update the corresponding row in the DataFrame
    row = st.session_state.question_number  # Specify the row index you want to update
    df.loc[row, 'Trust'] = trust_numeric
    df.loc[row, 'Choice'] = choice
    df.loc[row, 'TaskCompletionTime'] = int(task_completion_time)

    #Clicks
    totalClicks = (ClicksSource1 + ClicksSource2 + ClicksSource3 + ClicksSource4)
    df.loc[row, "ClicksSource1"] = ClicksSource1
    df.loc[row, "ClicksSource2"] = ClicksSource2
    df.loc[row, "ClicksSource3"] = ClicksSource3
    df.loc[row, "ClicksSource4"] = ClicksSource4
    df.loc[row, "TotalClicks"] = totalClicks

    #ViewTime
    df.loc[row, "ViewTimeSource1"] = int(ViewTimeSource1)
    df.loc[row, "ViewTimeSource2"] = int(ViewTimeSource2)
    df.loc[row, "ViewTimeSource3"] = int(ViewTimeSource3)
    df.loc[row, "ViewTimeSource4"] = int(ViewTimeSource4)
    df.loc[row, "TotalViewTime"] = int(ViewTimeSource1 + ViewTimeSource2 + ViewTimeSource3 + ViewTimeSource4)


    # Write the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    st.session_state.question_number = st.session_state.question_number + 1

    # Clicks
    st.session_state["source_clicks1"] = 0
    st.session_state["source_clicks2"] = 0
    st.session_state["source_clicks3"] = 0
    st.session_state["source_clicks4"] = 0

    # ViewTime
    st.session_state["source_watch_time1"] = 0
    st.session_state["source_watch_time2"] = 0
    st.session_state["source_watch_time3"] = 0
    st.session_state["source_watch_time4"] = 0

    ##Reset States to 0
    if st.session_state.question_number == 13:
        print("All tasks completed")
        switch_page("evaluation")
    else:
        st.rerun()


def displayPDF(file_path, ui_width):

    info = pdfinfo_from_path(file_path, userpw=None, poppler_path=None)

    maxPages = info["Pages"]
    for page in range(1, maxPages + 1, 5):
        images_from_path = convert_from_path(file_path, dpi=200,thread_count=3, first_page=page,use_pdftocairo=True, last_page=min(page + 5 - 1, maxPages))
        for page in images_from_path:
            st.image(page)

def store_and_compute_time_difference(var_name):
    # Check if the 'timestamp' exists in the session state
    if st.session_state[var_name] == 0:
        # Store the current timestamp
        st.session_state[var_name] = datetime.now()
        return {'current_timestamp': st.session_state[var_name], 'previous_timestamp': None, 'time_difference': None}
    else:
        # Compute the difference between now and the stored timestamp
        current_time = datetime.now()
        time_difference = (current_time - st.session_state[var_name]).total_seconds()
        # Prepare the return data
        return_data = {
            'current_timestamp': current_time,
            'previous_timestamp': st.session_state[var_name],
            'time_difference': time_difference
        }

        # Update the stored timestamp to the current time
        st.session_state[var_name] = current_time

        return return_data


def get_source_links(sessionID):
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    user_df = pd.read_csv(user_file)
    studyType = st.session_state["sampled_study_type"]
    question_id = user_df.iloc[st.session_state.question_number]["QuestionID"]

    if studyType == "SingleSource":
        folder_path = f"data/source_documents/1_combined_documents/Q{question_id}"
    elif studyType == "MultiSource":
        folder_path = f"data/source_documents/0_single_documents_v2/Q{question_id}"
    else:
        raise ValueError("Invalid studyType")

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    files = os.listdir(folder_path)
    document_paths = [os.path.join(folder_path, file) for file in files]

    print("folder_path:", folder_path)
    print("files:", files)

    return document_paths, files
