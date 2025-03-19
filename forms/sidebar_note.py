import utils.note as note

import streamlit as st

def display():
    global mr_info

    with st.sidebar.container(height=320):
        # Get the list of doctors by department
        if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
            st.session_state.doctors_by_dept = note.get_doctors_by_dept()

        st.caption("진료과/진료의")
        col11,col12 = st.columns([1, 1])
        with col11:
            # Get the list of departments
            depts = st.session_state.doctors_by_dept["kwa"].unique()
            dept = st.selectbox("진료과", options=depts, key="dept", placeholder="진료과", label_visibility="collapsed")

        with col12:
            # Get the list of doctors for the selected department
            doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==dept]["spth"]
            doctor = st.selectbox("진료의", options=doctors, key="doctor", placeholder="진료의", label_visibility="collapsed")

            # Get the list of patients for the selected doctor
            st.session_state.patients = note.get_patient_by_doctor(doctor)

        # Display the list of patients
        st.caption("담당환자")
        selected_row = st.dataframe(st.session_state.patients, key="df_patient", on_select="rerun", selection_mode="single-row", height=140, use_container_width=True, hide_index=True, )

        # Collect the operation record source from source data
        if selected_row and len(selected_row.selection.rows)>0:
            patient_id = st.session_state.patients["patient_id"][selected_row["selection"]["rows"][0]]
            adm_date = st.session_state.patients["adm_date"][selected_row["selection"]["rows"][0]]

            if not (st.session_state.get("patients_id") == patient_id and st.session_state.get("adm_date") == adm_date):
                st.session_state.patients_id = patient_id
                st.session_state.adm_date = adm_date

                st.session_state.mr_info = note.get_patient_mr_data(patient_id, adm_date, dept, doctor)
                st.session_state.mr_json = note.get_patient_mr_json(st.session_state.mr_info)

                # reset ai result
                st.session_state.cd_json = None
                st.session_state.cd_list = []
    pass
