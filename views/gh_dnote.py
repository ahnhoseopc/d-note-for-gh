import utils.auth as auth
import views.gh_dnote_ad as ad
import views.gh_dnote_pn as pn
import views.gh_dnote_ts as ts
import views.gh_dnote_op as op
import views.gh_dnote_rt as rt
import views.gh_dnote_db as db
import forms.sidebar_note as sidebar_note

import streamlit as st

DNOTE_HELP = """의사분들에게 환자치료에 집중하여 Quality care를 제공하는게 DK의 목표입니다. 

이에 의사분들이 많은 시간을 투자하고 있는 다양한 의무기록지는 의료환경에서 반드시 필요한 서류지만, 

의료진에게 환자치료시간외에 별도의 시간을 투입해야하는 다소 불편한 작업이었습니다.

과거에는 전공의가 많은 부분에서 도움을 주었지만, 향후 의료진의 인력문제가 더욱 심화될 환경속에서 

의사분들에게 반복적이고 시간이 많이 소요되는 업무를 지원하는 

“의무기록지 초안 작성”은 많은 도움이 될거라 확신합니다.

특히 퇴원요약지, 경과기록지, 수술기록지와 같은 EMR의 여러 DATA를 참조하여 정리해야하는 작업일 경우 

AI의 기술은 많은 도움을 줄 수 있습니다.

다양한 병원환경에서 이미 검증된 D-Note는 의사분들에게 서류작업에서 자유로울 수 있는 시간을 드리고자 합니다. 
"""

@auth.login_required
def main():
    # Side bar for chat history
    sidebar_note.display()

    #
    # Page title for D-Note
    #
    st.title("D-Note, 의무기록 자동화 Agent", help=DNOTE_HELP)

    tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["의무기록 자동화 Agent", "입원기록지", "***수술기록지**", "경과기록지", "검사기록", "***퇴원요약지**", "(의무기록DB)"])

    with tab0:
        st.markdown(DNOTE_HELP)

    # 입원기록지
    with tab1:
        ad.ad_record_source()
    with tab3:
        pn.pn_record_source()
    with tab4:
        ts.ts_record_source()
    with tab6:
        db.db_record_source()

    # 수술기록지
    with tab2:
        # col1, col2 = st.columns([5, 5])
        
        # Retrieving Source and Generate Target
        op.op_record_source()        

        op.op_record_target()
        
        st.divider()

        # Display Report Comparison
        # col1, col2 = st.columns([5, 5])
        
        # with col1:
        #     with st.expander("기존 수술기록지 (문서양식))", expanded=False):
        #         op.display_report(op.or_info["or-current"] if op.or_info and "or-current" in op.or_info else None)
    
        # with col2:
        #     with st.expander("기존 수술기록지 (문서양식))", expanded=False):
        #         op.display_report(op.or_info["or-current"] if op.or_info and "or-current" in op.or_info else None)

    # 퇴원요약지
    with tab5:
        # Retrieving Source and Generate Target
        # col1, col2 = st.columns([5, 5])

        rt.rt_summary_source()

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
