import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *



def main():
    st.header('Consent to Participate')
    st.write('I am aware that consent is voluntary and can be refused without disadvantages or revoked at any time without giving reasons. I know that in the event of a revocation, the lawfulness of the processing carried out on the basis of the consent until the revocation is not affected. I understand that in order to revoke, I can simply contact the contact persons mentioned in the information.')
    st.markdown("**By clicking on the button I consent to participate in this study.**")
    if st.button('I consent'):
        switch_page("initialQuestions")


main()