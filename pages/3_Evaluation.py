import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from streamlit_extras import vertical_slider
import extra_streamlit_components as stx


def willingness_to_use_model():
    st.title('Willingness to Use the Model')
    willingness = st.select_slider(
        'Whether users can envision using such a model for a task.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return willingness

def skepticism_towards_ai_content():
    st.title('Skepticism Towards AI-generated Content')
    skepticism = st.select_slider(
        'General skepticism of users towards AI-generated content.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return skepticism

def ease_of_reading():
    st.title('Feedback on Reading Experience')
    reading_ease = st.select_slider(
        'I found it easy to read and understand the texts.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return reading_ease

def cognitive_load():
    st.title('Cognitive Load Assessment')
    cognitive_load = st.select_slider(
        'How mentally demanding was the task?',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return cognitive_load

def perceived_usefulness():
    st.title('Perceived Usefulness (PU)')
    usefulness1 = st.select_slider(
        'Using a RAG in my job would enable me to accomplish tasks more quickly.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    usefulness2 = st.select_slider(
        'Using would make it easier to perform a similar job.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return usefulness1, usefulness2

def perceived_ease_of_use():
    st.title('Perceived Ease-of-Use (PEU)')
    ease_of_use1 = st.select_slider(
        'I would find a RAG-system easy to use.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    ease_of_use2 = st.select_slider(
        'My interaction with a RAG-system would be clear and understandable.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return ease_of_use1, ease_of_use2
def behavioral_intention():
    st.title('Behavioral Intention (BI)')
    intention1 = st.select_slider(
        'I will consider using this service.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    intention2 = st.select_slider(
        'I will inform others of the goodness of a RAG service.',
        options=[
            'Strongly disagree',
            'Disagree',
            'Neither agree nor disagree',
            'Agree',
            'Strongly agree'
        ],
        value='Neither agree nor disagree'  # Default selection
    )
    return intention1, intention2


ease_of_reading = ease_of_reading()
skepticism = skepticism_towards_ai_content()
willingnessToUse = willingness_to_use_model()
cognitive_load = cognitive_load()
usefulness1, usefulness2 = perceived_usefulness()
ease_of_use1, ease_of_use2 = perceived_ease_of_use()
intention1, intention2 = behavioral_intention()

