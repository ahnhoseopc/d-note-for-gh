import utils.auth as auth
import views.gh_dnote_00 as intro
import views.gh_dnote_cd as cd
import views.gh_dnote_ad as ad
import views.gh_dnote_pn as pn
import views.gh_dnote_ts as ts
import views.gh_dnote_op as op
import views.gh_dnote_rt as rt
import views.gh_dnote_db as db

import forms.sidebar as sidebar
import forms.sidebar_note as sidebar_note

import streamlit as st

@auth.login_required
def main():
    # Side bar for chat history
    sidebar_note.display()

    #
    # Page title for D-Note
    #
    st.title("D-Note, 의무기록 자동화 Agent")

    tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["의무기록 자동화 Agent", "상병정보", "입원기록지", "***수술기록지**", "경과기록지", "검사기록", "***퇴원요약지**", "(의무기록DB)"])

    with tab0:
        intro.intro_record_source()

    with tab1:
        cd.cd_record_source()

    # 입원기록지
    with tab2:
        ad.ad_record_source()

    # 수술기록지
    with tab3:
        # Retrieving Source and Generate Target
        op.op_record_source()        
        op.op_record_target()

    with tab4:
        pn.pn_record_source()

    with tab5:
        ts.ts_record_source()

    # 퇴원요약지
    with tab6:
        # Retrieving Source and Generate Target
        # col1, col2 = st.columns([5, 5])

        rt.rt_summary_source()
        rt.rt_summary_target()
        
    with tab7:
        db.db_record_source()

    st.divider()

    cols = st.columns(7)
    with cols[3]:
        st.image("assets/gh/gh_doctor.png", width=300)

if __name__ == "__page__":
    main()
    sidebar.display()
