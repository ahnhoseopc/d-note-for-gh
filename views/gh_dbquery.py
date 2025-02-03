import utils.auth as auth
import utils.base as base
import utils.config as config
import utils.db as db

import streamlit as st

def new_query():
    st.session_state.query_name = "query_" + base.get_random_string(4)
    st.session_state.query_sql = ""
    st.experimental_rerun() # Force a re-render to update the selectbox

def on_change_query_name():
    if "query_name" in st.session_state:
        st.session_state.query_sql = config.get_query(st.session_state.query_name)

@auth.login_required
def main():
    st.markdown("<style>.stTextArea>div>div>textarea { font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

    if "query_sql" not in st.session_state:
        query_list = config.get_query_list()
        query_sql = config.get_query(query_list[0])
        st.session_state.query_list = query_list
        st.session_state.query_sql = query_sql

    sql_rtn = st.text_area("SQL", key="query_sql", height=400)
    df_rtn = None

    col1, col2, col3, col4 = st.columns([16,2,2,2])

    with col1:
        query_name = st.selectbox("Query Name", options=st.session_state.query_list, key="query_name", on_change=on_change_query_name, label_visibility="collapsed")

    with col2:
        if st.button("New Query"):
            new_query()

    with col3:
        if st.button("Save Query"):
            config.save_query(query_name, sql_rtn)

    with col4:
        if st.button("Run Query"):
            st.session_state.df_rtn = db.run_sql(sql_rtn)

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
