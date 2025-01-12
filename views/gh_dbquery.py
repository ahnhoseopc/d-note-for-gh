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

config_path = Path(".streamlit", "config.toml") 
with open(config_path, "r", encoding="utf-8") as f:
    config_data = toml.load(f)
    sql_rtn = config_data["database"]["query_15"]

engine = get_sql_engine()

df_rtn = pandas.read_sql(sql_rtn, engine)

st.text_area("SQL", value=sql_rtn,height=400)
st.dataframe(df_rtn)
