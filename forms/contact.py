import re
import streamlit as st
import requests

WEBHOOK_URL = st.secrets["WEBHOOK_URL"]


def is_valid_email(email):
    # basic regex
    email_pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None

def contact_form():
    with st.form("contact_form"):
        name = st.text_input("First Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not WEBHOOK_URL:
                st.error("Email service is not setup. Please try again later.", icon="🚨")
                st.stop()

            if not email:
                st.error("Please provide your email address.", icon="📨")
                st.stop()

            if not is_valid_email(email):
                st.error("Please enter a valid email address.", icon="📧")
                st.stop()

            if not message:
                st.error("Please provide a message.", icon="📃")
                st.stop()

            data = {
                "name": name,
                "email": email,
                "message": message
            }

            response = requests.post(WEBHOOK_URL, json={data})
            if response.status_code == 200:
                st.success("Yout message has been sent successfully!", icon="🚀")
            else:
                st.error("Something went wrong. Please try again later.", icon="🚨")
            