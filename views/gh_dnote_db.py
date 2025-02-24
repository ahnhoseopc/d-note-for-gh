import streamlit as st

def db_record_source():
    with st.expander("소스 의료정보 (API입력데이터)", expanded=False):
        if st.session_state.get("mr_json"):
            st.json(st.session_state["mr_json"], expanded=1)
        else:
            st.write("의무기록이 없습니다.")
            return

        # Source data display
        if st.session_state.get("mr_info"):
            st.write("입원기록지")
            st.json(st.session_state["mr_info"]["ae"], expanded=1)
            st.write("입원기록지 GY")
            st.json(st.session_state["mr_info"]["ay"], expanded=1)
            st.write("상병")
            st.json(st.session_state["mr_info"]["il"], expanded=1)
            st.write("수술예약")
            st.json(st.session_state["mr_info"]["oy"], expanded=1)

            st.write("수술기록지")
            st.json(st.session_state["mr_info"]["or"], expanded=1)    

            st.write("경과기록지")
            st.json(st.session_state["mr_info"]["pn"], expanded=1)

            st.write("검사결과")
            st.json(st.session_state["mr_info"]["je"], expanded=1)
            st.json(st.session_state["mr_info"]["te"], expanded=1)
            st.json(st.session_state["mr_info"]["ce"], expanded=1)
            st.json(st.session_state["mr_info"]["yt"], expanded=1)

            st.write("프로토콜")
            st.json(st.session_state["mr_info"]["pt_o"], expanded=1)
            st.json(st.session_state["mr_info"]["pt_r"], expanded=1)
            
    return
