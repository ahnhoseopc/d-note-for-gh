import utils.base as base
import utils.note as note
import datetime

import streamlit as st

tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])
df_ae = None
df_ay = None
df_or = None
df_pn = None
df_rt = None

with tab1:

    col1, colm, col2 = st.columns([5, 1, 5])
    
    with colm:
        if st.button("➡️", key="write-op"):
            result = note.call_api(st.session_state["op-prompt"], "op-draft")
            st.session_state["op-draft"] = result

    with col1:
        col11, col12, col13, col14 = st.columns([2, 2 , 1, 1])
        with col11:
            st.text_input("등록번호:", key="patient-id-or")
        with col12:
            st.date_input("내원일", datetime.date(2024, 7, 1), key="admsn-date-or")
        with col13:
            if st.button("조회"):
                df_ae = note.call_db_patient_record("query_AE_P", st.session_state["patient-id-or"], st.session_state["admsn-date-or"])
                df_or = note.call_db_patient_record("query_OR_P", st.session_state["patient-id-or"], st.session_state["admsn-date-or"])
                df_pn = note.call_db_patient_record("query_PN_P", st.session_state["patient-id-or"], st.session_state["admsn-date-or"])

                import utils.base as base
                decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
                df_pn = df_pn.map(decode_rtf)


        st.text_area("Prompt", height=150, key="op-prompt")

        st.write("입원기록지")
        if df_ae is not None:
            st.json(df_ae.to_json(orient="records"))
        st.write("수술기록지")
        if df_or is not None:
            st.json(df_or.to_json(orient="records"))
        st.write("경과기록지")
        if df_pn is not None:
            st.json(df_pn.to_json(orient="records"))
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
    col1, colm, col2 = st.columns([5, 1, 5])
    with colm:
        if st.button("⇨", key="write-rt"):
            result = note.call_api(st.session_state["op-prompt"], "op-draft")
            st.session_state["op-draft"] = result
    with col1:
        col11, col12, col13 = st.columns([1, 1, 1])
        with col11:
            st.text_input("등록번호:", "18273645", key="patient-id-rt")
        with col12:
            st.date_input("내원일", datetime.datetime.today(), key="admsn-date-rt")
        with col13:
            if st.button("조회", key="search-rt"):
                df_ae = note.call_db_patient_record("query_AE_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
                df_ay = note.call_db_patient_record("query_AY_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
                df_or = note.call_db_patient_record("query_OR_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
                df_pn = note.call_db_patient_record("query_PN_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
                df_rt = note.call_db_patient_record("query_RT_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])

                decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
                df_pn = df_pn.map(decode_rtf)

        st.text_area("Prompt", height=150, key="rt-prompt")
        st.write("입원기록지")
        if df_ae is not None and len(df_ae) > 0:
            st.json(df_ae.to_json(orient="records"))
        if df_ay is not None and len(df_ay) > 0:
            st.json(df_ay.to_json(orient="records"))

        st.write("수술기록지")
        if df_or is not None:
            st.json(df_or.to_json(orient="records"))    
        st.write("경과기록지")
        if df_pn is not None:
            st.json(df_pn.to_json(orient="records"))

        st.write("검사결과")
        if df_rt is not None:
            st.json(df_rt.to_json(orient="records"))

    with col2:
        if df_rt is None:
            st.write("환자정보")
            st.write("의료진정보")
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
        else:
            st.write("주호소/입원사유")
            st.caption(df_rt["OCM32CHIEFCOMP".lower()][0])
            st.write("주진단명 (Final Diagnosis)")
            st.caption(df_rt["OCM32FINALDX".lower()][0])
            st.write("부진단명 (Secondary Diagnosis)")
            st.caption(df_rt["OCM32SCNDDX".lower()][0])

            st.write("수술명 (Treatment Op.)")
            st.caption(df_rt["OCM32OP".lower()][0])
            st.write("처치명 (Treatment Medical)")
            st.caption(df_rt["OCM32MEDICAL".lower()][0])

            st.write("중요검사소견 (Abnormal Finding or Lab)")
            st.caption(df_rt["OCM32PROBLEM".lower()][0])
            st.write("추후관리계획 (Follow-up Plan)")
            st.caption(df_rt["OCM32FOLLOW".lower()][0])
            st.write("경과요약 (Progress Summary)")
            st.caption(df_rt["OCM32OTHER".lower()][0])

            st.write("치료결과 (Result)")
            st.caption(df_rt["OCM32RTRSTCD".lower()][0])
            st.write("퇴원형태 (Type of Discharge)")
            st.caption(df_rt["OCM32RTTYPECD".lower()][0])
            st.write("퇴원약 (Medicine)")

    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
