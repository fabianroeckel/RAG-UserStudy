import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from loguru import logger
import datetime

def main():
    st.progress(5, f"Study Progress: 5% Complete")
    st.header('Consent to Participate')
    st.markdown(
                """Data protection information 
We thank you for your interest in our Prolific Study.
1. Data: 
Within the scope of your participation in the above study, we will be processing data of the participants. 
Within this study, these are the following pieces of information concerning you: Prolific Worker ID (note that this will only be used to pay you and ensure you participate only once. The ID will be deleted after the payment has been made.); Payment resulting from this study.
2. Person Responsible:  
Responsible for the data processing within the scope of the GDPR as well as other data protection regulations is: 
The University of Bayreuth is a body governed by public law. It is represented by President Professor Dr. Stefan Leible.
The Data Protection Officer is Thomas Frahnert.
3. Purpose of data processing 
The University of Bayreuth processes your data solely for specified, unambiguous and legitimate purposes. The purpose of the data processing in the present is to carry out the study. 

4. Legal basis for data processing: 
The legal basis for the processing of your data is your consent in accordance with Art. 6, Abs. 1 a) of GDPR. 
Consent is granted voluntarily. Consent can be revoked at any time with the effect for the future. Effect for the future means that a withdrawal of consent does not affect the legality of the processing carried out based on the consent until the revocation. 
If consent is refused or revoked, there are no disadvantages. 
5. Description of data processing: 
Participants will be presented with scenarios where a GenAI system answers questions, divided into groups with varying levels of access to source citations to explore how these features influence their trust in responses and decision-making. Data collected will be confidential, stored, and processed anonymously, accessible only to authorized personnel, and shared only with research partners; once payment is completed, identifying information will be deleted. Participation is voluntary, and you can withdraw anytime without consequences; if requested before the deletion of your Prolific Worker ID, your data will be deleted in full or in part.

6. Recipient: 
In principle, your data will not be transmitted to third parties. 
If it is exceptionally necessary for external service providers to process data for us on behalf of us, these are carefully selected by us and contractually obliged. The respective service providers will work exclusively according to our instructions. We ensure this through strict contractual regulations, technical and organizational measures and additional controls. 
There is no transfer of data to third countries outside the EU or the EEA or to an international organization. Automated decision-making, including profiling, is not performed. 
7. Storage time: 
The Prolific ID, the individual participation code as well as the declaration of consent will be deleted immediately after the completion of the payment. The anonymized research data will be kept for research and might be published in a report or journal article. 
8. Rights: 
You have the following rights in relation to your data: the right to confirm whether data concerning you is processed and to obtain information about the data processed, to further information on data processing and to copies of the data (Art. 15 GDPR); the right to correct or complete inaccurate or incomplete data (Art. 16 GDPR), right to immediate deletion of the data concerning you (Art. 17 GDPR); right to restrict processing (Article 18 GDPR); right to receive the data concerning you and provided by you and to transfer this data to other controllers (Art. 20 GDPR). 
You also have the right to complain to the supervisory authority about the processing of your data by the University of Bayreuth (Art. 77 GDPR). Supervisory authority within the meaning of Article 51 (1) GDPR on the University of Bayreuth is to be 
The State Commissioner for Data Protection and Freedom of Information Bayern is 
Prof. Dr. Thomas Petri
Wagmüllerstraße 18, 
80538 München
Email: poststelle@datenschutz-bayern.de
""")
    st.write('I am aware that consent is voluntary and can be refused without disadvantages or revoked at any time without giving reasons. I know that in the event of a revocation, the lawfulness of the processing carried out on the basis of the consent until the revocation is not affected. I understand that in order to revoke, I can simply contact the contact persons mentioned in the information.')
    st.markdown("**By clicking on the button I consent to participate in this study.**")
    if st.button('I consent'):
        log_to_file(f"./data/raw_answers/Logs/logs_{st.session_state['sessionID']}.txt",
                    f"{datetime.datetime.now()}: consent granted ")
        switch_page("initialQuestions_RAG")
main()