import utils.base as base
import utils.note as note
import json

import streamlit as st

or_info = None

def op_record_source():
    global or_info
    
    # Get the list of doctors by department
    if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
        st.session_state.doctors_by_dept = note.get_doctors_by_dept()

    col11,col12 = st.columns([1, 1])
    with col11:
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

    # Collect the operation record source from source data
    if selected_row and len(selected_row.selection.rows)>0:
        idnoa = st.session_state.op_patients["idnoa"][selected_row["selection"]["rows"][0]]
        lwdat = st.session_state.op_patients["lwdat"][selected_row["selection"]["rows"][0]]

        or_info = note.collect_or_source(idnoa, lwdat, kwa, spth)

    st.divider()

    with st.expander("수술기록지 소스 (선정항목)", expanded=True):
        if or_info:
            st.json(or_info["or-source"], expanded=1)

    with st.expander("수술기록지 소스 (DB)", expanded=False):
        # Source data display
        if or_info is not None:
            st.write("입원기록지")
            if len(or_info["ae"]):
                st.json(or_info["ae"], expanded=1)
            if len(or_info["ay"]):
                st.json(or_info["ay"], expanded=1)
            st.write("프로토콜")
            if len(or_info["pt"]):
                st.json(or_info["pt"], expanded=1)

    with st.expander("수술기록지 기존", expanded=False):
        if or_info is not None:
            st.write("수술기록지 DB")
            if "or" in or_info and len(or_info["or"]):
                st.json(or_info["or"], expanded=1)
            st.write("수술기록지 표시항목")
            if len(or_info["or-current"]):
                st.json(or_info["or-current"], expanded=1)

    return "op-record-source"

OR_PROMPT_DEFAULT = """입력된 데이터의 "present illness" 와 "plan"을 확인하여 "operation name"을 추정하라.
추정된 "operation name"을 참조하여 "protocols of doctor"의 "code" 또는 "code name"과 대응하는 것을 찾아서 해당하는 "protocol"을 찾아라.
응답으로 "present illness" 와 "plan", "operation name"과 "code", "code name", "protocol"을 json format으로 제시하라.
"""

def op_record_target():
    # 수술기록지 생성 프롬프트
    st.text_area("Prompt", value=OR_PROMPT_DEFAULT, height=150, key="or-prompt")

    # 수술기록지 작성 버튼
    cols = st.columns([3, 4])
    with cols[0]:
        or_write = st.button("➡️ 수술기록지 초안 작성", key="or-write")

    with cols[1]:
        st.radio("AI 모델 선택", ["MedLM", "Gemini-Pro", "Gemini-Flash"], key="ai-model-or", index=2, horizontal=True, label_visibility="collapsed")

    if or_write:
        with st.expander("AI지원 프로토콜 선택", expanded=True):
            response_container = st.empty()
            st.session_state["or-result"] = ""
            try:
                responses = note.call_api(st.session_state["or-prompt"], json.dumps(or_info["or-source"], indent=4), st.session_state["ai-model-or"].lower())
                for response in responses:
                    st.session_state["or-result"] += response.text
                    response_container.caption(st.session_state["or-result"])

                if base.is_json_format(st.session_state["or-result"]):
                    response_container.caption(json.loads(st.session_state["or-result"]))

            except Exception as e:
                response_container.caption(f"error when calling api: {e}")

    # 수술기록지 결과 비교: 기존 vs 신규
    with st.expander("수술기록지 신규", expanded=False):
        if "or-result" in st.session_state:
            result = st.session_state["or-result"]
            st.caption(result)

    # 수술기록지 결과 포맷
    with st.expander("수술기록지 양식", expanded=False):
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
