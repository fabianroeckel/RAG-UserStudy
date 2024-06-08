import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from loguru import logger

def main():
    st.title("Thank You for Participating!")
    st.write(
        """
        ## Your Contribution is Appreciated

        Thank you for taking the time to participate in our study. You can use the link below to get back to Proflic:
        """
    )
    st.markdown("https://app.prolific.com/submissions/complete?cc=CFUMHU8L")




    # You can add any additional content or contact information here

if __name__ == "__main__":
    try:
        main()
    except (KeyError, AttributeError) as e:
        print('I got a KeyError - reason "%s"' % str(e))
        switch_page("streamlit_app")
