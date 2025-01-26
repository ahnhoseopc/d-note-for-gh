import views.gh_dnote_op as op
import views.gh_dnote_rt as rt
import utils.note as note
import json

import streamlit as st

tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])

with tab1:

    col1, col2 = st.columns([5, 5])
    
    with col1:
        op.op_record_source()        

    with col2:
        op.op_record_target()

    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    col1, col2 = st.columns([5, 5])

    with col1:
        rt.rt_summary_source()

    with col2:
        rt.rt_summary_target()

    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

if "or-result" in st.session_state:
    st.write("경과요약1")
    st.caption(st.session_state["or-result"])
    # for response in st.session_state["or-result"]:
    #     st.caption(response.text)

if "rt-result" in st.session_state:
    st.write("경과요약2")
    st.caption(st.session_state["rt-result"])
    # for response in st.session_state["rt-result"]:
    #     st.caption(response.text)
