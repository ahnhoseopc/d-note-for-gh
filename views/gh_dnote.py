import utils.auth as auth
import views.gh_dnote_op as op
import views.gh_dnote_rt as rt

import streamlit as st

@auth.login_required
def main():
    tab1, tab2 = st.tabs(["수술기록지", "퇴원요약지"])

    # 수술기록지
    with tab1:
        col1, col2 = st.columns([5, 5])
        
        # Retrieving Source and Generate Target
        with col1:
            op.op_record_source()        

        with col2:
            op.op_record_target()

        # Display Report
        col1, col2 = st.columns([5, 5])
        
        with col1:
            with st.expander("기존 수술기록지 (문서양식))", expanded=False):
                op.display_report(op.or_info["or-current"] if op.or_info and "or-current" in op.or_info else None)
    
        with col2:
            with st.expander("기존 수술기록지 (문서양식))", expanded=False):
                op.display_report(op.or_info["or-current"] if op.or_info and "or-current" in op.or_info else None)

    # 퇴원요약지
    with tab2:
        # Retrieving Source and Generate Target
        col1, col2 = st.columns([5, 5])

        with col1:
            rt.rt_summary_source()

        with col2:
            rt.rt_summary_target()

        # Display Report
        col1, col2 = st.columns([5, 5])

        with col1:
            #rt.rt_summary_source()
            pass

        with col2:
            #rt.rt_summary_target()
            pass

    cols = st.columns(7)
    with cols[3]:
        st.image("https://www.moonhwa.or.kr/moonhwa/images/main02/img_symbol0302.png", width=300)

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
