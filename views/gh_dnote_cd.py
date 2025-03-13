import streamlit as st

def cd_record_source():
    with st.expander("상병정보", expanded=True):
        display_report(st.session_state.get("mr_json"))

    return "op-record-source"

CD_00_STYLE_0 = """<style>
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

CD_01_HEADER_3 = """<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### 상병정보 ( Illness Note )
Date of Admission: {}

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="좋은병원들" width="120">  
</td>
</tr>
</table>
"""

def display_report(mr_instance, param="0"):
    if mr_instance is None:
        st.write("의무기록이 없습니다.")
        return

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(CD_00_STYLE_0, unsafe_allow_html=True)
    
    st.markdown(CD_01_HEADER_3.format(
        mr_instance["patient"]["patient id"], 
        mr_instance["clinical staff"]["department"], 
        mr_instance["patient"]["date of admission"]), unsafe_allow_html = True)

    st.markdown("##### 상병코드  ")
    cd = st.session_state["mr_info"]["il"]
    for cd in st.session_state["mr_info"]["il"]:
        for key in cd.keys():
            if key.startswith("icd0") and len(cd[key].strip()) > 0:
                st.caption(f"{key}: {cd[key]}")

    st.text_area("주호소", value=mr_instance["subjective"]["chief complaints"], height=100, key="cc")
    st.text_area("현증상", value=mr_instance["subjective"]["present illness"], height=100, key="pi")
    st.text_area("소견", value=mr_instance["assessment"]["impression"], height=100, key="imp")
    
    pass
