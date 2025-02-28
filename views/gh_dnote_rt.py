import utils.base as base
import utils.note as note
import utils.note_template  as template

import json
import re
import copy
from datetime import datetime

import streamlit as st

def rt_summary_source():
    mr_json = st.session_state.get("mr_json")

    postfix = ""
    if mr_json is None or "discharge summary" not in mr_json or len(mr_json["discharge summary"].keys()) == 0 or "date of discharge" not in mr_json["discharge summary"]:
        postfix = " (기록없음)"

    with st.expander("퇴원요약지" + postfix, expanded=False):
        display_discharge_summary(st.session_state.get("mr_json"))


RT_PROMPT_DEFAULT = """
퇴원요약지의 각 항목 ,즉, 환자의 주호소, 주진단명, 부진단명, 수술명, 처치명, 중요검사소견, 추후관리계획, 경과요약, 치료결과, 퇴원형태, 퇴원약을 주어진 데이터를 확인하여  아래 가이드라인을 참고하여 작성하라.

1. 중요검사소견은 입원기간내에 시행한 조직검사결과와 영상판독 내용을 결과날짜(yyyy-mm-dd 형식)와 함께 원본 데이터 그대로 옮겨오도록 한다.

2. 경과요약은 입원사유와 수술내용, 검사결과, 경과기록을 각 한줄씩 작성하도록 한다. 평문으로 작성하라.
첫번쨰  줄은 "date of admission", "chief compaints" 와 "present illness", "impression" 등을 참고하여 입원사유를 입원날짜와 함께 작성한다. 
두번째 줄은 "operation"속성 내의 "operation date", "operation data", "operation procedures and findings", "operation notes"등을 참고하여 "[수술일자] 수술내용 요약"을  작성한다.  "operation"속성이 없으면 이 줄은 작성하지 않는다.
세번째 줄은 검사결과는 [검사일] 입원기간내의 조직검사결과를 요약하여 특이사항여부를 한줄로 요약한다.
네번째 줄은 경과기록은 [퇴원일]과 함께 "progress notes"내의 날짜별 기록을 참고하여 환자의 경과의 변화를 한줄로 요약한다. 검사결과와 이상소견여부를 확인하도록 한다. 
각 줄에서 해당사항이 없으면 표시하지 않는다.

3. 날짜는 "[2025-01-01]" 형식으로 표시한다.

4. 출력은 JSON으로 아래 형식으로 출력하라.
{"환자의 주호소":"", "주진단명":"", "부진단명":"", "수술명":"", "처치명":"", "중요검사소견":"", "추후관리계획":"", "경과요약":"", "치료결과":"", "퇴원형태":"", "퇴원약":""}
"""

def prepare_request_data(mr_json):
    mr_json_new = template.get_medical_record_template()

    if mr_json is None or mr_json["patient"] is None:
        return None

    mr_json_new["patient"] = copy.deepcopy(mr_json["patient"])
    mr_json_new["clinical staff"] = copy.deepcopy(mr_json["clinical staff"])

    mr_json_new["subjective"] = copy.deepcopy(mr_json["subjective"])
    mr_json_new["objective"] = copy.deepcopy(mr_json["objective"])
    mr_json_new["assessment"] = copy.deepcopy(mr_json["assessment"])
    mr_json_new["plan"] = copy.deepcopy(mr_json["plan"])

    mr_json_new["operation records"] = copy.deepcopy(mr_json["operation records"])
    mr_json_new["progress notes"] = copy.deepcopy(mr_json["progress notes"])

    mr_json_new["discharge protocols"] = copy.deepcopy(mr_json["discharge protocols"])

    return mr_json_new

def fill_in_discharge_summary(mr_json_new, mr_json, findings, progress_summary):
    if "discharge summary" not in mr_json or mr_json["discharge summary"] is None or "date of discharge" not in mr_json["discharge summary"]:
        discharge = template.get_discharge_summary_template()
        discharge["date of discharge"] = datetime.now().strftime("%Y-%m-%d")
        discharge["chief complaints"] = mr_json_new["subjective"]["chief complaints"]

        discharge["treatment result"] = ""
        discharge["final diagnosis"] = "\n".join(mr_json_new["assessment"]["diagnosis"])
        discharge["secondary diagnosis"] = "\n".join(mr_json_new["assessment"]["diagnosis"])

        if len(mr_json_new["operation records"]) > 0:
            op_name = mr_json_new["operation records"][0]["operation name"]
        else:
            op_name = mr_json_new["plan"]["operation plan"]

        discharge["treatment operation"] = op_name
        discharge["treatment medication"] = ""

        discharge["follow-up plan"] = "외래진료 예정"

        discharge["abnormal findings and lab result"] = ""
        discharge["progress summary"] = ""
        discharge["treatment result"] = "2 경쾌"

        discharge["type of discharge"] = "1 퇴원"
        discharge["discharge comments"] = ""

        discharge["report date"] = datetime.now().strftime("%Y-%m-%d")
        discharge["report time"] = datetime.now().strftime("%H:%M:%S")
    else:
        discharge = copy.deepcopy(mr_json["discharge summary"])

    mr_json_new["discharge summary"] = discharge
    mr_json_new["discharge summary"]["abnormal findings and lab result"] = findings
    mr_json_new["discharge summary"]["progress summary"] = progress_summary

    return mr_json_new

