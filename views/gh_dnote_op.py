import utils.base as base
import utils.note as note
import json

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
        kwa = st.selectbox("진료과", options=depts, key="op-dept", placeholder="진료과", label_visibility="collapsed")

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

        or_info = note.collect_or_source(idnoa, lwdat, kwa, spth)

    st.divider()

    if or_info is not None:
        st.write("입원기록지")
        if len(or_info["ae"]):
            st.json(or_info["ae"], expanded=1)
        if len(or_info["ay"]):
            st.json(or_info["ay"], expanded=1)
        st.write("프로토콜")
        if len(or_info["pt"]):
            st.json(or_info["pt"], expanded=1)

def op_record_target():
    with st.expander("수술기록지 소스", expanded=False):
        if or_info:
            st.json(or_info["or-source"], expanded=1)

    or_prompt = """
입력된 데이터의 "present illness" 와 "plan"을 확인하여 "operation name"을 추정하라.
추정된 "operation name"을 참조하여 "protocols of doctor"의 "code" 또는 "code name"과 매치가되는 것을 찾아서 해당하는 protocol을 표시하라.

                """
    st.text_area("Prompt", value=or_prompt, height=150, key="or-prompt")

    if st.button("➡️", key="or-write"):

        response_container = st.empty()
        st.session_state["or-result"] = ""
        try:
            responses = note.call_api(st.session_state["or-prompt"], json.dumps(or_info["or-source"], indent=4))
            if responses is not None:
                for response in responses:
                    if response is not None and "text" in response:
                        st.session_state["or-result"] += response.text
                        response_container.caption(st.session_state["or-result"])
        except Exception as e:
            response_container.caption(f"error when calling api: {e}")

    col1,col2 = st.columns(2)
    with col1:
        with st.expander("수술기록지 기존", expanded=False):
            if or_info is not None:
                st.write("수술기록지 record")
                if "or" in or_info and len(or_info["or"]):
                    st.json(or_info["or"], expanded=1)
                st.write("수술기록지 aligned")
                if len(or_info["or-current"]):
                    st.json(or_info["or-current"], expanded=1)
    with col2:
        with st.expander("수술기록지 신규", expanded=False):
            if "or-result" in st.session_state:
                # result = json.loads(st.session_state["or-result"])
                result = st.session_state["or-result"]
                st.json(result)

    st.header("수술기록지 (Operation Record)")
    if or_info is not None and len(or_info["or"]) > 0:
        patient_op_report = or_info["or"][0]
        st.subheader("환자정보")
        st.write("등록번호")
        st.caption(patient_op_report["ocm06idnoa"])

        st.subheader("의료진정보")
        cols = st.columns(3)
        with cols[0]:
            st.write("Surgeon")
            st.caption(base.ifnull(patient_op_report["ocm06kwa"], "<na>") + " / "
                        + base.ifnull(patient_op_report["ocm06spth"], "<na>") + " / "
                        + str(base.ifnull(patient_op_report["ocm06rgcd"], 0)))
        with cols[1]:
            st.write("PA")
            st.write("Nurse")
        with cols[2]:
            st.write("Anesthesiologist")
            st.write("Method of Anesthesia")

        st.subheader("진단정보")
        patient_op_cmta = patient_op_report["ocm06cmta"]
        patient_op_cmta_comp = patient_op_cmta.split("|")
        st.caption(patient_op_report["ocm06cmta"])

        st.write("Preoperative Diagnosis")
        st.caption(patient_op_cmta_comp[7])
        st.write("Postoperative Diagnosis")
        st.caption(patient_op_cmta_comp[11])

        st.subheader("수술정보")
        st.write("Name of Operation")
        st.caption(patient_op_cmta_comp[8])

        st.write("Procedures & Findings")
        st.caption(patient_op_report["ocm06cmtb"])
        st.write("수술 중 특이사항")
        memo = patient_op_report["ocm06memo"]
        st.caption(memo)
        if memo is None or memo[0] == 'N':
            memo = "무"
        else:
            memo = "유 : " + memo[2:]
        st.caption(memo)

        st.subheader("수술정보")
        cols = st.columns(4)
        with cols[0]:
            st.write("출혈정도")
            st.caption("alarm: " + base.ifnull(patient_op_report["ocm06alarm"],"<na>"))
        with cols[1]:
            st.write("패드확인 (유/무)")
            st.caption("cmplyn: " + base.ifnull(patient_op_report["cmplyn"],"<na>"))
            st.caption("emdv: " + base.ifnull(patient_op_report["ocm06emdv"],"<na>"))
        with cols[2]:
            st.write("Tissue of Path. (Y/N)")
            st.caption("tissueexmn: " + base.ifnull(patient_op_report["ocm06tissueexmn"],"<na>"))
            st.caption("tissueexmncnts: " + base.ifnull(patient_op_report["ocm06tissueexmncnts"],"<na>"))
        with cols[3]:
            st.write("Drains (Y/N)")
            st.caption("drngpipe: " + base.ifnull(patient_op_report["ocm06drngpipe"],"<na>"))
            st.caption("drngpipecnts: " + base.ifnull(patient_op_report["ocm06drngpipecnts"],"<na>"))
        
        cols = st.columns(2)
        with cols[0]:
            st.write("수술일시")
            st.caption(base.ifnull(patient_op_report["ocm06opdat"], "<na>") + " 시작:" 
                    + base.ifnull(patient_op_report["ocm06opstarttm"], "<na>") + " ~ 종료:"
                    + base.ifnull(patient_op_report["ocm06opendtm"], "<na>"))
        with cols[1]:
            st.write("작성일시")
            st.caption(patient_op_report["ocm06sysdat"] + " " + patient_op_report["ocm06systm"])
        
        st.write("치료계획")
        st.caption(patient_op_report["ocm06mdtrplan"])
        st.write("수술경과")
        st.caption(patient_op_report["ocm06opprgr"])
        st.write("PLCR")
        st.caption(patient_op_report["ocm06pclr"])
