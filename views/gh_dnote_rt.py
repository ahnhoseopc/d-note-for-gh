import utils.base as base
import utils.note as note
import json

import streamlit as st

rt_info = None

def rt_summary_source():
    global rt_info

    # Get the list of doctors by department
    if "doctors_by_dept" not in st.session_state or st.session_state.doctors_by_dept is None:
        st.session_state.doctors_by_dept = note.get_doctors_by_dept()

    col11,col12 = st.columns([1, 1])
    with col11:
        # Get the list of departments
        depts = st.session_state.doctors_by_dept["kwa"].unique()
        kwa = st.selectbox("진료과", options=depts, key="rt-dept", placeholder="진료과", label_visibility="collapsed")

    with col12:
        # Get the list of doctors for the selected department
        doctors = st.session_state.doctors_by_dept[st.session_state.doctors_by_dept["kwa"]==st.session_state["rt-dept"]]["spth"]
        spth = st.selectbox("진료의", options=doctors, key="rt-doctor", placeholder="진료의", label_visibility="collapsed")
        
        # Get the list of patients for the selected doctor
        st.session_state.rt_patients = note.get_patient_by_doctor(spth)

    # Display the list of patients
    selected_row = st.dataframe(st.session_state.rt_patients, key="rt-selected-patient", on_select="rerun", selection_mode="single-row", height=140, use_container_width=True)

    # Collect the discharge summary source from source data
    if selected_row and len(selected_row.selection.rows)>0:
        idnoa = st.session_state.rt_patients["idnoa"][selected_row["selection"]["rows"][0]]
        lwdat = st.session_state.rt_patients["lwdat"][selected_row["selection"]["rows"][0]]

        rt_info = note.collect_rt_source(idnoa, lwdat, kwa, spth)

    st.divider()

    with st.expander("소스 의료정보 (API입력데이터)", expanded=True):
        if rt_info:
            st.json(rt_info["rt-source"], expanded=1)

    with st.expander("소스 의료정보 (DB원본)", expanded=False):
        # Source data display
        if rt_info:
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

    with st.expander("기존 퇴원요약지 (DB)", expanded=False):
        st.write("퇴원요약지 (DB)")
        if rt_info and "rt" in rt_info and len(rt_info["rt"]) > 0:
            st.json(rt_info["rt"], expanded=1)

        # st.write("퇴원요약지 (항목)")
        # if rt_info and "rt-current" in rt_info and len(rt_info["rt-current"]) > 0:
        #     st.json(rt_info["rt-current"], expanded=1)

    with st.expander("기존 퇴원요약지 (문서양식)", expanded=False):
        st.write("퇴원요약지 (Discharge Summary)")
        if rt_info and "rt" in rt_info and len(rt_info["rt"]):
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


RT_PROMPT_DEFAULT = """환자의 주호소, 주진단명, 부진단명, 수술명, 처치명, 중요검사소견, 추후관리계획, 경과요약, 치료결과, 퇴원형태, 퇴원약을 확인하여 퇴원요약지를 작성하라.

1. 중요검사소견은 입원기간내에 시행한 조직검사결과를 원본 데이터 그대로 옮겨오도록 한다.

2. 경과요약은 입원사유와 수술내용, 검사결과, 경과기록을 각 한줄씩 작성하도록 한다.

입원사유는 "date of admission", "chief compaints" 와 "present illness", "impression" 등을 참고하여 작성하고
수술내용은 "operation"속성 내의 "operation date", "operation data", "operation procedures and findings", "operation notes"등을 참고한다. "operation"속성이 없으면 작성하지 않는다.
검사결과는 검사일과 입원기간내의 조직검사결과를 요약하여 특이사항여부를 한줄로 요약한다.
경과기록은 퇴원일과 함께 "progress notes"내의 날짜별 기록을 참고하여 환자의 경과의 변화를 한줄로 요약한다. 검사결과와 이상소견여부를 확인하도록 한다.

3. 날짜는 "[2025-01-01]" 형식으로 표시한다."""

RT_PROMPT_DEFAULT = """
퇴원요약지의 각 항목 ,즉, 환자의 주호소, 주진단명, 부진단명, 수술명, 처치명, 중요검사소견, 추후관리계획, 경과요약, 치료결과, 퇴원형태, 퇴원약을 주어진 데이터를 확인하여  아래 가이드라인을 참고하여 작성하라.

1. 중요검사소견은 입원기간내에 시행한 조직검사결과를 원본 데이터 그대로 옮겨오도록 한다.

2. 경과요약은 입원사유와 수술내용, 검사결과, 경과기록을 각 한줄씩 작성하도록 한다. 
첫번쨰  줄은 "date of admission", "chief compaints" 와 "present illness", "impression" 등을 참고하여 입원사유를 입원날짜와 함께 작성한다. 
두번쨰 줄은 "operation"속성 내의 "operation date", "operation data", "operation procedures and findings", "operation notes"등을 참고하여 "[수술일자] 수술내용 요약"을  작성한다.  "operation"속성이 없으면 이 줄은 작성하지 않는다.
세번째 줄은 검사결과는 [검사일] 입원기간내의 조직검사결과를 요약하여 특이사항여부를 한줄로 요약한다.
네번째 줄은 경과기록은 [퇴원일]과 함께 "progress notes"내의 날짜별 기록을 참고하여 환자의 경과의 변화를 한줄로 요약한다. 검사결과와 이상소견여부를 확인하도록 한다.

3. 날짜는 "[2025-01-01]" 형식으로 표시한다."""

def rt_summary_target():
    # 퇴원요약지 생성 프롬프트
    st.text_area("Prompt", value=RT_PROMPT_DEFAULT, height=150, key="rt-prompt")

    # 수술기록지 작성 버튼
    cols = st.columns([3, 4])
    with cols[0]:
        rt_write = st.button("➡️ 퇴원요약지 경과 요약", key="rt-write")

    with cols[1]:
        st.radio("AI 모델 선택", ["MedLM", "Gemini-Pro", "Gemini-Flash"], key="ai-model-rt", index=2, horizontal=True, label_visibility="collapsed")

    protocol = ""
    if rt_write:
        with st.expander("AI지원 퇴원요약지 초안", expanded=True):
            st.session_state["rt-result"] = ""
            response_container = st.empty()
            response_container.caption(st.session_state["rt-result"])
            try:
                responses = note.call_api(st.session_state["rt-prompt"], json.dumps(rt_info["rt-source"], indent=4), st.session_state["ai-model-rt"].lower())
                for response in responses:
                    st.session_state["rt-result"] += response.text
                    response_container.caption(st.session_state["rt-result"])

                if base.is_json_format(st.session_state["rt-result"]):
                    result_json = json.loads(st.session_state["rt-result"])
                    response_container.json(result_json)
            except Exception as e:
                response_container.caption(f"error when calling api: {e}")
            print("rt-result= ", st.session_state["rt-result"])

    with st.expander("퇴원요약지 신규", expanded=False):
        st.caption(protocol)
