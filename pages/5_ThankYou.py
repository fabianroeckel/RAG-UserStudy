import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def main():
    st.title("Thank You for Participating!")

    st.write(
        """
        ## Your Contribution is Appreciated

        Thank you for taking the time to participate in our study. Your input is valuable 
        and will help us in our research. If you have any questions or feedback, please 
        don't hesitate to reach out to us.

        We sincerely appreciate your contribution!
        """
    )

    # You can add any additional content or contact information here

if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        print('I got a KeyError - reason "%s"' % str(e))
        switch_page("streamlit_app")
