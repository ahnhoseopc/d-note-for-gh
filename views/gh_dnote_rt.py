import utils.base as base
import utils.note as note
import datetime

import streamlit as st

df_ae = None
df_ay = None
df_or = None
df_pn = None
df_rt = None

def on_select():
    if "selected-patient-rt" in st.session_state:
        selected_row = st.session_state["selected-patient-rt"]
        if selected_row and "selection" in selected_row and "rows" in selected_row["selection"] and len(selected_row["selection"]["rows"]) > 0:

            idnoa = st.session_state.op_patients["환자번호"][selected_row["selection"]["rows"][0]]
            lwdat = st.session_state.op_patients["내원일"][selected_row["selection"]["rows"][0]]

            note.collect_rt_info(st.session_state["op-prompt"], idnoa, lwdat)
    pass

def rt_summary_source():
    global df_ae, df_ay, df_or, df_pn, df_rt

    df_doctors = note.run_sql("SELECT * FROM doctors")
    
    col11,col12 = st.columns([1, 1])
    with col11:
        dept = st.selectbox("진료과", options=["GY","EN"], key="dept-rt", placeholder="진료과", label_visibility="collapsed")
    with col12:
        doctors_by_dept = {"GY":["001324","020341"], "EN":["120321","100321"]}
        if dept:
            dockers = doctors_by_dept[dept]
        else:
            dockers = []
        st.selectbox("진료의", options=dockers, key="doctors-rt", placeholder="진료의", label_visibility="collapsed")

    st.session_state.op_patients = {"환자번호":["123456", "234567", "345678"], "내원일":["20241001", "20241002", "20241003"]}

    st.dataframe(st.session_state.op_patients, on_select=on_select, selection_mode="single-row", height=140, use_container_width=True, key="selected-patient-rt")

    st.divider()

    # col11, col12, col13 = st.columns([2, 2, 1])
    # with col11:
    #     st.text_input("등록번호:", "18273645", key="patient-id-rt")
    # with col12:
    #     st.date_input("내원일", datetime.datetime.today(), key="admsn-date-rt")
    # with col13:
    #     if st.button("조회", key="search-rt"):
    #         df_ae = note.call_db_patient_record("query_AE_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
    #         df_ay = note.call_db_patient_record("query_AY_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
    #         df_or = note.call_db_patient_record("query_OR_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
    #         df_pn = note.call_db_patient_record("query_PN_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])
    #         df_rt = note.call_db_patient_record("query_RT_P", st.session_state["patient-id-rt"], st.session_state["admsn-date-rt"])

    #         decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    #         df_pn = df_pn.map(decode_rtf)

    # st.divider()

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

def rt_summary_target():
    global df_ae, df_ay, df_or, df_pn, df_rt

    st.header("퇴원요약지 (Discharge Summary)")
    if df_rt is None or len(df_rt) == 0:
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
