import forms.login as login

from functools import wraps
import streamlit as st

def authenticate(user_id, password):
    # authenticate user
    st.session_state.logged_in = True
    st.session_state.user_id = user_id
    return True

def check_auth():
    """인증 상태 확인"""
    return st.session_state.get('logged_in', False)

def login_required(func):
    """로그인 필요한 페이지에 대한 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_auth():
            login.login_form(authenticate)
            return
        return func(*args, **kwargs)
    return wrapper

def logout():
    """로그아웃 처리"""
    if st.session_state.get('logged_in'):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()