import utils.base as base
import utils.note as note
import utils.note_template  as template

import json

import streamlit as st

def rt_summary_source():
    with st.expander("소스 의료정보 (API입력데이터)", expanded=True):
        if st.session_state.get("mr_json"):
            st.json(st.session_state["mr_json"], expanded=1)

        # Source data display
        if st.session_state.get("mr_info"):
            st.write("입원기록지")
            st.json(st.session_state["mr_info"]["ae"], expanded=1)
            st.write("입원기록지 GY")
            st.json(st.session_state["mr_info"]["ay"], expanded=1)
            st.write("상병/진단")
            st.json(st.session_state["mr_info"]["il"], expanded=1)    

            st.write("수술예약")
            st.json(st.session_state["mr_info"]["oy"], expanded=1)    
            st.write("수술기록지")
            st.json(st.session_state["mr_info"]["or"], expanded=1)    

            st.write("경과기록지")
            st.json(st.session_state["mr_info"]["pn"], expanded=1)

            st.write("검사결과")
            st.json(st.session_state["mr_info"]["je"], expanded=1)
            st.json(st.session_state["mr_info"]["te"], expanded=1)
            st.json(st.session_state["mr_info"]["ce"], expanded=1)
            st.json(st.session_state["mr_info"]["yt"], expanded=1)

    with st.expander("기존 퇴원요약지 (문서양식)", expanded=False):
        display_report(st.session_state.get("mr_json"))



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

    mr_json = st.session_state.get("mr_json")
    mr_json_new = template.get_medical_record_template()
    mr_json_new["patient"] = mr_json["patient"]
    mr_json_new["clinical staff"] = mr_json["clinical staff"]

    mr_json_new["subjective"] = mr_json["subjective"]
    mr_json_new["objective"] = mr_json["objective"]
    mr_json_new["assessment"] = mr_json["assessment"]
    mr_json_new["plan"] = mr_json["plan"]

    mr_json_new["operation records"] = mr_json["operation records"]
    mr_json_new["progress notes"] = mr_json["progress notes"]

    mr_json_new["discharge protocols"] = mr_json["discharge protocols"]

    operation_name, operation_protocol = "", ""

    protocol = ""
    if rt_write:
        with st.expander("AI지원 퇴원요약지 초안", expanded=True):
            st.session_state["rt-result"] = ""
            response_container = st.empty()
            response_container.caption(st.session_state["rt-result"])
            try:
                responses = note.call_api(st.session_state["rt-prompt"], json.dumps(mr_json, indent=4), st.session_state["ai-model-rt"].lower())
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
        display_report(mr_json_new, "new")


def display_report(mr_json, param="old"):
    ds = mr_json["discharge summary"]

    st.write("퇴원요약지 (Discharge Summary)")

    st.write("주호소/입원사유")
    st.caption(ds["chief complaints"])

    st.write("주진단명 (Final Diagnosis)")
    st.caption(ds["final diagnosis"])
    st.write("부진단명 (Secondary Diagnosis)")
    st.caption(ds["secondary diagnosis"])

    st.write("수술명 (Treatment Op.)")
    st.caption(ds["treatment operation"])
    st.write("처치명 (Treatment Medical)")
    st.caption(ds["treatment medication"])

    st.write("중요검사소견 (Abnormal Finding or Lab)")
    st.text_area(ds["abnormal findings and lab result"], key=f"findings_{param}")
    st.write("추후관리계획 (Follow-up Plan)")
    st.text_area(ds["follow-up plan"], key=f"follow_up_plan_{param}")
    st.write("경과요약 (Progress Summary)")
    st.text_area(ds["progress summary"], key=f"progress_summary_{param}")

    st.write("치료결과 (Result)")
    st.caption(ds["treatment result"])
    st.write("퇴원형태 (Type of Discharge)")
    st.caption(ds["type of discharge"])
    st.write("비고 (Discharge Comments)")
    st.caption(ds["discharge comments"])

    st.write("퇴원일)")
    st.caption(ds["report date"])
    st.write("퇴원시간)")
    st.caption(ds["report time"])

    st.write("퇴원약 (Medicine)")
