import utils.note as note

import streamlit as st

rt_info = None

def rt_summary_source():
    col11,col12 = st.columns([1, 1])
    with col11:
        if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
            st.session_state.doctors_by_dept = note.get_doctors_by_dept()

        depts = st.session_state.doctors_by_dept["kwa"].unique()
        st.selectbox("진료과", options=depts, key="rt-dept", placeholder="진료과", label_visibility="collapsed")

    with col12:
        doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==st.session_state["rt-dept"]]["spth"]
        st.selectbox("진료의", options=doctors, key="rt-doctor", placeholder="진료의", label_visibility="collapsed", on_change="rerun")
        st.session_state.rt_patients = note.get_patient_by_doctor(st.session_state["rt-doctor"])

    selected_row = st.dataframe(st.session_state.rt_patients, key="rt-selected-patient", on_select="rerun", selection_mode="single-row", height=140, use_container_width=True)

    global rt_info

    if selected_row and len(selected_row["selection"]["rows"]) > 0:
        idnoa = st.session_state.rt_patients["idnoa"][selected_row["selection"]["rows"][0]]
        lwdat = st.session_state.rt_patients["lwdat"][selected_row["selection"]["rows"][0]]

        rt_info = note.collect_rt_source(idnoa, lwdat)

    st.divider()

    if rt_info is not None:
        st.write("입원기록지")
        if len(rt_info["ae"]) > 0:
            st.json(rt_info["ae"])
        if len(rt_info["ay"]) > 0:
            st.json(rt_info["ay"])

        st.write("수술기록지")
        if len(rt_info["or"]) > 0:
            st.json(rt_info["or"])    
        st.write("경과기록지")
        if len(rt_info["pn"]) > 0:
            st.json(rt_info["pn"])

        st.write("검사결과")
        if len(rt_info["rt"]) > 0:
            st.json(rt_info["rt"])

def rt_summary_target():
    st.text_area("Prompt", height=150, key="rt-prompt")

    st.header("퇴원요약지 (Discharge Summary)")
    if rt_info is None or len(rt_info["rt"]) == 0:
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
        st.caption(rt_info["rt"]["ocm32chiefcomp"][0])
        st.write("주진단명 (Final Diagnosis)")
        st.caption(rt_info["rt"]["ocm32finaldx"][0])
        st.write("부진단명 (Secondary Diagnosis)")
        st.caption(rt_info["rt"]["ocm32scnddx"][0])

        st.write("수술명 (Treatment Op.)")
        st.caption(rt_info["rt"]["ocm32op"][0])
        st.write("처치명 (Treatment Medical)")
        st.caption(rt_info["rt"]["ocm32medical"][0])

        st.write("중요검사소견 (Abnormal Finding or Lab)")
        st.caption(rt_info["rt"]["ocm32problem"][0])
        st.write("추후관리계획 (Follow-up Plan)")
        st.caption(rt_info["rt"]["ocm32follow"][0])
        st.write("경과요약 (Progress Summary)")
        st.caption(rt_info["rt"]["ocm32other"][0])

        st.write("치료결과 (Result)")
        st.caption(rt_info["rt"]["ocm32rtrstcd"][0])
        st.write("퇴원형태 (Type of Discharge)")
        st.caption(rt_info["rt"]["ocm32rttypecd"][0])
        st.write("퇴원약 (Medicine)")

