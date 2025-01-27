import utils.config as config
import utils.base as base
import utils.db as db
import utils.genai as genai

def run_sql(query_sql):
    return db.run_sql(query_sql)

def get_medical_note(query_name, patient_id, admsn_date, kwa=None, spth=None):
    #admsn_date = admission_date.strftime("%Y%m%d")
    query = config.get_query(query_name)
    if patient_id is not None and admsn_date is not None:
        query = query.replace("$patient_id", patient_id).replace("$admsn_date", admsn_date)
    if kwa is not None and spth is not None:
        query = query.replace("$kwa", kwa).replace("$spth", spth)
    print(query_name , "=" , query)
    return run_sql(query)

def get_doctors_by_dept():
    query_name = "query_DOCT"
    query = config.get_query(query_name)

    return run_sql(query)

def get_patient_by_doctor(spth):
    query_name = "query_PTNT"
    query = config.get_query(query_name)
    query = query.replace("$spth", base.ifnull(spth,""))
    return run_sql(query)

#
# Operation Report (수술기록지)
#
def collect_or_source(patient_id, admsn_date, kwa, spth):
    df_ae = get_medical_note("query_AE_P", patient_id, admsn_date)
    df_ay = get_medical_note("query_AY_P", patient_id, admsn_date)
    df_pt = get_medical_note("query_PT_O", None, None, kwa, spth)

    decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    df_pt = df_pt.map(decode_rtf)

    df_or = get_medical_note("query_OR_P", patient_id, admsn_date)

    or_source = {
        "patient": {
            "patient id": patient_id,
            "date of admission": admsn_date,

            "sex": df_ae["ocm31sex"][0] if len(df_ae) > 0 else df_ay["ocm41sex"][0] if len(df_ay) > 0 else None,
            "age": df_ae["ocm31age"][0] if len(df_ae) > 0 else df_ay["ocm41age"][0] if len(df_ay) > 0 else None,
            },
        "clinical staff": {
            "department": df_ae["ocm31kwa"][0] if len(df_ae) > 0 else df_ay["ocm41kwa"][0] if len(df_ay) > 0 else None,
            "doctor in charge": df_ae["ocm31spth"][0] if len(df_ae) > 0 else df_ay["ocm41spth"][0] if len(df_ay) > 0 else None,
            "physician assistant": None,
            "nurse": None,
            "anesthesiologist": None,
            "method of anesthesia": None,
            },

        "subjective": {
            "chief complaints": df_ae["ocm31cc"][0] if len(df_ae) > 0 else df_ay["ocm41cc"][0] if len(df_ay) > 0 else None,
            "pain": df_ae["ocm31pain2"][0] if len(df_ae) > 0 else df_ay["ocm41pain2"][0] if len(df_ay) > 0 else None,
            "onset": df_ae["ocm31onset"][0] if len(df_ae) > 0 else df_ay["ocm41onset"][0] if len(df_ay) > 0 else None,

            "present illness": df_ae["ocm31pi"][0] if len(df_ae) > 0 else df_ay["ocm41pi"][0] if len(df_ay) > 0 else None,

            "obsteric gpal": None if len(df_ae) > 0 else base.ifnull(df_ay["ocm41ohg"][0],"<na>")+'/'+base.ifnull(df_ay["ocm41ohp"][0],"<na>")+'/'+base.ifnull(df_ay["ocm41oha"][0],"<na>")+'/'+base.ifnull(df_ay["ocm41ohl"][0],"<na>") if len(df_ay) > 0 else None,
            "menstrual history": None if len(df_ae) > 0 else base.ifnull(df_ay["ocm41lmp"][0],"<na>")+'/'+base.ifnull(df_ay["ocm41pmp"][0],"<na>")+'/'+base.ifnull(df_ay["ocm41interval"][0],"<na>")+'/'+base.ifnull(df_ay["ocm41menache"][0],"<na>") if len(df_ay) > 0 else None,

            "past medical history": df_ae["ocm31pmhx"][0] if len(df_ae) > 0 else df_ay["ocm41phx"][0] if len(df_ay) > 0 else None,
            "admission-operation history": None if len(df_ae) > 0 else df_ay["ocm41adm"][0] if len(df_ay) > 0 else None,

            "social history": df_ae["ocm31soc"][0] if len(df_ae) > 0 else df_ay["ocm41shx"][0] if len(df_ay) > 0 else None,
            "family history": df_ae["ocm31family"][0] if len(df_ae) > 0 else df_ay["ocm41fhx"][0] if len(df_ay) > 0 else None,
            },
        
        "objective": {
            "review of systems": None if len(df_ae) > 0 else df_ay["ocm41ros"][0] if len(df_ay) > 0 else None,
            "other review of systems": df_ae["ocm31rosother"][0] if len(df_ae) > 0 else df_ay["ocm41rosother"][0] if len(df_ay) > 0 else None,
            },

        "assessment": {
            "impression": df_ae["ocm31imp"][0] if len(df_ae) > 0 else df_ay["ocm41imp"][0] if len(df_ay) > 0 else None,
            "diagnosis": [None],
            },
        "plan": {
            "operation name": None,
            "plan": df_ae["ocm31plan"][0] if len(df_ae) > 0 else df_ay["ocm41planop"][0] if len(df_ay) > 0 else None,
            "discharge plan": df_ae["ocm31rtplan"][0] if len(df_ae) > 0 else df_ay["ocm41rtplan"][0] if len(df_ay) > 0 else None,
            "educational plan": df_ae["ocm31edu"][0] if len(df_ae) > 0 else df_ay["ocm41edct"][0] if len(df_ay) > 0 else None,
            },

        "report date": df_ae["ocm31sysdat"][0] if len(df_ae) > 0 else df_ay["ocm41sysdat"][0] if len(df_ay) > 0 else None,
        "report time": df_ae["ocm31systm"][0] if len(df_ae) > 0 else df_ay["ocm41systime"][0] if len(df_ay) > 0 else None,

        "protocols of doctor": df_pt.to_dict(orient="records")
    }

    or_current = {
        "patient": {
            "patient id": patient_id,
            "date of admission": admsn_date,
            },
        "clinical staff": {
            "department": df_or["ocm06kwa"][0] if len(df_or) > 0 else None,
            "doctor in charge": df_or["ocm06spth"][0] if len(df_or) > 0 else None,
            "doctor assistant": str(df_or["ocm06rgcd"][0]) if len(df_or) > 0 else None,
            },

        "operation data": df_or["ocm06cmta"][0].split('|') if len(df_or) > 0 else None,
        "operation procedures and findings": df_or["ocm06cmtb"][0] if len(df_or) > 0 else None,
        "operation notes": df_or["ocm06memo"][0] if len(df_or) > 0 else None,

        "additional data": {
            "alarm": df_or["ocm06alarm"][0] if len(df_or) > 0 else None,
            "cmplyn": df_or["cmplyn"][0] if len(df_or) > 0 else None,
            "emdv": df_or["ocm06emdv"][0] if len(df_or) > 0 else None,
            "pclr": df_or["ocm06pclr"][0] if len(df_or) > 0 else None,
            },
        "operation check": {
            "tissue examination": df_or["ocm06tissueexmn"][0] if len(df_or) > 0 else None,
            "tissue examination contents": df_or["ocm06tissueexmncnts"][0] if len(df_or) > 0 else None,
            "drain pipe": df_or["ocm06drngpipe"][0] if len(df_or) > 0 else None,
            "drain pipe contents": df_or["ocm06drngpipecnts"][0] if len(df_or) > 0 else None,
            },
 
        "operation date": df_or["ocm06opdat"][0] if len(df_or) > 0 else None,
        "operation start time": df_or["ocm06opstarttm"][0] if len(df_or) > 0 else None,
        "operation end time": df_or["ocm06opendtm"][0] if len(df_or) > 0 else None,
        "report date": df_or["ocm06sysdat"][0] if len(df_or) > 0 else None,
        "report time": df_or["ocm06systm"][0] if len(df_or) > 0 else None,

        "medical treatment plan": df_or["ocm06mdtrplan"][0] if len(df_or) > 0 else None,
        "operation progress": df_or["ocm06opprgr"][0] if len(df_or) > 0 else None,
    }

    or_info = {
        "ae":df_ae.to_dict(orient="records"), 
        "ay":df_ay.to_dict(orient="records"), 
        "pt":df_pt.to_dict(orient="records"), 
        "or":df_or.to_dict(orient="records"), 

        "or-source": or_source,
        "or-current": or_current
    }

    return or_info

