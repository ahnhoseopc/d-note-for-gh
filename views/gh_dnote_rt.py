import re
import utils.base as base
import utils.note as note
import utils.note_template  as template

import json

import streamlit as st

def extract_discharge(mr_json):
    if mr_json is None:
        return None
    
    if "discharge summary" not in mr_json and keys:
        return None

    discharge = mr_json["discharge summary"]
    if len(discharge.keys()) == 0:
        return None

    return discharge

def rt_summary_source():
    mr_json = st.session_state.get("mr_json")
    discharge = extract_discharge(mr_json)
    with st.expander("퇴원요약지", expanded=discharge is None):
        display_discharge_summary(st.session_state.get("mr_json"))


RT_PROMPT_DEFAULT = """
퇴원요약지의 각 항목 ,즉, 환자의 주호소, 주진단명, 부진단명, 수술명, 처치명, 중요검사소견, 추후관리계획, 경과요약, 치료결과, 퇴원형태, 퇴원약을 주어진 데이터를 확인하여  아래 가이드라인을 참고하여 작성하라.

1. 중요검사소견은 입원기간내에 시행한 조직검사결과를 원본 데이터 그대로 옮겨오도록 한다.

2. 경과요약은 입원사유와 수술내용, 검사결과, 경과기록을 각 한줄씩 작성하도록 한다. 평문으로 작성하라.
첫번쨰  줄은 "date of admission", "chief compaints" 와 "present illness", "impression" 등을 참고하여 입원사유를 입원날짜와 함께 작성한다. 
두번쨰 줄은 "operation"속성 내의 "operation date", "operation data", "operation procedures and findings", "operation notes"등을 참고하여 "[수술일자] 수술내용 요약"을  작성한다.  "operation"속성이 없으면 이 줄은 작성하지 않는다.
세번째 줄은 검사결과는 [검사일] 입원기간내의 조직검사결과를 요약하여 특이사항여부를 한줄로 요약한다.
네번째 줄은 경과기록은 [퇴원일]과 함께 "progress notes"내의 날짜별 기록을 참고하여 환자의 경과의 변화를 한줄로 요약한다. 검사결과와 이상소견여부를 확인하도록 한다.

3. 날짜는 "[2025-01-01]" 형식으로 표시한다.

4. 출력은 JSON으로 아래 형식으로 출력하라.
{"환자의 주호소":"", "주진단명":"", "부진단명":"", "수술명":"", "처치명":"", "중요검사소견":"", "추후관리계획":"", "경과요약":"", "치료결과":"", "퇴원형태":"", "퇴원약":""}
"""

def prepare_request_data(mr_json):
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

    return mr_json_new

def fill_in_discharge_summary(mr_json, findings, progress_summary):
    mr_json_new = prepare_request_data(mr_json)

    mr_json_new["discharge summary"] = mr_json["discharge summary"]
    mr_json_new["discharge summary"]["abnormal findings and lab result"] = findings
    mr_json_new["discharge summary"]["progress summary"] = progress_summary

    return mr_json_new

def rt_summary_target():
    cols = st.columns([3, 3, 3])
    with cols[0]:
        rt_write = st.button("➡️ 퇴원요약지 초안 작성", key="rt-write", use_container_width=True)

    with cols[1]:
        with st.popover("⚙️ Prompt", use_container_width=True):
            st.text_area("Prompt", value=RT_PROMPT_DEFAULT, height=150, key="rt-prompt")

    with cols[2]:
        st.radio("AI 모델 선택", ["MedLM", "Gemini-Pro", "Gemini-Flash"], key="ai-model-rt", index=2, horizontal=True, label_visibility="collapsed")

    if rt_write:
        mr_json = st.session_state.get("mr_json")
        mr_json_new = prepare_request_data(mr_json)

        with st.expander("AI 결과", expanded=True):
            st.session_state["rt-result"] = ""
            response_container = st.empty()
            response_container.caption(st.session_state["rt-result"])
            try:
                responses = note.call_api(st.session_state["rt-prompt"], json.dumps(mr_json, indent=4), st.session_state["ai-model-rt"].lower())

                for response in responses:
                    st.session_state["rt-result"] += response.text
                    response_container.caption(st.session_state["rt-result"])

                st.session_state["rt-result"] = re.sub(r"```json\s*|\s*```", "", st.session_state["rt-result"]).strip()
                
                if base.is_json_format(st.session_state["rt-result"]):
                    result_json = json.loads(st.session_state["rt-result"])
                    response_container.json(result_json)
            except Exception as e:
                response_container.caption(f"error when calling api: {e}")
                pass
        
        mr_json_new = fill_in_discharge_summary(mr_json, result_json["중요검사소견"], result_json["경과요약"])

        with st.expander("퇴원요약지 초안", expanded=False):
            display_discharge_summary(mr_json_new, "new")
    pass

RT_00_STYLE_0 = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: none !important;
            padding: 10px;
            text-align: left;
        }
    </style>
"""
RT_01_HEADER_4 = """
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**입 원 일**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### 퇴원요약지 (Discharge Summary)
Date of Discharge: {}

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="좋은병원들" width="120">  
</td>
</tr>
</table>

---
"""

def display_discharge_summary(mr_json, param="old"):
    discharge = extract_discharge(mr_json)
    if discharge is None:
        st.write("퇴원요약지가 없습니다.")
        return


    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(RT_00_STYLE_0, unsafe_allow_html=True)

    st.write(RT_01_HEADER_4.format(
        mr_json["patient"]["patient id"], 
        mr_json["patient"]["date of admission"],
        mr_json["clinical staff"]["department"], 
        discharge["date of discharge"]), unsafe_allow_html = True)

    st.markdown("##### 주호소/입원사유")
    st.caption(discharge["chief complaints"])

    st.markdown("##### 주진단명 (Final Diagnosis)")
    st.caption(discharge["final diagnosis"])
    st.markdown("##### 부진단명 (Secondary Diagnosis)")
    st.caption(discharge["secondary diagnosis"])

    st.markdown("##### 수술명 (Treatment Op.)")
    st.caption(discharge["treatment operation"])
    st.markdown("##### 처치명 (Treatment Medical)")
    st.caption(discharge["treatment medication"])

    st.markdown("##### 중요검사소견 (Abnormal Finding or Lab)")
    st.text_area(label="중요검사소견", height=180, value=discharge["abnormal findings and lab result"], key=f"findings_{param}", label_visibility= "collapsed")
    st.markdown("##### 추후관리계획 (Follow-up Plan)")
    st.text_input(label="추후관리계획", value=discharge["follow-up plan"], key=f"follow_up_plan_{param}", label_visibility= "collapsed")
    st.markdown("##### 경과요약 (Progress Summary)")
    st.text_area(label="경과요약", height=180, value=discharge["progress summary"], key=f"progress_summary_{param}", label_visibility= "collapsed")

    st.markdown("##### 치료결과 (Result)")
    st.caption(discharge["treatment result"])
    st.markdown("##### 퇴원형태 (Type of Discharge)")
    st.caption(discharge["type of discharge"])
    st.markdown("##### 비고 (Discharge Comments)")
    st.caption(discharge["discharge comments"])

    st.markdown("##### 기록일")
    st.caption(discharge["report date"])
    st.markdown("##### 기록시간")
    st.caption(discharge["report time"])

    # st.markdown("##### 퇴원약 (Medicine)")
