import utils.base as base
import utils.note as note
import utils.note_template as template

import json
import re

import streamlit as st

def op_record_source():
    mr_json = st.session_state.get("mr_json")

    postfix = ""
    if mr_json is None or "operation records" not in mr_json or len(mr_json["operation records"]) == 0:
        postfix = " (기록없음)"

    with st.expander("수술기록지" + postfix, expanded=False):
        display_report(st.session_state.get("mr_json"))

    return "op-record-source"

OR_PROMPT_DEFAULT = """1. 입력된 데이터의 "present illness" , "impression", "plan", "operation name"을 확인하여 "estimated operation name"을 추정하라.
2. 추정된 "estimated operation name"을 참조하여 "protocols of doctor"의 "code" 또는 "code name"과 대응하는 것을 찾아서 해당하는 "protocol"을 찾아라.
3. 응답으로 "present illness" 와 "impression", "plan", "operation name", "estimated operation name"과 "code", "code name", "protocol"을 json format으로 제시하라.
"""

def op_record_target():
    # 수술기록지 생성 프롬프트
    # st.text_area("Prompt", value=OR_PROMPT_DEFAULT, height=150, key="or-prompt")

    # 수술기록지 작성 버튼
    cols = st.columns([3, 3, 4])
    with cols[0]:
        or_write = st.button("➡️ 수술기록지 초안 작성", key="or-write", use_container_width=True)

    with cols[1]:
        with st.popover("⚙️ Prompt", use_container_width=True):
            # 퇴원요약지 생성 프롬프트
            st.text_area("Prompt", value=OR_PROMPT_DEFAULT, height=150, key="or-prompt")

    with cols[2]:
        st.radio("AI 모델 선택", ["MedLM", "Gemini-Pro", "Gemini-Flash"], key="ai-model-or", index=2, horizontal=True, label_visibility="collapsed")

    if or_write:
        mr_json = st.session_state.get("mr_json")
        if "mr_json" not in st.session_state or "patient" not in mr_json:
            return

        mr_json_new = template.get_medical_record_template()

        mr_json_new["patient"] = mr_json["patient"]
        mr_json_new["clinical staff"] = mr_json["clinical staff"]

        mr_json_new["subjective"] = mr_json["subjective"]
        mr_json_new["objective"] = mr_json["objective"]
        mr_json_new["assessment"] = mr_json["assessment"]
        mr_json_new["plan"] = mr_json["plan"]

        mr_json_new["operation protocols"] = mr_json["operation protocols"]

        operation_name, operation_protocol = "", ""
        

        with st.expander("AI지원 프로토콜 선택", expanded=True):
            st.session_state["or-result"] = ""
            response_text = ""
            response_container = st.empty()
            try:
                responses = note.call_api(st.session_state["or-prompt"], json.dumps(mr_json_new), st.session_state["ai-model-or"].lower())
                for response in responses:
                    response_text += response.text
                    response_container.caption(response_text)

                st.session_state["or-result"] = response_text

                response_text = re.sub(r"```json\s*|\s*```", "", response_text).strip()

                if base.is_json_format(response_text):
                    json_result = json.loads(response_text)
                    operation_name = json_result["estimated operation name"] if "estimated operation name" in json_result else response_text
                    operation_protocol = json_result["protocol"] if "protocol" in json_result else response_text
                    response_container.json(json_result)

            except Exception as e:
                response_container.caption(f"error when calling api: {e}")

        op_record = mr_json_new["operation records"][0]
        op_record["operation name"] = operation_name
        op_record["operation procedures and findings"] = operation_protocol

        mr_json_new["operation records"] = []
        mr_json_new["operation records"].append(op_record)

        # 수술기록지 결과 포맷
        with st.expander("수술기록지 신규", expanded=False):
            display_report(mr_json_new, "new")
    pass

