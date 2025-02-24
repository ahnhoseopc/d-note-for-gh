import streamlit as st

def llm_settings_form(prompt):
    with st.form("contact_form"):
        new_prompt = st.text_area("Prompt", value=prompt)
        submitted = st.form_submit_button("Submit")

        if submitted:
            return new_prompt
