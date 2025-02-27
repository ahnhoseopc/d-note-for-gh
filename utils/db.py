#import oracledb as ora
import cx_Oracle as ora
import sqlalchemy
import pandas

import streamlit as st
HOST = st.secrets["GHDB_HOST"]
PORT = st.secrets["GHDB_PORT"]
SVCN = st.secrets["GHDB_SVCN"]
USER = st.secrets["GHDB_USER"]
PASS = st.secrets["GHDB_PASS"]

CLNT = st.secrets["ORACLE_CLNT_PATH"]

if CLNT == "":
    #CLNT = r"D:\UTIL\DK\instantclient_12_1"
    #CLNT = r"D:\UTIL\DK\instantclient_11_2"
    #CLNT = r"D:\UTIL\DK\instantclient_10_2"
    #CLNT = r"C:\oracle\instantclient_23_6"
    CLNT = r"C:/instantclient_23_6"

import os
if "ORACLE_HOME" not in os.environ:
    os.environ["ORACLE_HOME"] = CLNT
    os.environ["PATH"] = CLNT + ";" + os.environ["PATH"]

os.environ["NLS_CHARACTERSET"]="KO16MSWIN949"
#os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

try:
    if "oracle" not in st.session_state:
        ora.init_oracle_client(lib_dir=os.environ["ORACLE_HOME"])
        st.session_state["oracle"] = True
except:
    pass

def get_sql_engine():
    DSN = ora.makedsn(host=HOST,port=PORT,service_name=SVCN)
    #logging.info(DSN) # (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.1.1.71)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=JAINOCS)))
    con = ora.connect(user=USER, password=PASS, dsn=DSN)
    #logging.info(con.version) # 10.2.0.4.0
    engine = sqlalchemy.create_engine("oracle+cx_oracle://", creator= lambda : con)
    #engine = sqlalchemy.create_engine("oracle+oracledb://", creator= lambda : con)
    return engine

def run_sql(query_sql):
    engine = get_sql_engine()
    df_query = pandas.read_sql(query_sql, engine)
    return df_query