#
# Discharge Summary Report (퇴원요약지)
#
def collect_rt_source(patient_id, admsn_date):
    df_ae = get_medical_note("query_AE_P", patient_id, admsn_date)
    df_ay = get_medical_note("query_AY_P", patient_id, admsn_date)
    df_or = get_medical_note("query_OR_P", patient_id, admsn_date)
    df_pn = get_medical_note("query_PN_P", patient_id, admsn_date)

    df_je = get_medical_note("query_JE_P", patient_id, admsn_date)
    df_te = get_medical_note("query_TE_P", patient_id, admsn_date)
    df_ce = get_medical_note("query_CE_P", patient_id, admsn_date)
    df_yt = get_medical_note("query_YT_P", patient_id, admsn_date)

    df_rt = get_medical_note("query_RT_P", patient_id, admsn_date)

    decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
    df_pn = df_pn.map(decode_rtf)

    rt_info = {
        "ae":df_ae.to_dict(orient="records"), 
        "ay":df_ay.to_dict(orient="records"), 
        "or":df_or.to_dict(orient="records"), 
        "pn":df_pn.to_dict(orient="records"), 

        "je":df_je.to_dict(orient="records"), 
        "te":df_te.to_dict(orient="records"), 
        "ce":df_ce.to_dict(orient="records"), 
        "yt":df_yt.to_dict(orient="records"), 

        "rt":df_rt.to_dict(orient="records")
        }

    return rt_info

def call_api(prompt, data):
    print("prompt: " + prompt)
    print("data: " + data)
    reponses = genai.generate([prompt, data])
    return reponses
