import random
import uuid
import csv
import os
import pandas as pd
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import urllib
import base64

def getQuestion (sessionID, numberQuestion):
    pd.set_option('display.max_colwidth', None)
    # Load the dataset file
    dataset_file = "data/RAG_Dataset.csv"
    dataset_df = pd.read_csv(dataset_file)
    # Load the user-specific file
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    user_df = pd.read_csv(user_file)

    # Get the first QuestionID from the user-specific file
    first_question_id = user_df.loc[numberQuestion, "QuestionID"]
    print(f"first_question_id {first_question_id}")

    # Find the row in the dataset file with the matching QuestionID
    matching_row = dataset_df.loc[dataset_df["QuestionID"] == first_question_id]
    print(matching_row["Question"].values[0])
    return matching_row["Question"].values[0]

def getResponse(sessionID, numberQuestion):
    pd.set_option('display.max_colwidth', None)
    # Load the dataset file
    dataset_file = "data/RAG_Dataset.csv"
    dataset_df = pd.read_csv(dataset_file)
    # Load the user-specific file
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    user_df = pd.read_csv(user_file)

    # Get the first QuestionID from the user-specific file
    first_question_id = user_df.loc[numberQuestion, "QuestionID"]
    print(f"first_question_id {first_question_id}")

    # Find the row in the dataset file with the matching QuestionID
    matching_row = dataset_df.loc[dataset_df["QuestionID"] == first_question_id]
    print(matching_row["ResponseCorrect"].values[0])
    return matching_row["ResponseCorrect"].values[0]

def getSampledQuestionIDs():
    # Generate a list of 20 question IDs (for demonstration purpose, you can replace this with your actual logic)
    return random.sample(range(1, 41), 20)

def getSampledStudyType():
    study_type = random.sample(range(1, 3), 1)
    studyType_mapping = {
        1: "NoSources",
        2: "SingleSource",
        3: "MultiSource",
    }
    return studyType_mapping.get(study_type[0])

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
    session_id = random.randint(1,10)
    return session_id



def generateNewCSFFiles (sessionID):
    # Initialize file counter
    filenameUserStudy = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    print("SESSION-ID")
    print(sessionID)
    # Create a CSV file and write headers
    with open(filenameUserStudy, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userID', 'studyType', 'QuestionID', 'Choice', 'Trust', 'Interaction'])

        # Get sampled question IDs
        sampled_question_ids = getSampledQuestionIDs()
        sampled_studyType = getSampledStudyType()

        # Write 20 rows to the CSV file
        for question_id in sampled_question_ids:
            # Assuming 'Choice', 'Trust', 'Interaction' are placeholders and you need to fill them accordingly
            # You can modify this part according to your actual data generation logic
            choice = "SomeChoice"
            trust = "SomeTrust"
            interaction = 0
            writer.writerow([sessionID,sampled_studyType, question_id, choice, trust, interaction])

    fileNameGeneralQuestions = f"./data/raw_answers/UserGeneral/GeneralQuestions{sessionID}.csv"
    with open(fileNameGeneralQuestions, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userID', 'PreviousExperienceLLM', 'PreviousExperienceRAG'])



    print(f"CSV file '{filenameUserStudy}' and '{fileNameGeneralQuestions}' have been generated successfully.")


def update_questionaire(trust, choice, session_id, page_number):
    # Map likert scale options to numerical values
    trust_mapping = {'Not at all': 1, 'Slightly': 2, 'Moderately': 3, 'Very much': 4, 'Completely': 5}
    trust_numeric = trust_mapping[trust]

    # Load the CSV file
    file_path = f'./data/raw_answers/UserStudy/UserStudy_{session_id}.csv'
    df = pd.read_csv(file_path)

    # Update the corresponding row in the DataFrame
    row = page_number  # Specify the row index you want to update
    df.loc[row, 'Trust'] = trust_numeric
    df.loc[row, 'Choice'] = choice

    # Write the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    st.session_state.question_number = st.session_state.question_number +1
    st.rerun()

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 100%;">"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(layout="wide")