def rt_summary_target():
    ai_models =  ["MedLM", "Gemini-Pro", "Gemini-Flash"]
    ai_model = ai_models[-1]
    rt_prompt = RT_PROMPT_DEFAULT

    cols = st.columns([3, 3, 3])
    with cols[0]:
        rt_write = st.button("➡️ 퇴원요약지 초안 작성", key="rt-write", use_container_width=True, disabled=not st.session_state.get("mr_json"))

    with cols[1]:
        if "user_id" in st.session_state and st.session_state.user_id == "dma":
            with st.popover("⚙️ Prompt", use_container_width=True):
                prompt = st.text_area("Prompt", value=RT_PROMPT_DEFAULT, height=150, key="rt-prompt")
                if prompt:
                    rt_prompt = prompt

    with cols[2]:
        if "user_id" in st.session_state and st.session_state.user_id == "dma":
            with st.popover("⚙️ AI 모델", use_container_width=True):
                ai_model = st.radio("AI 모델 선택", ai_models, key="ai-model-rt", index=2, horizontal=True, label_visibility="collapsed")

    if rt_write:
        mr_json = st.session_state.get("mr_json")
        mr_json_new = prepare_request_data(mr_json)

        with st.expander("AI 결과", expanded=False):
            st.session_state["rt-result"] = ""
            response_container = st.empty()
            response_container.caption(st.session_state["rt-result"])
            try:
                responses = note.call_api(rt_prompt, json.dumps(mr_json, indent=4), ai_model.lower())

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
        
        mr_json_new = fill_in_discharge_summary(mr_json_new, mr_json, result_json["중요검사소견"], result_json["경과요약"])

        with st.expander("퇴원요약지 초안", expanded=False):
            display_discharge_summary(mr_json_new, "new")

        cols = st.columns(2)
        with cols[0]:
            display_discharge_summary(mr_json, "o1")
        with cols[1]:
            display_discharge_summary(mr_json_new, "n2")
        
    pass

def display_discharge_summary(mr_json, param="old"):

    if mr_json is None:
        st.write("의무기록이 없습니다.")
        return None
    
    if "discharge summary" not in mr_json:
        st.write("퇴원요약지가 없습니다.")
        return None

    discharge = mr_json["discharge summary"]
    if discharge is None or "date of discharge" not in discharge:
        st.write("퇴원요약지가 없습니다.")
        return None

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

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(RT_00_STYLE_0, unsafe_allow_html=True)

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
    st.write(RT_01_HEADER_4.format(
        mr_json["patient"]["patient id"], 
        mr_json["patient"]["date of admission"],
        mr_json["clinical staff"]["department"], 
        discharge["date of discharge"]), unsafe_allow_html = True)

    st.markdown("##### 주호소/입원사유")
    st.code(discharge["chief complaints"])

    st.markdown("##### 주진단명 (Final Diagnosis)")
    st.text_area(label="주진단명", key=f"pdiagnosis_{param}", height=68, value=discharge["final diagnosis"], label_visibility="collapsed")
    st.markdown("##### 부진단명 (Secondary Diagnosis)")
    st.text_area(label="부진단명", key=f"sdiagnosis_{param}", height=68, value=discharge["secondary diagnosis"], label_visibility="collapsed")

    st.markdown("##### 수술명 (Treatment Op.)")
    st.text_area(label="수술명", key=f"operation_{param}", height=68, value=discharge["treatment operation"], label_visibility="collapsed")
    st.markdown("##### 처치명 (Treatment Medical)")
    st.text_area(label="처치명", key=f"treatment_{param}", height=68, value=discharge["treatment medication"], label_visibility="collapsed")

    st.markdown("##### 🔵 중요검사소견 (Abnormal Finding or Lab) ")
    st.text_area(label="중요검사소견", key=f"findings_{param}", height=180, value=discharge["abnormal findings and lab result"], label_visibility= "collapsed")

    st.markdown("##### 추후관리계획 (Follow-up Plan)")
    st.text_area(label="추후관리계획", key=f"follow_up_{param}", height=68, value=discharge["follow-up plan"], label_visibility= "collapsed")

    st.markdown("##### 🔵 경과요약 (Progress Summary) ")
    with st.container():
        st.text_area(label="경과요약", key=f"progress_summary_{param}", height=180, value=discharge["progress summary"], label_visibility= "collapsed")

    st.markdown("##### 치료결과 (Result)")
    discharge["treatment result"] = "1 완쾌" if discharge["treatment result"].strip() == "1" else "2 경쾌" if discharge["treatment result"].strip() == "2" else discharge["treatment result"]
    st.text_area(label="치료결과", key=f"treatment_result_{param}", height=68, value=discharge["treatment result"], label_visibility= "collapsed")
    st.markdown("##### 퇴원형태 (Type of Discharge)")
    discharge["type of discharge"] = "1 퇴원" if discharge["type of discharge"].strip() == "1" else discharge["type of discharge"]
    st.text_area(label="퇴원형태", key=f"discharge_type_{param}", height=68, value=discharge["type of discharge"], label_visibility= "collapsed")
    st.markdown("##### 비고 (Discharge Comments)")
    st.text_area(label="비고", key=f"discharge_comments_{param}", height=68, value=discharge["discharge comments"], label_visibility= "collapsed")

    st.markdown("##### 기록일")
    st.code(discharge["report date"])
    st.markdown("##### 기록시간")
    st.code(discharge["report time"])

    # st.markdown("##### 퇴원약 (Medicine)")
