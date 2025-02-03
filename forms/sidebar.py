import utils.auth as auth

import streamlit as st
import random

def display():
    st.markdown(
        """
        <style>
            .bottom-widget {
                position: fixed;
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                background-color: white;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                z-index: 100;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="bottom-widget">', unsafe_allow_html=True)

    with st.sidebar.container(height=200):

        cols = st.columns([1,1,1])
        with cols[0]: st.metric("Grade", value=random.randint(80,99))
        with cols[1]: st.metric("Index", value=random.randint(80,99))
        with cols[2]: st.metric("Count", value=random.randint(50,99))

        if auth.check_auth():
            st.caption(f"Welcome, *{st.session_state.user_id} 과장님*")

        if auth.check_auth():
            if st.button("Logout", use_container_width=True):
                auth.logout()
        else:
            if st.button("Login", use_container_width=True):
                st.rerun()

    with st.sidebar.container():
        cols = st.columns([3,1])
        with cols[0]: st.text("Provided by ")
        with cols[1]: st.image("assets/dk_logo.png", width=40)

    st.markdown('</div>', unsafe_allow_html=True)