OP_01_HEADER = """
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: `{} `  
**입 원 일**: `{} `  
**진 료 과**: `{} `  

</td>
<td align="center" width="50%">

### 수술기록지 ( Operation Record )
Date of Operation: `{} `

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="좋은병원들" width="120">  
</td>
</tr>
</table>

"""
OP_02_STAFF = """
<table width="100%">
<tr>
<td colspan="2" align="left" width="25%">
<b>Surgeon</b>: {}  
</td>
<td colspan="2" align="left" width="25%">
<b>PA</b>:   {} 
</td>
<td colspan="2" align="left" width="25%">
<b>Nurse</b>:  {}  
</td>
<td colspan="2" align="left" width="25%">
<b>Anesthesiologist</b>:   {} 
</td>
</tr>
<tr>
<td colspan="6" align="left">
</td>
<td colspan="2" align="left">
<b>Method of Anesthesia</b>: {} 
</td>
</tr>
</table>
"""
OP_03_DIAGNOSIS = """
#### Preoperative diagnosis:  
```{}  
```
#### Postoperative diagnosis:  
```{}  
```
#### Name of Operation:  
```{}  
```
---
"""
OP_04_PROCEDURES = """

#### Procedures & Findings:  

"""
OP_05_MEMO = """
#### 특이사항:
```{}
```"""
OP_06_ADDITIONAL = """
<table width="100%">
<tr>
<td width="33%" align="center">

##### 출혈정도:   
패드 확인:  ☐ 유  ■ 무  
</td>
<td width="33%" align="center">

##### **Tissue of path.**:  
■ Yes   ☐ No 
</td>
<td width="33%" align="center">

##### **Drains**:  
☐ Yes (      )   ■ No  
</td>
</tr>
</table>

##### 수술일시:   
- `{} `  **2024년10월22일 10시40분 ~ 11시00분 종료**  
"""
OP_07_TAIL = """
<table width="100%">
<tr>
<td width="50%">
<b>Dictated Written by</b>: {}
</td>
<td width="25%" align="right">
<b>Surgeon's Signatures</b>: {} 
</td>
<td width="25%" align="right">
</td>
</tr>
</table>


**작성일시**: `{} {} `  
"""

def display_report(mr_instance, param="0"):
    if mr_instance is None:
        st.write("의무기록이 없습니다.")
        return

    if "operation records" not in mr_instance or len(mr_instance["operation records"]) == 0:
        st.write("수술기록지가 없습니다.")
        return

    op_record = mr_instance["operation records"][0]

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown("""
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
    """, unsafe_allow_html=True)

    st.write(OP_01_HEADER.format(
        mr_instance["patient"]["patient id"], 
        mr_instance["patient"]["date of admission"], 
        mr_instance["clinical staff"]["department"], 
        op_record["operation date"]), unsafe_allow_html = True)
    st.write(OP_02_STAFF.format(
        base.ifnull(op_record["surgeon"], "<na>"), 
        base.ifnull(op_record["assistant"], "<na>"), 
        base.ifnull(op_record["nurse"], "<na>"), 
        base.ifnull(op_record["anesthesiologist"], "<na>"), 
        base.ifnull(op_record["method of anesthesia"], "<na>")), unsafe_allow_html = True)
    st.write(OP_03_DIAGNOSIS.format(
        base.ifnull(op_record["preoperative diagnosis"], "<na>"), 
        base.ifnull(op_record["postoperative diagnosis"], "<na>"),
        base.ifnull(op_record["operation name"], "<na>")))
    st.write(OP_04_PROCEDURES.format(
        base.ifnull("", "<na>")), unsafe_allow_html = True)
    st.text_area("procedures",op_record["operation procedures and findings"], height=300, label_visibility= "collapsed")

    st.write(OP_05_MEMO.format(
        base.ifnull(op_record["operation notes"], "무")), unsafe_allow_html = True)
    cols = st.columns([1,4])
    with cols[0]:
        st.radio("특이사항 유무", ["유", "무"], key=f"abnormality_{param}", index=1, horizontal=True, label_visibility="collapsed")
    with cols[1]:
        st.text_input("특이사항", op_record["operation notes"], label_visibility= "collapsed")

    st.write(OP_06_ADDITIONAL.format(
        base.ifnull(op_record["additional data"]["alarm"], "<na>"), 
        base.ifnull(op_record["additional data"]["cmplyn"], "<na>"), 
        base.ifnull(op_record["additional data"]["emdv"], "<na>"), 
        base.ifnull(op_record["additional data"]["pclr"], "<na>"), 

        base.ifnull(op_record["operation check"]["tissue examination"], "<na>"), 
        base.ifnull(op_record["operation check"]["tissue examination contents"], "<na>"), 
        base.ifnull(op_record["operation check"]["drain pipe"], "<na>"), 
        base.ifnull(op_record["operation check"]["drain pipe contents"], "<na>"), 

        base.ifnull(op_record["operation date"], "<na>")), unsafe_allow_html = True)
    st.write(OP_07_TAIL.format(
        base.ifnull(mr_instance["clinical staff"]["doctor in charge"], "<na>"), 
        base.ifnull(mr_instance["clinical staff"]["doctor in charge"], 0), 
        base.ifnull(op_record["report date"], "<na>"),
        base.ifnull(op_record["report time"], "<na>")), unsafe_allow_html = True)
    
    # st.markdown(OP_01_HEADER)
    # st.markdown(OP_02_STAFF)
    # st.markdown(OP_03_DIAGNOSIS)
    # st.markdown(OP_04_PROCEDURES)
    # st.markdown(OP_05_MEMO)
    # st.markdown(OP_06_ADDITIONAL)
    # st.markdown(OP_07_TAIL)

    pass

