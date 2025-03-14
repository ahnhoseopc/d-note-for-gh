from utils import config
import utils.base as base
import utils.cdgen as cdgen
import json
import re

import streamlit as st

def cd_record_source():
    with st.expander("상병정보", expanded=False):
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
<img src="{}" alt="좋은병원들" width="120">  
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
        mr_instance["patient"]["date of admission"],
        config.get_option("customer.logo_url")), unsafe_allow_html = True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 상병코드  ")
    with col2:
        with st.popover("AI추천 상병코드", icon=":material/microbiology:" ,disabled=cd_json==None, use_container_width=True):
            #❌❎✖️💛⭐
            if cd_json:
                for cd in cd_json:
                    with st.container(border=True):
                        st.markdown(f"###### {cd["description"]}")
                        # len_cdsub = len(cd["subCodes"])
                        len_maxcd = 4
                        cols_cdsub = st.columns(len_maxcd)
                        for i,cdsub in enumerate(cd["subCodes"]):
                            with cols_cdsub[i%len_maxcd]:
                                if st.button(("⭐" if i==0 else "") + cdsub["code"], key="sub_"+cd["code"] + "_" + cdsub["code"], help=f"({cdsub["relevance_score"]}) {cdsub["description"]}", use_container_width=True):
                                    print(cdsub["code"] , [cd["code"] for cd in st.session_state.cd_list])
                                    if cdsub["code"] not in [cd["code"] for cd in st.session_state.cd_list]:
                                        st.session_state.cd_list.append(cdsub)
                                    pass
                                pass
                            pass
                        pass
                    pass
                pass
            pass
            with st.container(border=True):
                cdman = st.text_input("질병분류 기호", key="aa"+param, help="질병 분류기호와 설명을 입력하세요.")
                if st.button("수기입력", key="cd_input_"+param):
                    if cdman:
                        cdsub = {"code": cdman.split()[0], "description": " ".join(cdman.split()[1:]), "relevance_score":0}
                        if cdsub["code"] not in [cd["code"] for cd in st.session_state.cd_list]:
                            st.session_state.cd_list.append(cdsub)
                        pass
                    pass
                pass
            pass
        pass
    pass

    if cd_json:
        st.markdown("**선택 상병코드**")
        with st.container(border=True):
            for cd in st.session_state.cd_list:
                if st.button(f"**{cd["code"]}** {cd["description"]} ❎", key=cd["code"]):
                    st.session_state.cd_list.remove(cd)
                    st.rerun()
                pass
            pass
        st.markdown("**참조 상병코드**")
    else:
        st.markdown("**기존 상병코드**")
    pass

    with st.container(border=True):
        for cd in st.session_state["mr_info"]["il"]:
            for key in cd.keys():
                if key.startswith("icd0") and len(cd[key].strip()) > 0:
                    st.caption(f"{cd[key]}")
                pass
            pass
        pass

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
        mr_instance["patient"]["date of admission"],
        config.get_option("customer.logo_url")), unsafe_allow_html = True)

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
