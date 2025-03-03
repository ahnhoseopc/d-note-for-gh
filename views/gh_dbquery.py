import utils.auth as auth
import utils.base as base
import utils.config as config
import utils.db as db

import streamlit as st

def on_change_query_name():
    if "query_name" in st.session_state:
        st.session_state.query_sql = config.get_query(st.session_state.query_name)

@auth.login_required
def main():
    #
    # Text Area의 코드를 Courier New 로 설정하기
    # 
    st.markdown("<style>.stTextArea>div>div>textarea { font-family: 'Courier New'; font-size: 14px; }</style>", unsafe_allow_html=True)

    if "query_sql" not in st.session_state:
        query_list = config.get_query_list()
        query_sql = config.get_query(query_list[0])
        st.session_state.query_list = query_list
        st.session_state.query_sql = query_sql
        st.session_state.query_name = query_list[0]

    col_select_name, col_del, col_new_name, col_new, col_save, col_run = st.columns([8,2,4,2,2,2])

    with col_del:
        if st.button("Delete", use_container_width=True):
            query_name = st.session_state.query_name
            config.delete_query(query_name)
            st.session_state.query_list.remove(query_name)
            st.session_state.query_name = st.session_state.query_list[0]
            st.session_state.query_sql = config.get_query(st.session_state.query_name)

    with col_new:
        if st.button("New", use_container_width=True) and st.session_state.new_query_name:
            st.session_state.query_sql = "-- COPIED FROM PREVIOUS QUERY\n" + st.session_state.query_sql
            config.save_query(st.session_state.new_query_name, st.session_state.query_sql)
            st.session_state.query_list += [st.session_state.new_query_name]
            st.session_state.query_name = st.session_state.new_query_name
            st.session_state.new_query_name = ""

    with col_select_name:
        query_name = st.selectbox("Query Name", options=st.session_state.query_list, format_func=lambda x: x.upper(), key="query_name", on_change=on_change_query_name, label_visibility="collapsed")

    with col_new_name:
        st.text_input("New Query Name", key="new_query_name",label_visibility="collapsed")

    with col_save:
        if st.button("Save", use_container_width=True):
            config.save_query(query_name, st.session_state.sql_rtn)

    with col_run:
        if st.button("Run", use_container_width=True):
            st.session_state.df_rtn = db.run_sql(st.session_state.sql_rtn)

    # SQL
    st.text_area("SQL", value=st.session_state.query_sql, key="sql_rtn", height=400)

    #
    # 결과 데이터프레임 - 건별 데이터
    #
    if "df_rtn" in st.session_state and st.session_state.df_rtn is not None:
        col1, col2 = st.columns([2,2])
        with col1:
            selected_row= st.dataframe(st.session_state.df_rtn, on_select="rerun", selection_mode="single-row", key="selected_row")

        with col2:
            if selected_row and len(selected_row["selection"]["rows"]) > 0:
                rownum = selected_row["selection"]["rows"][0]
                dict = st.session_state.df_rtn.iloc[rownum]

                decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
                dict = dict.map(decode_rtf)

                json_str = dict.to_json(orient="index")
                st.json(json_str)

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
