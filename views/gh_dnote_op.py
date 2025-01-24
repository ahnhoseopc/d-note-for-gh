import utils.note as note

import streamlit as st

or_info = None

def op_record_source():
    global or_info
    
    col11,col12 = st.columns([1, 1])
    with col11:
        # Get the list of doctors by department
        if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
            st.session_state.doctors_by_dept = note.get_doctors_by_dept()

        # Get the list of departments
        depts = st.session_state.doctors_by_dept["kwa"].unique()
        st.selectbox("진료과", options=depts, key="op-dept", placeholder="진료과", label_visibility="collapsed")

    with col12:
        # Get the list of doctors for the selected department
        doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==st.session_state["op-dept"]]["spth"]
        spth = st.selectbox("진료의", options=doctors, key="op-doctor", placeholder="진료의", label_visibility="collapsed")

        # Get the list of patients for the selected doctor
        st.session_state.op_patients = note.get_patient_by_doctor(spth)

    # Display the list of patients
    selected_row = st.dataframe(st.session_state.op_patients, on_select="rerun", selection_mode="single-row", height=140, use_container_width=True, key="selected-patient-op")

    if selected_row and len(selected_row.selection.rows)>0:
        idnoa = st.session_state.op_patients["idnoa"][selected_row["selection"]["rows"][0]]
        lwdat = st.session_state.op_patients["lwdat"][selected_row["selection"]["rows"][0]]

        or_info = note.collect_or_source(idnoa, lwdat)

    st.divider()

    if or_info is not None:
        st.write("입원기록지")
        if len(or_info["ae"]):
            st.json(or_info["ae"])
        st.write("수술기록지")
        if len(or_info["or"]):
            st.json(or_info["or"])
        st.write("경과기록지")
        if len(or_info["pn"]):
            st.json(or_info["pn"])
        st.write("검사결과")

def op_record_target():
    st.text_area("Prompt", height=150, key="or-prompt")

    st.header("수술기록지 (Operation Record)")
    if or_info is None or len(or_info["or"]) == 0:
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
        st.caption(or_info["or"]["ocm32chiefcomp"][0])
        st.write("주진단명 (Final Diagnosis)")
        st.caption(or_info["or"]["ocm32finaldx"][0])
        st.write("부진단명 (Secondary Diagnosis)")
        st.caption(or_info["or"]["ocm32scnddx"][0])

        st.write("수술명 (Treatment Op.)")
        st.caption(or_info["or"]["ocm32op"][0])
        st.write("처치명 (Treatment Medical)")
        st.caption(or_info["or"]["ocm32medical"][0])

        st.write("중요검사소견 (Abnormal Finding or Lab)")
        st.caption(or_info["or"]["ocm32problem"][0])
        st.write("추후관리계획 (Follow-up Plan)")
        st.caption(or_info["or"]["ocm32follow"][0])
        st.write("경과요약 (Progress Summary)")
        st.caption(or_info["or"]["ocm32other"][0])

        st.write("치료결과 (Result)")
        st.caption(or_info["or"]["ocm32rtrstcd"][0])
        st.write("퇴원형태 (Type of Discharge)")
        st.caption(or_info["or"]["ocm32rttypecd"][0])
        st.write("퇴원약 (Medicine)")

