import utils.base as base
import utils.cdgen as cdgen
import json
import re

import streamlit as st

def cd_record_source():
    with st.expander("상병정보", expanded=True):
        mr_json = st.session_state.get("mr_json")
        display_report(mr_json)

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

def cd_record_target():
    cd_write = st.button("➡️ 상병코드 제안", key="cd-write", use_container_width=True, disabled=not st.session_state.get("mr_json"))

    mr_json = st.session_state.get("mr_json")

    if cd_write:
        query = "Chief Complaints: " + mr_json["subjective"]["chief complaints"] + "\n\nPresent Illness: " + mr_json["subjective"]["present illness"] + "\n\nImpression: " + mr_json["assessment"]["impression"]
        
        with st.expander("AI 결과", expanded=False):
            response_container = st.empty()
            try:
                result_json = cdgen.generate(query)
                response_container.json(result_json)
                st.session_state.cd_json = result_json
                st.session_state.cd_list = []
                pass
            except Exception as e:
                response_container.caption(f"error when calling api: {e}")
                pass
            pass

        # cols = st.columns(2)
        # with cols[0]:
        #     display_report(mr_json, None, "o1")
        # with cols[1]:
        # display_report(mr_json, result_json, "n2")
        
        pass
    pass

    cd_json = st.session_state.get("cd_json")
    if cd_json:
        display_report(mr_json, cd_json, "n2")

def display_report(mr_instance, cd_json=None, param="0"):
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
    if cd_json:
        cols = st.columns(2)
#❌❎✖️💛⭐
        with cols[1]:
            for cd in cd_json:
                with st.container():
                    st.markdown(f"#### {cd["description"]}")
                    len_cdsub = len(cd["subCodes"])
                    cols_cdsub = st.columns(len_cdsub)
                    for i,cdsub in enumerate(cd["subCodes"]):
                        with cols_cdsub[i]:
                            if st.button(("⭐" if i==0 else "") + cdsub["code"], key="sub_"+cdsub["code"], help=f"({cdsub["relevance_score"]}) {cdsub["description"]}"):
                                st.session_state.cd_list.append(cdsub)
                                pass

        with cols[0]:
            for cd in st.session_state.cd_list:
                cols_cd = st.columns([2,8,1])
                with cols_cd[2]:
                    if st.button("❎", key=cd["code"]):
                        st.session_state.cd_list.remove(cd)
                        pass
                    pass
                with cols_cd[0]:
                    st.caption(cd["code"])
                with cols_cd[1]:
                    st.caption(cd["description"])
            pass

    else:
        for cd in st.session_state["mr_info"]["il"]:
            for key in cd.keys():
                if key.startswith("icd0") and len(cd[key].strip()) > 0:
                    st.caption(f"{cd[key]}")

    st.text_area("주호소", value=mr_instance["subjective"]["chief complaints"], height=100, key="cc"+param)
    st.text_area("현증상", value=mr_instance["subjective"]["present illness"], height=100, key="pi"+param)
    st.text_area("소견", value=mr_instance["assessment"]["impression"], height=100, key="imp"+param)
    
def display_report_old(mr_instance, param="0"):
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
