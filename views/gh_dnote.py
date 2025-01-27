import views.gh_dnote_op as op
import views.gh_dnote_rt as rt

import streamlit as st

tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])

with tab1:

    col1, col2 = st.columns([5, 5])
    
    with col1:
        op.op_record_source()        

    with col2:
        op.op_record_target()

    st.image("https://www.moonhwa.or.kr/moonhwa/board/image.do?mId=68&id=gLIPvyTqKyW+zoW9e3tGypgPir8mJPqFvO0/L3mUun8=", use_container_width=True)

with tab2:
    col1, col2 = st.columns([5, 5])

    with col1:
        rt.rt_summary_source()

    with col2:
        rt.rt_summary_target()

    st.image("https://www.moonhwa.or.kr/moonhwa/board/image.do?mId=68&id=Bs40RWz9R+Hh8//twWklygJ3bggWUiqg5oAQxj4QmgY=", use_container_width=True)

st.image("https://www.moonhwa.or.kr/moonhwa/images/main02/img_symbol0302.png", use_container_width=True)
