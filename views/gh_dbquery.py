import utils.base as base
import utils.config as config
import utils.db as db

import streamlit as st

def new_query():
    st.session_state.query_name = "query_" + base.get_random_string(4)
    st.session_state.query_sql = ""
    st.experimental_rerun() # Force a re-render to update the selectbox

def on_change_query_name():
    st.session_state.query_sql = config.get_query(st.session_state.query_name)

st.markdown("<style>.stTextArea>div>div>textarea { font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

if "query_sql" not in st.session_state:
    query_list = config.get_query_list()
    query_sql = config.get_query("query_01")
    st.session_state.query_list = query_list

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
        df_rtn = db.run_sql(sql_rtn)

st.write(st.session_state.query_list)
st.write(st.session_state.query_name)

if df_rtn is not None:
    st.dataframe(df_rtn)
