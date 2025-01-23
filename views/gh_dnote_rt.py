import utils.note as note

import streamlit as st

df_ae = None
df_ay = None
df_or = None
df_pn = None
df_rt = None

def on_select_patient():
    global df_ae, df_ay, df_or, df_pn, df_rt

    if "selected-patient-rt" in st.session_state:
        selected_row = st.session_state["selected-patient-rt"]
        if selected_row and "selection" in selected_row and "rows" in selected_row["selection"] and len(selected_row["selection"]["rows"]) > 0:

            idnoa = st.session_state.rt_patients["idnoa"][selected_row["selection"]["rows"][0]]
            lwdat = st.session_state.rt_patients["lwdat"][selected_row["selection"]["rows"][0]]

            df_ae, df_ay, df_or, df_pn, df_rt = note.collect_rt_info(st.session_state["prompt-rt"], idnoa, lwdat)
    pass

def on_change_doctor():
    pass

def rt_summary_source():
    global df_ae, df_ay, df_or, df_pn, df_rt

    col11,col12 = st.columns([1, 1])
    with col11:
        if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
            st.session_state.doctors_by_dept = note.get_doctors_by_dept()

        depts = st.session_state.doctors_by_dept["kwa"].unique()
        st.selectbox("진료과", options=depts, key="dept-rt", placeholder="진료과", label_visibility="collapsed")

    with col12:
        doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==st.session_state["dept-rt"]]["spth"]
        st.selectbox("진료의", options=doctors, key="doctor-rt", placeholder="진료의", label_visibility="collapsed", on_change=on_change_doctor)
        st.session_state.rt_patients = note.get_patient_by_doctor(st.session_state["doctor-rt"])

    st.dataframe(st.session_state.rt_patients, on_select=on_select_patient, selection_mode="single-row", height=140, use_container_width=True, key="selected-patient-rt")

    st.divider()

    st.text_area("Prompt", height=150, key="prompt-rt")
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
