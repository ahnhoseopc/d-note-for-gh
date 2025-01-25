import views.gh_dnote_op as op
import views.gh_dnote_rt as rt
import utils.note as note
import json

import streamlit as st

tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])

with tab1:

    col1, colm, col2 = st.columns([5, 1, 5])
    
    with colm:
        if st.button("➡️", key="or-write"):
            st.session_state["or-result"] = ""
            responses = note.call_api(st.session_state["or-prompt"], json.dumps(op.or_info, indent=4))
            if responses is not None:
                response_container = st.empty()
                for response in responses:
                    if response is not None:
                        response_container.markdown(response.text)
                        # st.session_state["or-result"] += response.text

    with col1:
        op.op_record_source()        

    with col2:
        op.op_record_target()

    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    col1, colm, col2 = st.columns([5, 1, 5])
    with colm:
        if st.button("⇨", key="rt-write"):
            st.session_state["rt-result"] = ""
            responses = note.call_api(st.session_state["rt-prompt"], json.dumps(rt.rt_info))
            if responses is not None:
                for response in responses:
                    if response is not None:
                        st.caption(response)
                        # st.session_state["or-result"] += response.text
               # st.session_state["rt-result"] += response.text
            
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
