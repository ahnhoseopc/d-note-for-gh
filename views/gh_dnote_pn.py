import utils.base as base

import streamlit as st

def pn_record_source():
    with st.expander("경과기록", expanded=True):
        display_report(st.session_state.get("mr_json"))

    return "op-record-source"


PN_00_STYLE_0 = """
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
PN_01_HEADER_3 = """
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**입 원 일**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### 경과기록지 ( Progress Note )
Date of Note: {}

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="나의병원들" width="120">  
</td>
</tr>
</table>

---
"""

PN_02_NOTES_1= """
#### Progress Note:  

"""

PN_07_TAIL_2 = """
<table width="100%">
<tr>
<td width="70%">
</td>
<td width="30%">
<b></b>:
</td>
</tr>
</table>

---

**작성일시**: {} {} 2024-10-22 11:00  
"""

def display_report(mr_instance, param="0"):
    if mr_instance is None:
        st.write("의무기록이 없습니다.")
        return

    notes = mr_instance.get("progress notes")
    if notes is None or len(notes)==0:
        st.write("경과기록이 없습니다.")
        return

    options = [note["order date"] for note in notes]
    if len(options) == 0:
        st.write("경과기록이 없습니다.")
        return

    if len(options) == 1:
        order_date = options[0]
        st.write(f"기록일: {order_date}")
        # order_date = st.select_slider("기록일", options=options, value=options[0], disabled=True)
    else:
        order_date = st.select_slider(
            "기록일",
            options=options,
            # value=(notes[0]["order date"], notes[-1]["order date"]),
        )

    note = next((note for note in notes if note["order date"] == order_date), None)
    if note is None:
        st.write("경과기록이 없습니다.")
        return

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(PN_00_STYLE_0, unsafe_allow_html=True)

    st.markdown(PN_01_HEADER_3.format(
        mr_instance["patient"]["patient id"], 
        mr_instance["patient"]["date of admission"],
        mr_instance["clinical staff"]["department"], 
        note["order date"]), unsafe_allow_html = True)
    
    st.markdown(PN_02_NOTES_1, unsafe_allow_html = True)
        
    st.code(base.ifnull(note["order note"], ""))

    if note.get("report date"):
        st.markdown(PN_07_TAIL_2.format(
            base.ifnull(note["report date"], ""), 
            base.ifnull(note["report time"], "")), unsafe_allow_html = True)
    
    pass
