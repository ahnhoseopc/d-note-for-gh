import oracledb
import sqlalchemy
import pandas

import streamlit as st
HOST = st.secrets["GHDB_HOST"]
PORT = st.secrets["GHDB_PORT"]
USER = st.secrets["GHDB_USER"]
PASS = st.secrets["GHDB_PASS"]

def get_sql_engine():
    con = oracledb.connect(user=USER, password=PASS, host=HOST, port=PORT)
    engine = sqlalchemy.create_engine("oracle+oracledb://", creator= lambda : con)
    return engine

def run_sql(query_sql):
    engine = get_sql_engine()
    df_query = pandas.read_sql(query_sql, engine)
    return df_query
