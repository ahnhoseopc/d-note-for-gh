import utils.note as note

import streamlit as st

df_ae = None
df_ay = None
df_or = None
df_pn = None
df_rt = None

def on_select_patient():
    global df_ae, df_ay, df_or, df_pn, df_rt

    if "selected-patient-op" in st.session_state:
        selected_row = st.session_state["selected-patient-op"]
        if selected_row and "selection" in selected_row and "rows" in selected_row["selection"] and len(selected_row["selection"]["rows"]) > 0:
            idnoa = st.session_state.op_patients["idnoa"][selected_row["selection"]["rows"][0]]
            lwdat = st.session_state.op_patients["lwdat"][selected_row["selection"]["rows"][0]]

            df_ae, df_ay, df_or, df_pn, df_rt = note.collect_rt_info(st.session_state["prompt-op"], idnoa, lwdat)
    pass

def op_record_source():
    global df_ae, df_ay, df_or, df_pn, df_rt
    
    col11,col12 = st.columns([1, 1])
    with col11:
        if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
            st.session_state.doctors_by_dept = note.get_doctors_by_dept()

        depts = st.session_state.doctors_by_dept["kwa"].unique()
        st.selectbox("진료과", options=depts, key="dept-op", placeholder="진료과", label_visibility="collapsed")

    with col12:
        doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==st.session_state["dept-op"]]["spth"]
        spth = st.selectbox("진료의", options=doctors, key="doctor-op", placeholder="진료의", label_visibility="collapsed")
        st.session_state.op_patients = note.get_patient_by_doctor(spth)

    st.dataframe(st.session_state.op_patients, on_select=on_select_patient, selection_mode="single-row", height=140, use_container_width=True, key="selected-patient-op")

    st.divider()

    st.text_area("Prompt", height=150, key="prompt-op")

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

def op_record_target():
    global df_ae, df_ay, df_or, df_pn, df_rt

    st.header("수술기록지 (Operation Record)")
    if df_rt is None or len(df_rt) == 0:
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
