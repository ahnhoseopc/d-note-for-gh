import streamlit as st
import pandas

import oracledb
import sqlalchemy

def get_sql_engine():
    HOST = st.secrets["GHDB_HOST"]
    PORT = st.secrets["GHDB_PORT"]
    USER = st.secrets["GHDB_USER"]
    PASS = st.secrets["GHDB_PASS"]

    con = oracledb.connect(user=USER, password=PASS, host=HOST, port=PORT)
    engine = sqlalchemy.create_engine("oracle+oracledb://", creator= lambda : con)
    return engine

import toml
from pathlib import Path

def save_query(query_name, query):
    config_path = Path(".streamlit", "config.toml")
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        config_data["database"][query_name] = query

    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config_data, f)

def get_query(query_name):
    config_path = Path(".streamlit", "config.toml")
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = toml.load(f)
        return config_data["database"][query_name]

st.markdown("<style>.stTextArea>div>div>textarea { font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

query_name = "query_15"
sql_rtn = st.text_area("SQL", value=get_query(query_name),height=400)
df_rtn = None

col1, col2, col3 = st.columns([20,2,2])

with col1:
    query_name = st.text_input("Query Name", value=query_name, key="query_name", label_visibility = "collapsed")

with col2:
    if st.button("Run Query"):
        engine = get_sql_engine()
        df_rtn = pandas.read_sql(sql_rtn, engine)

with col3:
    if st.button("Save Query"):
        save_query(query_name, sql_rtn)


if df_rtn is not None:
    st.dataframe(df_rtn)
