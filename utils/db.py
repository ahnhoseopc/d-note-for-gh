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

import os
#CLNT = r"D:\UTIL\DK\instantclient_12_1"
CLNT = r"D:\UTIL\DK\instantclient_11_2"
#CLNT = r"D:\UTIL\DK\instantclient_10_2"
CLNT = r"C:\oracle\instantclient_23_6"

os.environ["ORACLE_HOME"] = CLNT
os.environ["PATH"] = CLNT + ";" + os.environ["PATH"]
os.environ["NLS_CHARACTERSET"]="KO16MSWIN949"
#os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

try:
    if "oracle" not in st.session_state:
        ora.init_oracle_client(lib_dir=CLNT)
        st.session_state["oracle"] = True
except:
    pass

def get_sql_engine():
    DSN = ora.makedsn(host=HOST,port=PORT,service_name=SVCN)
    #print(DSN) # (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.1.1.71)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=JAINOCS)))
    con = ora.connect(user=USER, password=PASS, dsn=DSN)
    #print(con.version) # 10.2.0.4.0
    engine = sqlalchemy.create_engine("oracle+cx_oracle://", creator= lambda : con)
    #engine = sqlalchemy.create_engine("oracle+oracledb://", creator= lambda : con)
    return engine

def run_sql(query_sql):
    engine = get_sql_engine()
    df_query = pandas.read_sql(query_sql, engine)
    return df_query

#print("CLNT : " + CLNT)

# df = run_sql("""
# SELECT
# SAP07STATUS -- STATUS
# , SAP07IDNOA -- 환자번호
# , SAP07IDNOB -- 타급종구분
# , SAP07LWDAT -- 래원일
# , SAP07IOCD -- 입외구분
# , SAP07ODRDAT -- 오더일
# , SAP07ODRNO -- 오더번호
# , SAP07SLPNO -- 전표번호
# , SAP07PTLGNO -- 미사용
# , SAP07RSTDAT -- 검사완료일
# , SAP07RSTTIM -- 검사완료시간
# , SAP07INTP -- Cytologic Interpretation
# , SAP07RCMT -- Recommendation
# , SAP07SPTH -- 판독의
# , SAP07DOCCD -- 예비판독의
# , SAP07SPMNO -- 샘플번호
# , SAP07RSTYN -- 결과유무
# , SAP07SNDYN -- 사인유뮤
# , SAP07SUBNO --
# FROM JAIN_OCS.SAPCYT07
# WHERE ROWNUM < 10
#              """)

# print(df)



