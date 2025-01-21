import utils.note as note
import datetime

import streamlit as st

tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])

with tab1:

    col1, col2 = st.columns([1, 1])
    with col1:
        col11, col12, col13 = st.columns([2, 1, 2])
        with col11:
            st.text_input("등록번호:", key="patient-id-or")
        with col12:
            if st.button("조회"):
                df = note.call_db("query_AE_P", st.session_state["patient-id-or"])
        with col13:
            if st.button("작성"):
                result = note.call_api(st.session_state["op-prompt"], "op-draft")
                st.session_state["op-draft"] = result

        st.text_area("Prompt", height=250, key="op-prompt")
        st.write("입원기록지")
        st.write("수술기록지")
        st.write("경과기록지")
        st.write("검사결과")

    with col2:
        st.header("수술기록지 (Operation Record)")
        st.subheader("환자정보")
        st.subheader("의료진정보")
        st.write("Surgeon")
        st.write("PA")
        st.write("Nurse")
        st.write("Anesthesiologist")
        st.write("Method of Anesthesia")
        st.subheader("진단정보")
        st.write("Preoperative Diagnosis")
        st.write("Postoperative Diagnosis")
        st.subheader("수술술정보")
        st.write("Name of Operation")
        st.write("Procedures & Findings")
        st.write("수술 중 특이사항")
        st.write("수술일시")
        st.write("출혈정도")
        st.write("패드확인 (유/무)")
        st.write("Tissue of Pathology (Y/N)")
        st.write("Drains (Y/N)")
        st.write("작성일시")

    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("퇴원요약지 (Discharge Summary)")
    col1, col2 = st.columns([1, 1])

    with col1:
        col11, col12, col13, col14 = st.columns([1, 1, 1, 2])
        with col11:
            st.text_input("등록번호:", key="patient-id-rt")
        with col12:
            st.date_input("내원일일", datetime.date(2024, 7, 1), key="admsn-date")
        with col13:
            if st.button("조회"):
                df_ae = note.call_db("query_AE_P", st.session_state["patient-id-rt"])
                df_or = note.call_db("query_OR_P", st.session_state["patient-id-rt"])
                df_pn = note.call_db("query_PN_P", st.session_state["patient-id-rt"])
        with col14:
            if st.button("작성"):
                result = note.call_api(st.session_state["op-prompt"], "op-draft")
                st.session_state["op-draft"] = result

        st.text_area("Prompt", height=250, key="rt-prompt")
        st.write("환자번호")
        st.write("환자명")
        st.write("성별")
        st.write("나이")

    with col2:
        st.write("환자정보")
        st.write("주호소/입원사유")
        st.write("주진단명 (Final Diagnosis)")
        st.write("부진단명 (Secondary Diagnosis)")
        st.write("수술명 (Treatment Op.)")
        st.write("처치명 (Treatment Medical)")
        st.write("중요검사소견 (Abnormal Finding or Lab)")
        st.write("추후관리계획 (Follow-up Plan)")
        st.write("경과요약 (Progress Summary)")
        st.write("치료결과 (Result)")
        st.write("퇴원형태 (Type of Discharge)")
        st.write("퇴원약 (Medicine)")
        

    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
