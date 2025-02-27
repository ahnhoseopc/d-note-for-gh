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

TS_01_HEADER_5 = """
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**입 원 일**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### {}
Date of Result: {}

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="좋은병원들" width="120">  
</td>
</tr>
</table>

---
"""


def display_report(mr_instance):
    if mr_instance is None:
        st.write("의무기록이 없습니다.")
        return

    if not mr_instance or not mr_instance.get("objective") or not mr_instance["objective"].get("lab-result"):
        st.write("검사기록이 없습니다.")
        return

    lab_result = mr_instance.get("objective").get("lab-result")

    options = [lab for lab in lab_result.keys() if len(lab_result[lab])>0]

    if len(options) == 0:
        st.write("검사기록이 없습니다.")
        return

    if len(options) == 1:
        lab = options[0]
        st.write(f"검사종류: {lab}")
        # lab = st.select_slider("검사종류", options=options, value=options[0], disabled=True)
    else:
        lab = st.select_slider("검사종류", options=options)

    lab_name = {
        "biopsy test":"병리검사",
        "cytology test":"세포검사",
        "diagnostic test":"진단검사",
        "vital signs":"바이탈",
        "video reading":"영상판독",
    }

    # CSS를 이용하여 테이블의 테두리 제거
    st.markdown(TS_00_STYLE_0, unsafe_allow_html=True)

    st.write(TS_01_HEADER_5.format(
        mr_instance["patient"]["patient id"], 
        mr_instance["patient"]["date of admission"],        
        mr_instance["clinical staff"]["department"], 
        lab_name[lab],
        lab_result[lab][0]["result date"] if "result date" in lab_result[lab][0].keys() 
        else lab_result[lab][0]["result date"]), unsafe_allow_html = True)

    for result in lab_result[lab]:
        if lab == "biopsy test":
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Order Date")
                st.code(result["order date"])
            with cols[1]:
                st.markdown("#### Result Date")
                st.code(result["result date"])

            cols = st.columns(2)
            with cols[1]:
                st.markdown("#### Test Result")
                st.code(result["test result"])
            with cols[1]:
                st.markdown("#### Comments")
                st.code(result["test note"])

            st.divider()

        if lab == "cytology test":
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Order Date")
                st.code(result["order date"])
            with cols[1]:
                st.markdown("#### Result Date")
                st.code(result["result date"])

            st.markdown("#### Test Result")
            st.code(result["test result"])

            st.divider()

        if lab == "diagnostic test":
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Order Date")
                st.code(result["order date"])
            with cols[1]:
                st.markdown("#### Result Date")
                st.code(result["result date"])

            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Test Code")
                st.code(result["test code"])
            with cols[1]:
                st.markdown("#### Test Name")
                st.code(result["test name"])

            cols = st.columns(2)
            with cols[1]:
                st.markdown("#### Test Result")
                st.code(result["test result"])

            with cols[1]:
                st.markdown("#### Upper Limit")
                st.code(result["test upper limit"])
                st.markdown("#### Lower Limit")
                st.code(result["test lower limit"])

                st.markdown("#### Test Unit")
                st.code(result["test unit"])

            st.divider()

        if lab == "vital signs":
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Result Date")
                st.code(result["result date"])
            with cols[1]:
                st.markdown("#### Result Time")
                st.code(result["result time"])

            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Temperature")
                st.code(result["temperature"])

            with cols[1]:
                st.markdown("#### Pulse")
                st.code(result["pulse"])
                st.markdown("#### Heart Rate")
                st.code(result["heart rate"])
                st.markdown("#### Respiratory Rate")
                st.code(result["respiratory rate"])

            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Systolic Blood Pressure")
                st.code(result["systolic blood pressure"])
            with cols[1]:
                st.markdown("#### Diastolic Blood Pressure")
                st.code(result["diastolic blood pressure"])

            st.divider()

        if lab == "video reading":
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### Order Date")
                st.code(result["order date"])
            with cols[1]:
                st.markdown("#### Result Date")
                st.code(result["result date"])

            st.markdown("#### Findings")
            st.code(result["findings"])
            st.markdown("#### Impression")
            st.code(result["impression"])

            st.divider()

    pass