def display_report_old(mr_instance):
    st.divider()

    st.subheader("환자정보")
    st.write("등록번호")
    st.caption(mr_instance["patient"]["patient id"])

    st.subheader("의료진정보")
    cols = st.columns(3)
    with cols[0]:
        st.write("Surgeon")
        st.caption(base.ifnull(mr_instance["clinical staff"]["department"], "<na>") + " / "
                 + base.ifnull(mr_instance["clinical staff"]["doctor in charge"], "<na>") + " / "
             + str(base.ifnull(mr_instance["clinical staff"]["doctor assistant"], 0)))
    with cols[1]:
        st.write("PA")
        st.write("Nurse")
    with cols[2]:
        st.write("Anesthesiologist")
        st.write("Method of Anesthesia")

    st.subheader("진단정보")
    st.write("Preoperative Diagnosis")
    st.caption(mr_instance["operation data"][7] if mr_instance["operation data"] and len(mr_instance["operation data"])>=11 else mr_instance["operation data"])
    st.write("Postoperative Diagnosis")
    st.caption(mr_instance["operation data"][11] if mr_instance["operation data"] and len(mr_instance["operation data"])>=11 else None)

    st.subheader("수술정보")
    st.write("Name of Operation")
    st.caption(mr_instance["operation data"][8] if mr_instance["operation data"] and len(mr_instance["operation data"])>=11 else None)
    st.write("Procedures & Findings")
    st.caption(mr_instance["operation procedures and findings"])

    st.write("수술 중 특이사항")
    memo = mr_instance["operation notes"]
    if memo is None or memo[0] == 'N':
        memo = "무"
    else:
        memo = "유 : " + memo[2:]
    st.caption(memo)

    st.subheader("수술정보")
    cols = st.columns(4)
    with cols[0]:
        st.caption("alarm: <>")
        st.caption(mr_instance["additional data"]["alarm"])
    with cols[1]:
        st.write("패드확인 (유/무)")
        st.caption("cmplyn: <>")
        st.caption(mr_instance["additional data"]["cmplyn"])
        st.caption("emdv: <>")
        st.caption(mr_instance["additional data"]["emdv"])
        st.caption("pclr: <>")
        st.caption(mr_instance["additional data"]["pclr"])
    with cols[2]:
        st.write("Tissue of Path. (Y/N)")
        st.caption(mr_instance["operation check"]["tissue examination"])
        st.caption(mr_instance["operation check"]["tissue examination contents"])
    with cols[3]:
        st.write("Drains (Y/N)")
        st.caption(mr_instance["operation check"]["drain pipe"])
        st.caption(mr_instance["operation check"]["drain pipe contents"])
    
    cols = st.columns(2)
    with cols[0]:
        st.write("수술일시")
        st.caption(f"{mr_instance['operation date']} {mr_instance['operation start time']} ~ {mr_instance['operation end time']}") 
    with cols[1]:
        st.write("작성일시")
        st.caption(f"{mr_instance['report date']} {mr_instance['report time']}")
    
    st.write("치료계획")
    st.caption(mr_instance["medical treatment plan"])
    st.write("수술경과")
    st.caption(mr_instance["operation progress"])
