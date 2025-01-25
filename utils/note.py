import utils.config as config
import utils.base as base
import utils.db as db
import utils.genai as genai

def run_sql(query_sql):
    return db.run_sql(query_sql)

def get_medical_note(query_name, patient_id, admsn_date):
    #admsn_date = admission_date.strftime("%Y%m%d")
    query = config.get_query(query_name)
    query = query.replace("$patient_id", patient_id).replace("$admsn_date", admsn_date)
    print(query_name , "=" , query)
    return run_sql(query)

def get_doctors_by_dept():
    query_name = "query_DOCT"
    query = config.get_query(query_name)

    return run_sql(query)

def get_patient_by_doctor(spth):
    query_name = "query_PTNT"
    query = config.get_query(query_name)
    query = query.replace("$spth", spth)
    return run_sql(query)

def collect_or_source(patient_id, admsn_date):
    df_ae = get_medical_note("query_AE_P", patient_id, admsn_date)
    df_ay = get_medical_note("query_AY_P", patient_id, admsn_date)
    df_or = get_medical_note("query_OR_P", patient_id, admsn_date)
    df_pn = get_medical_note("query_PN_P", patient_id, admsn_date)

    decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    df_pn = df_pn.map(decode_rtf)

    or_info = {
        "ae":df_ae.to_dict(orient="records"), 
        "ay":df_ay.to_dict(orient="records"), 
        "or":df_or.to_dict(orient="records"), 
        "pn":df_pn.to_dict(orient="records"),
        }

    return or_info

def collect_rt_source(patient_id, admsn_date):
    df_ae = get_medical_note("query_AE_P", patient_id, admsn_date)
    df_ay = get_medical_note("query_AY_P", patient_id, admsn_date)
    df_or = get_medical_note("query_OR_P", patient_id, admsn_date)
    df_pn = get_medical_note("query_PN_P", patient_id, admsn_date)
    df_rt = get_medical_note("query_RT_P", patient_id, admsn_date)

    decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    df_pn = df_pn.map(decode_rtf)

    rt_info = {
        "ae":df_ae.to_dict(orient="records"), 
        "ay":df_ay.to_dict(orient="records"), 
        "or":df_or.to_dict(orient="records"), 
        "pn":df_pn.to_dict(orient="records"), 
        "rt":df_rt.to_dict(orient="records")
        }

    return rt_info

def call_api(prompt, data):
    print("prompt: " + prompt)
    print("data: " + data)
    reponses = genai.generate([prompt, data])
    return reponses
