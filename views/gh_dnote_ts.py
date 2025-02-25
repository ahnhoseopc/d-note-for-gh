import streamlit as st

def ts_record_source():
    with st.expander("검사기록", expanded=True):
        display_report(st.session_state.get("mr_json"))

    return "op-record-source"


TS_00_STYLE_0 = """
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

TS_01_HEADER_4 = """
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### {}
Date of Admission: {}

</td>
<td align="right" width="25%">
<img src="../assets/gh_logo.png" alt="좋은병원들" width="120">  
</td>
</tr>
</table>

"""


def display_report(mr_instance):
    if mr_instance is None:
        st.write("의무기록이 없습니다.")
        return

    if not mr_instance or not mr_instance.get("objective") or not mr_instance["objective"].get("lab-result"):
        st.write("검사기록이 없습니다.")
        return

    lab_result = mr_instance.get("objective").get("lab-result")

    options = [lab for lab in lab_result.keys() if len(lab)>0]

    lab = st.select_slider("검사종류",options=options)
    lab_name = {
        "biopsy test":"병리검사",
        "cytology test":"세포검사",
        "diagnostic test":"진단검사",
        "vital signs":"바이탈",
        "video reading":"영상판독",
    }

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(TS_00_STYLE_0, unsafe_allow_html=True)

    st.write(TS_01_HEADER_4.format(
        mr_instance["patient"]["patient id"], 
        mr_instance["clinical staff"]["department"], 
        lab_name[lab],
        mr_instance["patient"]["date of admission"]), unsafe_allow_html = True)

    for result in lab_result[lab]:
        if lab == "biopsy test":
            st.markdown("#### Order Date")
            st.caption(result["order date"])
            st.markdown("#### Result Date")
            st.caption(result["result date"])

            st.markdown("#### Test Result")
            st.caption(result["test result"])
            st.markdown("#### Comments")
            st.caption(result["test note"])

        if lab == "cytology test":
            st.markdown("#### Order Date")
            st.caption(result["order date"])
            st.markdown("#### Result Date")
            st.caption(result["result date"])

            st.markdown("#### Test Result")
            st.caption(result["test result"])

        if lab == "diagnostic test":
            st.markdown("#### Order Date")
            st.caption(result["order date"])
            st.markdown("#### Result Date")
            st.caption(result["result date"])

            st.markdown("#### Test Code")
            st.caption(result["test code"])
            st.markdown("#### Test Name")
            st.caption(result["test name"])

            st.markdown("#### Test Result")
            st.caption(result["test result"])

            st.markdown("#### Upper Limit")
            st.caption(result["test upper limit"])
            st.markdown("#### Lower Limit")
            st.caption(result["test lower limit"])

            st.markdown("#### Test Unit")
            st.caption(result["test unit"])

        if lab == "vital signs":
            st.markdown("#### Reading Date")
            st.caption(result["reading date"])
            st.markdown("#### Reading Time")
            st.caption(result["reading time"])

            st.markdown("#### Temperature")
            st.caption(result["temperature"])
            st.markdown("#### Pulse")
            st.caption(result["pulse"])

            st.markdown("#### Heart Rate")
            st.caption(result["heart rate"])
            st.markdown("#### Respiratory Rate")
            st.caption(result["respiratory rate"])

            st.markdown("#### Systolic Blood Pressure")
            st.caption(result["systolic blood pressure"])
            st.markdown("#### Diastolic Blood Pressure")
            st.caption(result["diastolic blood pressure"])

        if lab == "video reading":
            st.markdown("#### Order Date")
            st.caption(result["order date"])
            st.markdown("#### Reading Date")
            st.caption(result["reading date"])

            st.markdown("#### Findings")
            st.caption(result["findings"])
            st.markdown("#### Impression")
            st.caption(result["impression"])
    pass
