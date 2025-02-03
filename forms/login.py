import re
import streamlit as st

def is_valid_id(user_id):
    # basic regex
    user_id_pattern = r"^[a-zA-Z0-9._]+$"
    matched = re.match(user_id_pattern, user_id) is not None

    return matched

@st.dialog("Login to DMA!")
def login_form(authenticate):
    with st.form("login_form"):
        user_id = st.text_input("Login Id", key="id", placeholder="구글 ID를 사용하세요.")
        password = st.text_input("Password", key="pw", type="password", placeholder="비밀번호는 비워두세요.")
        submitted = st.form_submit_button("로그인")

        if submitted:
            if is_valid_id(user_id):
                if authenticate(user_id, password):
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.rerun()
                else:
                    st.switch_page("views/gh_about.py")                
            else:
                st.error("Please enter a valid id. Refresh this page. (F5)", icon="📧")
                st.stop()
