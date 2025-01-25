import utils.base as base
import utils.note as note

import streamlit as st

rt_info = None

def rt_summary_source():
    global rt_info

    col11,col12 = st.columns([1, 1])
    with col11:
        # Get the list of doctors by department
        if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
            st.session_state.doctors_by_dept = note.get_doctors_by_dept()

        # Get the list of departments
        depts = st.session_state.doctors_by_dept["kwa"].unique()
        st.selectbox("진료과", options=depts, key="rt-dept", placeholder="진료과", label_visibility="collapsed")

    with col12:
        # Get the list of doctors for the selected department
        doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==st.session_state["rt-dept"]]["spth"]
        spth = st.selectbox("진료의", options=doctors, key="rt-doctor", placeholder="진료의", label_visibility="collapsed", on_change="rerun")
        
        # Get the list of patients for the selected doctor
        st.session_state.rt_patients = note.get_patient_by_doctor(spth)

    # Display the list of patients
    selected_row = st.dataframe(st.session_state.rt_patients, key="rt-selected-patient", on_select="rerun", selection_mode="single-row", height=140, use_container_width=True)

    if selected_row and len(selected_row.selection.rows)>0:
        idnoa = st.session_state.rt_patients["idnoa"][selected_row["selection"]["rows"][0]]
        lwdat = st.session_state.rt_patients["lwdat"][selected_row["selection"]["rows"][0]]

        rt_info = note.collect_rt_source(idnoa, lwdat)

    st.divider()

    if rt_info is not None:
        st.write("입원기록지")
        if "ae" in rt_info and len(rt_info["ae"]) > 0:
            st.json(rt_info["ae"], expanded=1)
        if "ay" in rt_info and len(rt_info["ay"]) > 0:
            st.json(rt_info["ay"], expanded=1)

        st.write("수술기록지")
        if "or" in rt_info and len(rt_info["or"]) > 0:
            st.json(rt_info["or"], expanded=1)    
        st.write("경과기록지")
        if "pn" in rt_info and len(rt_info["pn"]) > 0:
            st.json(rt_info["pn"], expanded=1)

        st.write("검사결과")
        if "je" in rt_info and len(rt_info["je"]) > 0:
            st.json(rt_info["je"], expanded=1)
        if "te" in rt_info and len(rt_info["te"]) > 0:
            st.json(rt_info["te"], expanded=1)
        if "ce" in rt_info and len(rt_info["ce"]) > 0:
            st.json(rt_info["ce"], expanded=1)
        if "yt" in rt_info and len(rt_info["yt"]) > 0:
            st.json(rt_info["yt"], expanded=1)

        st.write("퇴원요약")        
        if "rt" in rt_info and len(rt_info["rt"]) > 0:
            st.json(rt_info["rt"], expanded=1)

def rt_summary_target():
    st.text_area("Prompt", height=150, key="rt-prompt")

    st.header("퇴원요약지 (Discharge Summary)")
    if rt_info is None or "rt" not in rt_info or len(rt_info["rt"]) == 0:
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
        patient_rt_report = rt_info["rt"][0]

        st.write("주호소/입원사유")
        st.caption(patient_rt_report["ocm32chiefcomp"])
        st.write("주진단명 (Final Diagnosis)")
        st.caption(patient_rt_report["ocm32finaldx"])
        st.write("부진단명 (Secondary Diagnosis)")
        st.caption(patient_rt_report["ocm32scnddx"])

        st.write("수술명 (Treatment Op.)")
        st.caption(patient_rt_report["ocm32op"])
        st.write("처치명 (Treatment Medical)")
        st.caption(patient_rt_report["ocm32medical"])

        st.write("중요검사소견 (Abnormal Finding or Lab)")
        st.caption(patient_rt_report["ocm32problem"])
        st.write("추후관리계획 (Follow-up Plan)")
        st.caption(patient_rt_report["ocm32follow"])
        st.write("경과요약 (Progress Summary)")
        st.caption(patient_rt_report["ocm32other"])

        st.write("치료결과 (Result)")
        st.caption(patient_rt_report["ocm32rtrstcd"])
        st.write("퇴원형태 (Type of Discharge)")
        st.caption(patient_rt_report["ocm32rttypecd"])
        st.write("퇴원약 (Medicine)")

