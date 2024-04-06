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
from pdf2jpg import pdf2jpg
import numpy as np
from PIL import Image
import shutil

FOOTER_ROWS = 300
WHITE_VALUE = 255

def getQuestion (sessionID, numberQuestion):
    print(numberQuestion)
    pd.set_option('display.max_colwidth', None)
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    user_df = pd.read_csv(user_file)
    # Find the row in the dataset file with the matching QuestionID

    #question_id = user_df.iloc[[numberQuestion]]["QuestionID"]

    #question_type = user_df.iloc[[numberQuestion]]["shuffled_questiontypes"]
    print("user_df.iloc[numberQuestion]")
    print(user_df.iloc[numberQuestion])
    question_id = user_df.iloc[numberQuestion]["QuestionID"]
    question_type = user_df.iloc[numberQuestion]["shuffled_questiontypes"]
    print(f"Question_type: {question_type}")
    study_dataset_df = ""
    if question_type == "Correct":
        study_dataset_df = pd.read_csv("./data/RAG_Dataset-Correct_Responses.csv")
        print(study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Question"])

    if question_type == "EvidentBaselessInformation":
        study_dataset_df = pd.read_csv("./data/RAG_Dataset-Evident_Baseless_Information.csv", on_bad_lines='skip')

    if question_type == "EvidentConflict":
        study_dataset_df = pd.read_csv("./data/RAG_Dataset-Evident_Conflict.csv")


    question = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Question"].values[0]
    return question

def getQuestionAndResponse (sessionID):
    pd.set_option('display.max_colwidth', None)
    user_file = f"./data/raw_answers/UserStudy/UserStudy_{sessionID}.csv"
    user_df = pd.read_csv(user_file)


    question_id = user_df.iloc[st.session_state.question_number]["QuestionID"]
    question_type = user_df.iloc[st.session_state.question_number]["shuffled_questiontypes"]


    if question_type == "Correct":
        study_dataset_df = pd.read_csv("./data/RAG_Dataset-Correct_Responses.csv")
        print(study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Question"])

    if question_type == "EvidentBaselessInformation":
        study_dataset_df = pd.read_csv("./data/RAG_Dataset-Evident_Baseless_Information.csv", on_bad_lines='skip')

    if question_type == "EvidentConflict":
        study_dataset_df = pd.read_csv("./data/RAG_Dataset-Evident_Conflict.csv")


    question = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Question"].values[0]
    response = study_dataset_df.loc[study_dataset_df["QuestionID"] == question_id]["Response"].values[0]
    return question, response

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


def getShuffledOrderOfQuestions():
    # Create a list with the desired distribution
    question_type = ["Correct"] * 10 + ["EvidentConflict"] * 3 + ["EvidentBaselessInformation"] * 7

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
        sampled_question_ids = getSampledQuestionIDs()

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



def displayPDF(file_path, ui_width):
    # Read file as bytes:
    with open(file_path, "rb") as file:
        bytes_data = file.read()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)