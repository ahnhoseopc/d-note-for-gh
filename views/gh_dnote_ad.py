import utils.base as base

import streamlit as st

def ad_record_source():
    with st.expander("입원기록지", expanded=True):
        display_report(st.session_state.get("mr_json"))

    return "op-record-source"


AD_00_STYLE_0 = """
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
AD_01_HEADER_3 = """
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### 입원기록지 ( Addmission Note )
Date of Admission: {}

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="나의병원들" width="120">  
</td>
</tr>
</table>

"""

AD_02_SUBJECTIVE_4 = """
#### Chief Complaints:  
```
{}  
```
#### Pain:  
```
{}  
```
#### Onset:  
```
{}  
```
#### Present Illness:  
```
{}
```"""

AD_03_NICU_HISTORY_2 = """
#### Maternal History:
```{}```

#### Neonatal History:
```{}
```"""

AD_03_OBGY_HISTORY_3 = """
#### Obsteric History:
```{}
```
#### Obsteric History:
```{}
```
#### Admission/Operation History:
```{}
```"""

AD_03_HISTORY_3 = """
#### Past History:
```{}
```
#### Social History:
```{}
```
#### Family History:
```{}
```"""


AD_04_OBJECTIVE_2 = """

#### Review of Systems:
```{}
```
#### Physical Examination:   
```{}
```"""

AD_05_ASSESSMENT_1 = """

#### Impression:
```{}
```"""

AD_06_PLAN_3 = """

#### Plan:   
- **치료계획**: `{}`
- **퇴원계획**: `{}`
- **환자교육**: `{} `
"""

AD_07_TAIL_3 = """
<table width="100%">
<tr>
<td width="70%">
</td>
<td width="30%">
<b>Staff's Signatures</b>: {}   
</td>
</tr>
</table>

---

**작성일시**: {} {}
"""

def display_report(mr_instance, param="0"):
    if mr_instance is None:
        st.write("의무기록이 없습니다.")
        return

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(AD_00_STYLE_0, unsafe_allow_html=True)

    st.write(AD_01_HEADER_3.format(
        mr_instance["patient"]["patient id"], 
        mr_instance["clinical staff"]["department"], 
        mr_instance["patient"]["date of admission"]), unsafe_allow_html = True)

    st.write(AD_02_SUBJECTIVE_4.format(
        base.ifnull(mr_instance["subjective"]["chief complaints"], "<na>"), 
        base.ifnull(mr_instance["subjective"]["pain"], "<na>"),
        base.ifnull(mr_instance["subjective"]["onset"], "<na>"),
        base.ifnull(mr_instance["subjective"]["present illness"], "<na>")), unsafe_allow_html = True)

    if mr_instance["clinical staff"]["department"] == "GY":
        st.write(AD_03_OBGY_HISTORY_3.format(
            base.ifnull(mr_instance["subjective"]["obsteric gpal"], "<na>"),
            base.ifnull(mr_instance["subjective"]["menstrual history"], "<na>"),
            base.ifnull(mr_instance["subjective"]["admission-operation history"], "<na>")), unsafe_allow_html = True)

    st.write(AD_03_HISTORY_3.format(
        base.ifnull(mr_instance["subjective"]["past medical history"], "<na>"),
        base.ifnull(mr_instance["subjective"]["social history"], "<na>"),
        base.ifnull(mr_instance["subjective"]["family history"], "<na>")), unsafe_allow_html = True)

    st.write(AD_04_OBJECTIVE_2.format(
        base.ifnull(mr_instance["objective"]["review of systems"], "<na>"),
        base.ifnull(mr_instance["objective"]["other review of systems"], "")), unsafe_allow_html = True)

    cols = st.columns([1,4])
    with cols[0]:
        st.radio("특이사항 유무", ["유", "무"], key=f"abnormality_ad", index=1, horizontal=True, label_visibility="collapsed")
    with cols[1]:
        st.text_input("특이사항", value="", key=f"abnormality_text_ad", label_visibility= "collapsed")

    st.write(AD_05_ASSESSMENT_1.format(
        base.ifnull(mr_instance["assessment"]["impression"], "<na>")), unsafe_allow_html = True)

    st.write(AD_06_PLAN_3.format(
        base.ifnull(mr_instance["plan"]["operation plan"], "<na>"), 
        base.ifnull(mr_instance["plan"]["treatment plan"], ""), 
        base.ifnull(mr_instance["plan"]["discharge plan"], ""), 
        base.ifnull(mr_instance["plan"]["educational plan"], "<na>")), unsafe_allow_html = True)
    
    pass
