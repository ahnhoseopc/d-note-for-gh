import views.gh_dnote_op as op
import views.gh_dnote_rt as rt

import utils.base as base
import utils.note as note

import streamlit as st

tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])

with tab1:

    col1, colm, col2 = st.columns([5, 1, 5])
    
    with colm:
        if st.button("➡️", key="write-op"):
            op_data = st.session_state["admsn-date-or"]
            result = note.call_api(st.session_state["op-prompt"], op_data)
            st.session_state["op-draft"] = result

    with col1:
        op.op_record_source()        

    with col2:
        op.op_record_target()

    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("퇴원요약지 (Discharge Summary)")
    col1, colm, col2 = st.columns([5, 1, 5])
    with colm:
        if st.button("⇨", key="write-rt"):
            result = note.call_api(st.session_state["op-prompt"], "op-draft")
            st.session_state["op-draft"] = result
    with col1:
        rt.rt_summary_source()

    with col2:
        rt.rt_summary_target()

    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
