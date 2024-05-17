import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *

def main():
    st.progress(5, f"Study Progress: 5% Complete")
    st.header('Consent to Participate')
    st.markdown(
                """Data protection information 
We thank you for your interest in our Prolific Study on “Investigating Appropriate Reliance in Retrieval Augmented Generation Systems”. The purpose of this survey is to collect information about the influence of sources and citations on a person’s reliance on RAG-systems.
1. Data 
Within the scope of your participation in the above study, we will be processing data of the participants. 
Within this study, these are the following pieces of information concerning you: 
•	Prolific Worker ID (note that this will only be used to pay you and ensure you participate only once. The ID will be deleted after the payment has been made.) 
•	Payment resulting from this study.
2. Person Responsible 
Responsible for the data processing within the scope of the GDPR as well as other data protection regulations is: 
The University of Bayreuth is a body governed by public law. It is represented by President Professor Dr. Stefan Leible.
The Data Protection Officer is Thomas Frahnert.
3. Purpose of data processing 
The University of Bayreuth processes your data solely for specified, unambiguous and legitimate purposes. The purpose of the data processing in the present is to carry out the study “From Documents to Decisions – Investigating Appropriate Reliance in Retrieval Augmented Generation Systems”. 


4. Legal basis for data processing 
The legal basis for the processing of your data is your consent in accordance with Art. 6, Abs. 1 a) of GDPR. 
Consent is granted voluntarily. Consent can be revoked at any time with the effect for the future. Effect for the future means that a withdrawal of consent does not affect the legality of the processing carried out based on the consent until the revocation. 
If consent is refused or revoked, there are no disadvantages. 
5. Description of data processing 
Upon consenting to participate, you'll be presented with scenarios where a Retrieval-Augmented Generation (RAG) system provides answers based on document retrieval. You'll review the generated response and, depending on the study group, verify the information through one or more source documents. Participants will be divided into groups with varying levels of access to source citations, allowing for an exploration of how these features influence their trust in RAG-generated responses and their decision-making.
Participants will be assigned to one of three groups: the control group, which has no access to source verification, and the treatment groups, which has expanded access to source citations (one or multiple sources) for validation. While completing a set of 20 tasks, each group will be asked to assess their Trust on the RAG system and try to detect errors based on the given outputs of the RAG-system. At the end of the study, all participants will be required to provide basic demographic information. Additionally, you will be asked to enter your Prolific Worker ID for payment purposes, which will be deleted once the payment process is completed.
All data collected during the study will be kept strictly confidential and stored, processed, and evaluated in a manner that maintains anonymity. Only authorized personnel will have access to the data, and it will not be shared with external parties except research partners at the Karlsruhe Institute of Technology. Once payment is completed, your Prolific Worker ID, individual participation code, and declaration of consent will be deleted, preventing further identification. Anonymized research data will be retained for analysis and might be published in a report or journal article. The results of the study will be published exclusively in anonymized and/or aggregated form.
Participation in the study is voluntary, and you will not face any repercussions if you choose not to participate. Even after providing consent, you can withdraw at any time without consequences. If you request, your data will be deleted in full or in part, but this must occur before the deletion of your Prolific Worker ID from the research data, after which no link to individual participants is possible. 
6. Recipient 
In principle, your data will not be transmitted to third parties. 
If it is exceptionally necessary for external service providers to process data for us on behalf of us, these are carefully selected by us and contractually obliged. The respective service providers will work exclusively according to our instructions. We ensure this through strict contractual regulations, technical and organizational measures and additional controls. 
There is no transfer of data to third countries outside the EU or the EEA or to an international organization. Automated decision-making, including profiling, is not performed. 
7. Storage time 
The Prolific ID, the individual participation code as well as the declaration of consent will be deleted immediately after the completion of the payment. The anonymized research data will be kept for research and might be published in a report or journal article. 
8. Rights 
You have the following rights in relation to your data: 
•	the right to confirm whether data concerning you is processed and to obtain information about the data processed, to further information on data processing and to copies of the data (Art. 15 GDPR), 
•	the right to correct or complete inaccurate or incomplete data (Art. 16 GDPR), 
•	right to immediate deletion of the data concerning you (Art. 17 GDPR), 
•	right to restrict processing (Article 18 GDPR), 
•	right to receive the data concerning you and provided by you and to transfer this data to other controllers (Art. 20 GDPR). 
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
        switch_page("initialQuestions_RAG")
main()