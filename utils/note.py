import utils.config as config
import utils.base as base
import utils.db as db
import utils.genai as genai

def run_sql(query_sql):
    df_query = db.run_sql(query_sql)
    return df_query

def call_db(query_name, patient_id, admsn_date):
    #admsn_date = admission_date.strftime("%Y%m%d")
    query = config.get_query(query_name)
    query = query.replace("$patient_id", patient_id)
    query = query.replace("$admsn_date", admsn_date)

    print(query)
    result = run_sql(query)
    return result

def call_api(prompt, data):
    # Replace this with your actual API call
    # For demonstration purposes, we'll just return a random string
    reponses = genai.generate([prompt, data])
    result = base.get_random_string(100)
    return reponses

def collect_op_info(prompt, patient_id, admsn_date):
    df_ae = call_db("query_AE_P", patient_id, admsn_date)
    df_or = call_db("query_OR_P", patient_id, admsn_date)
    df_pn = call_db("query_PN_P", patient_id, admsn_date)

    decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    df_pn = df_pn.map(decode_rtf)

    return df_ae, df_or, df_pn

def collect_rt_info(prompt, patient_id, admsn_date):
    df_ae = call_db("query_AE_P", patient_id, admsn_date)
    df_ay = call_db("query_AY_P", patient_id, admsn_date)
    df_or = call_db("query_OR_P", patient_id, admsn_date)
    df_pn = call_db("query_PN_P", patient_id, admsn_date)
    df_rt = call_db("query_RT_P", patient_id, admsn_date)

    decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    df_pn = df_pn.map(decode_rtf)

    return df_ae, df_ay, df_or, df_pn, df_rt
