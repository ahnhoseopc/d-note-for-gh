import datetime
import re
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

    with st.expander("소스 의료정보 (API입력데이터)", expanded=True):
        if or_info:
            st.json(or_info["or-source"], expanded=1)

    with st.expander("소스 의료정보 (DB원본)", expanded=False):
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

    with st.expander("기존 수술기록지 (DB)", expanded=False):
        if or_info is not None:
            st.write("수술기록지 (DB)")
            if "or" in or_info and len(or_info["or"]):
                st.json(or_info["or"], expanded=1)
            # st.write("수술기록지 표시항목")
            # if len(or_info["or-current"]):
            #     st.json(or_info["or-current"], expanded=1)

    with st.expander("기존 수술기록지 (문서양식))", expanded=False):
        display_report(or_info["or-current"] if or_info and "or-current" in or_info else None)

    return "op-record-source"

OR_PROMPT_DEFAULT = """1. 입력된 데이터의 "present illness" , "impression"과 "plan"을 확인하여 "operation name"을 추정하라.
2. 추정된 "operation name"을 참조하여 "protocols of doctor"의 "code" 또는 "code name"과 대응하는 것을 찾아서 해당하는 "protocol"을 찾아라.
3. 응답으로 "present illness" 와 "impression" 그리고 "plan", "operation name"과 "code", "code name", "protocol"을 json format으로 제시하라.
"""

def op_record_target():
    # 수술기록지 생성 프롬프트
    st.text_area("Prompt", value=OR_PROMPT_DEFAULT, height=150, key="or-prompt")

    # 수술기록지 작성 버튼
    cols = st.columns([3, 4])
    with cols[0]:
        or_write = st.button("➡️ 수술기록지 Protocol AI 검색", key="or-write")

    with cols[1]:
        st.radio("AI 모델 선택", ["MedLM", "Gemini-Pro", "Gemini-Flash"], key="ai-model-or", index=2, horizontal=True, label_visibility="collapsed")

    operation_name, operation_protocol = "", ""
    
    if or_write:
        with st.expander("AI지원 프로토콜 선택", expanded=True):
            st.session_state["or-result"] = ""
            response_text = ""
            response_container = st.empty()
            try:
                responses = note.call_api(st.session_state["or-prompt"], json.dumps(or_info["or-source"], indent=4), st.session_state["ai-model-or"].lower())
                for response in responses:
                    response_text += response.text
                    response_container.caption(response_text)

                st.session_state["or-result"] = response_text

                response_text = re.sub(r"```json\s*|\s*```", "", response_text).strip()

                if base.is_json_format(response_text):
                    json_result = json.loads(response_text)
                    operation_name = json_result["operation name"] if "operation name" in json_result else response_text
                    operation_protocol = json_result["protocol"] if "protocol" in json_result else response_text
                    response_container.json(json_result)

            except Exception as e:
                response_container.caption(f"error when calling api: {e}")

    # 수술기록지 결과 비교: 기존 vs 신규
    or_draft = None
    with st.expander("수술기록지 신규", expanded=False):
        if "or-result" in st.session_state:
            result = st.session_state["or-result"]
            st.caption(result)

            if or_info and "or" in or_info and len(or_info["or"]):
                or_draft = note.generate_or_draft(or_info["or"][0], operation_name, operation_protocol)
                st.json(or_draft)

    # 수술기록지 결과 포맷
    with st.expander("수술기록지 신규", expanded=False):
        display_report(or_draft)

def display_report(or_instance):
    st.header("수술기록지 (Operation Record)")

    if or_instance is None:
        st.write("수술기록지가 없습니다.")
        return

    st.subheader("환자정보")
    st.write("등록번호")
    st.caption(or_instance["patient"]["patient id"])

    st.subheader("의료진정보")
    cols = st.columns(3)
    with cols[0]:
        st.write("Surgeon")
        st.caption(base.ifnull(or_instance["clinical staff"]["department"], "<na>") + " / "
                 + base.ifnull(or_instance["clinical staff"]["doctor in charge"], "<na>") + " / "
             + str(base.ifnull(or_instance["clinical staff"]["doctor assistant"], 0)))
    with cols[1]:
        st.write("PA")
        st.write("Nurse")
    with cols[2]:
        st.write("Anesthesiologist")
        st.write("Method of Anesthesia")

    st.subheader("진단정보")
    st.write("Preoperative Diagnosis")
    st.caption(or_instance["operation data"][7] if or_instance["operation data"] and len(or_instance["operation data"])>=11 else or_instance["operation data"])
    st.write("Postoperative Diagnosis")
    st.caption(or_instance["operation data"][11] if or_instance["operation data"] and len(or_instance["operation data"])>=11 else None)

    st.subheader("수술정보")
    st.write("Name of Operation")
    st.caption(or_instance["operation data"][8] if or_instance["operation data"] and len(or_instance["operation data"])>=11 else None)
    st.write("Procedures & Findings")
    st.caption(or_instance["operation procedures and findings"])

    st.write("수술 중 특이사항")
    memo = or_instance["operation notes"]
    if memo is None or memo[0] == 'N':
        memo = "무"
    else:
        memo = "유 : " + memo[2:]
    st.caption(memo)

    st.subheader("수술정보")
    cols = st.columns(4)
    with cols[0]:
        st.caption("alarm: <>")
        st.caption(or_instance["additional data"]["alarm"])
    with cols[1]:
        st.write("패드확인 (유/무)")
        st.caption("cmplyn: <>")
        st.caption(or_instance["additional data"]["cmplyn"])
        st.caption("emdv: <>")
        st.caption(or_instance["additional data"]["emdv"])
        st.caption("pclr: <>")
        st.caption(or_instance["additional data"]["pclr"])
    with cols[2]:
        st.write("Tissue of Path. (Y/N)")
        st.caption(or_instance["operation check"]["tissue examination"])
        st.caption(or_instance["operation check"]["tissue examination contents"])
    with cols[3]:
        st.write("Drains (Y/N)")
        st.caption(or_instance["operation check"]["drain pipe"])
        st.caption(or_instance["operation check"]["drain pipe contents"])
    
    cols = st.columns(2)
    with cols[0]:
        st.write("수술일시")
        st.caption(f"{or_instance['operation date']} {or_instance['operation start time']} ~ {or_instance['operation end time']}") 
    with cols[1]:
        st.write("작성일시")
        st.caption(f"{or_instance['report date']} {or_instance['report time']}")
    
    st.write("치료계획")
    st.caption(or_instance["medical treatment plan"])
    st.write("수술경과")
    st.caption(or_instance["operation progress"])
