import utils.config as config
import utils.base as base
import utils.db as db
import utils.genai as genai
import utils.note_template as template

import streamlit as st

def run_sql(query_sql):
    return db.run_sql(query_sql)

def get_medical_data(query_name, patient_id, admsn_date, kwa=None, spth=None):
    #admsn_date = admission_date.strftime("%Y%m%d")
    query = config.get_query(query_name)
    if patient_id is not None and admsn_date is not None:
        query = query.replace("$patient_id", patient_id).replace("$admsn_date", admsn_date)
    if kwa is not None and spth is not None:
        query = query.replace("$kwa", kwa).replace("$spth", spth)
    print("query_name" , "=" , query_name)
    return run_sql(query)

@st.cache_data()
def get_doctors_by_dept():
    query_name = "query_DOCT"
    query = config.get_query(query_name)

    return run_sql(query)

@st.cache_data()
def get_patient_by_doctor(spth):
    query_name = "query_PTNT"
    query = config.get_query(query_name)
    query = query.replace("$spth", base.ifnull(spth,""))
    return run_sql(query)

#
# Lambda functions for data processing
#
# Protocols are in rtf format
decode_rtf = lambda x: base.decode_rtf(x) if type(x) == str and base.is_rtf_format(x) else x
# Discharge protocols are in the format of "Chief Complaints|Final Diagnosis|Secondary Diagnosis|Treatment Operation|Treatment Medical|Abnormal Findings and/or Lab Result|Follow-up Plan|Progress Summary"
split_keys = ["Chief Complaints","Final Diagnosis","Secondary Diagnosis","Treatment Operation","Treatment Medical","Abnormal Findings and/or Lab Result","Follow-up Plan","Progress Summary",]
split_protocol = lambda x: dict(zip(split_keys, x.split("|") if type(x) == str else x))

#
# Patient records from the database
#
def get_patient_mr_data(patient_id, admsn_date, dept, doctor):
    # 일반 입원기록
    df_ae = get_medical_data("query_AE_P", patient_id, admsn_date)
    # 산부인과 입원기록
    df_ay = get_medical_data("query_AY_P", patient_id, admsn_date)
    # 상병/진단 정보
    df_il = get_medical_data("query_IL_P", patient_id, admsn_date)
    # 수술예약 정보
    df_oy = get_medical_data("query_OY_P", patient_id, admsn_date)

    # 수술 기록 Operation Report
    df_or = get_medical_data("query_OR_P", patient_id, admsn_date)

    # 결과 기록 Progress notes
    df_pn = get_medical_data("query_PN_P", patient_id, admsn_date)
    df_pn = df_pn.map(decode_rtf)

    # 퇴원 요약 Discharge Summary
    df_rt = get_medical_data("query_RT_P", patient_id, admsn_date)

    # 수술 프로토콜 Operation Protocols of Doctor
    df_pt_o = get_medical_data("query_PT_O", None, None, dept, doctor)
    df_pt_o = df_pt_o.map(decode_rtf)

    # 퇴원요약 프로토콜 Discharge Protocols of Doctor
    df_pt_r = get_medical_data("query_PT_R", None, None, dept, doctor)
    df_pt_r["protocol"] = df_pt_r["protocol"].map(split_protocol)
    df_pt_r = df_pt_r.map(decode_rtf)

    # Lab results and other tests
    df_je = get_medical_data("query_JE_P", patient_id, admsn_date)
    df_te = get_medical_data("query_TE_P", patient_id, admsn_date)
    df_ce = get_medical_data("query_CE_P", patient_id, admsn_date)
    df_yt = get_medical_data("query_YT_P", patient_id, admsn_date)

    mr_info = {
        "ae":df_ae.to_dict(orient="records"), 
        "ay":df_ay.to_dict(orient="records"), 
        "il":df_il.to_dict(orient="records"), 
        "oy":df_oy.to_dict(orient="records"), 
        "or":df_or.to_dict(orient="records"), 
        "pn":df_pn.to_dict(orient="records"), 
        "rt":df_rt.to_dict(orient="records"), 

        "pt_o":df_pt_o.to_dict(orient="records"), 
        "pt_r":df_pt_r.to_dict(orient="records"), 

        "te":df_te.to_dict(orient="records"), 
        "ce":df_ce.to_dict(orient="records"), 
        "yt":df_yt.to_dict(orient="records"), 
        "je":df_je.to_dict(orient="records"), 
    }

    return mr_info

#
# Medical Record (진료기록)
#
def get_patient_mr_json(mr_info):
    mr = template.get_medical_record_template()

    # Admission Report
    mr["patient"]["patient id"] = mr_info["ae"][0]["ocm31idnoa"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41idnoa"] if len(mr_info["ay"]) > 0 else None
    mr["patient"]["date of admission"] = mr_info["ae"][0]["ocm31lwdat"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41lwdat"] if len(mr_info["ay"]) > 0 else None
    mr["patient"]["sex"] = mr_info["ae"][0]["ocm31sex"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41sex"] if len(mr_info["ay"]) > 0 else None
    mr["patient"]["age"] = mr_info["ae"][0]["ocm31age"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41age"] if len(mr_info["ay"]) > 0 else None

    mr["clinical staff"]["department"] = mr_info["ae"][0]["ocm31kwa"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41kwa"] if len(mr_info["ay"]) > 0 else None
    mr["clinical staff"]["doctor in charge"] = mr_info["ae"][0]["ocm31spth"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41spth"] if len(mr_info["ay"]) > 0 else None

    # Admission Report
    mr["subjective"]["chief complaints"] = mr_info["ae"][0]["ocm31cc"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41cc"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["pain"] = mr_info["ae"][0]["ocm31pain2"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41pain2"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["onset"] = mr_info["ae"][0]["ocm31onset"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41onset"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["present illness"] = mr_info["ae"][0]["ocm31pi"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41pi"] if len(mr_info["ay"]) > 0 else None

    mr["subjective"]["obsteric gpal"] = mr_info["ay"][0]["ocm41ohg"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["menstrual history"] = mr_info["ay"][0]["ocm41lmp"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["admission-operation history"] = mr_info["ay"][0]["ocm41adm"] if len(mr_info["ay"]) > 0 else None

    mr["subjective"]["past medical history"] = mr_info["ae"][0]["ocm31pmhx"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41phx"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["social history"] = mr_info["ae"][0]["ocm31soc"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41shx"] if len(mr_info["ay"]) > 0 else None
    mr["subjective"]["family history"] = mr_info["ae"][0]["ocm31family"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41fhx"] if len(mr_info["ay"]) > 0 else None

    mr["objective"]["review of systems"] = mr_info["ay"][0]["ocm41ros"] if len(mr_info["ay"]) > 0 else None
    mr["objective"]["other review of systems"] = mr_info["ae"][0]["ocm31rosother"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41rosother"] if len(mr_info["ay"]) > 0 else None

    mr["assessment"]["impression"] = mr_info["ae"][0]["ocm31imp"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41imp"] if len(mr_info["ay"]) > 0 else None

    mr["plan"]["treatment plan"] = mr_info["ae"][0]["ocm31plan"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41planop"] if len(mr_info["ay"]) > 0 else None
    mr["plan"]["discharge plan"] = mr_info["ae"][0]["ocm31rtplan"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41rtplan"] if len(mr_info["ay"]) > 0 else None
    mr["plan"]["educational plan"] = mr_info["ae"][0]["ocm31edu"] if len(mr_info["ae"]) > 0 else mr_info["ay"][0]["ocm41edct"] if len(mr_info["ay"]) > 0 else None


    # 상병/진단 정보
    mr["assessment"]["diagnosis"] = [mr_info["il"][0][icd] for icd in ["icd01","icd02","icd03","icd04","icd05"] if len(mr_info["il"][0][icd].strip()) > 0] if len(mr_info["il"]) > 0 else None
    # 수술예약 정보
    mr["plan"]["operation plan"] = mr_info["oy"][0]["operation_name"] if len(mr_info["oy"]) > 0 else None

    # Lab Results
    mr["objective"]["lab-result"]["biopsy test"] = []
    for te in mr_info["te"]:
        mr["objective"]["lab-result"]["biopsy test"].append({
            "order date": te["sap06odrdat"], 
            "result date": te["sap06rstdat"], 
            "test result": te["sap06gross"],
            "test note": te["sap06note"]
            })
    mr["objective"]["lab-result"]["cytology test"] = []
    for ce in mr_info["ce"]:
        mr["objective"]["lab-result"]["cytology test"].append({
            "order date": ce["sap08odrdat"], 
            "result date": ce["sap08rstdat"], 
            "test result": ce["sap08diag"]
        })
    mr["objective"]["lab-result"]["video reading"] = []
    for yt in mr_info["yt"]:
        mr["objective"]["lab-result"]["video reading"].append({
            "order date": yt["srd04odrdat"], 
            "result date": yt["srd04rddat"], 
            "findings": yt["srd04find"],
            "impression": yt["srd04imp"]
        })

    mr["objective"]["lab-result"]["diagnostic test"] = []
    for je in mr_info["je"]:
        mr["objective"]["lab-result"]["diagnostic test"].append({
            "order date": je["scp42odrdat"], 
            "result date": je["scp42tstdat"], 
            "test code": je["scp42sugacd"],
            "test name": "",
            "test result": je["scp42result"],
            "test comment": je["scp42cmt"],
            "test comment rst": je["scp42rstcmt"],
            "test comment lis": je["scp42liscmt"],
            "test upper limit": "",
            "test lower limit": "",
            "test unit": ""
        })

    mr["objective"]["lab-result"]["vital signs"] = []
    for vs in mr_info["vs"] if "vs" in mr_info else []:
        mr["objective"]["lab-result"]["vital signs"].append({
            "result date": vs["rddate"], 
            "result time": vs["rdtime"], 
            "temperature": vs["temperature"],
            "pulse": vs["pulse"],
            "heart rate": vs["hr"],
            "respiratory rate": vs["rr"],
            "systolic blood pressure": vs["sbp"],
            "diastolic  blood pressure": vs["dbp"]
        })

    # Operation Reports
    mr["operation records"] = []
    for op in mr_info["or"]:
        mr["operation records"].append({
            "surgeon": op["cmta01spth"],
            "assistant": None,
            "nurse": None,
            "anesthesiologist": None,
            "method of anesthesia": None,

            "operation date": op["ocm06opdat"],
            "operation start time": op["ocm06opstarttm"], 
            "operation end time": op["ocm06opendtm"], 

            "operation name": op["cmta08opname"],
            "preoperative diagnosis": op["cmta07predx"],
            "postoperative diagnosis": op["cmta11postdx"],

            "operation procedures and findings": op["ocm06cmtb"],
            "operation notes": op["ocm06memo"],
            "medical treatment plan": op["ocm06mdtrplan"],
            "operation progress": op["ocm06opprgr"],

            "additional data": {
                "alarm": op["ocm06alarm"],
                "cmplyn": op["cmplyn"],
                "emdv": op["ocm06emdv"],
                "pclr": op["ocm06pclr"],
            },
        
            "operation check": {
                "tissue examination": op["ocm06tissueexmn"],
                "tissue examination contents": op["ocm06tissueexmncnts"],
                "drain pipe": op["ocm06drngpipe"],
                "drain pipe contents": op["ocm06drngpipecnts"]
                },
        
        "report date": op["ocm06sysdat"],
        "report time": op["ocm06systm"],
        })

    # Progress Notes
    mr["progress notes"] = []
    for pn in mr_info["pn"]:
        mr["progress notes"].append({
            "order date":pn["odr03odrdat"], 
            "order note":pn["odr03odrcmt"]})

    # Discharge Summary
    mr["discharge summary"] = {}
    for rt in mr_info["rt"]:
        mr["discharge summary"] = {
            "date of discharge": rt["ocm32rtdat"],

            "chief complaints": rt["ocm32chiefcomp"],
            "final diagnosis": rt["ocm32finaldx"],
            "secondary diagnosis": rt["ocm32scnddx"],
            "treatment operation": rt["ocm32op"],
            "treatment medication": rt["ocm32medical"],
            "abnormal findings and lab result": rt["ocm32problem"],

            "follow-up plan": rt["ocm32follow"],
            "progress summary": rt["ocm32other"],
            "treatment result": rt["ocm32rtrstcd"],
            "type of discharge": rt["ocm32rttypecd"],
            "discharge comments": rt["ocm32rtcmt"],
            "medicine": [],

            "report date": rt["ocm32sysdat"],
            "report time": rt["ocm32systm"],
            }
    
    # Protocols
    mr["operation protocols"] = mr_info["pt_o"]
    mr["discharge protocols"] = mr_info["pt_r"]

    return mr

#
# Operation Report (수술기록지)
#
def fill_or_source(patient_id, admsn_date, kwa, spth, mr_info):
    # 일반 입원기록
    df_ae = mr_info.get("ae")
    # 산부인과 입원기록
    df_ay = mr_info.get("ay")
    # 상병 정보
    df_il = mr_info.get("il")
    # 수술예약 정보
    df_oy = mr_info.get("oy")
   # Protocol of Doctor
    df_pt = mr_info.get("pt_o")

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
            "doctor assistant": None,
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
            "diagnosis": [df_il[icd][0] for icd in ["icd01","icd02","icd03","icd04","icd05"] if len(df_il[icd][0].strip()) > 0] if len(df_il) > 0 else None,
            },
        "plan": {
            "operation name": df_oy["operation_name"][0] if len(df_oy) > 0 else None,
            "plan": df_ae["ocm31plan"][0] if len(df_ae) > 0 else df_ay["ocm41planop"][0] if len(df_ay) > 0 else None,
            "discharge plan": df_ae["ocm31rtplan"][0] if len(df_ae) > 0 else df_ay["ocm41rtplan"][0] if len(df_ay) > 0 else None,
            "educational plan": df_ae["ocm31edu"][0] if len(df_ae) > 0 else df_ay["ocm41edct"][0] if len(df_ay) > 0 else None,
            },

        "report date": df_ae["ocm31sysdat"][0] if len(df_ae) > 0 else df_ay["ocm41sysdat"][0] if len(df_ay) > 0 else None,
        "report time": df_ae["ocm31systm"][0] if len(df_ae) > 0 else df_ay["ocm41systime"][0] if len(df_ay) > 0 else None,

        "protocols of doctor": df_pt.to_dict(orient="records")
    }

    return or_source

#
# Operation Report (수술기록지)
#
def fill_op_record_from_db(df_or):
    if len(df_or) == 0:
        return None
    
    op_record = template.get_medical_record_template().get("operation records")[0]

    op_record["staff"] = {
        "surgeon": df_or["cmta08spth"][0],
        "assistant": None,
        "nurse": None,
        "anesthesiologist": None,
        "method of anesthesia": None,
    },

    op_record["operation date"] = df_or["ocm06opdat"][0] if len(df_or) > 0 else None
    op_record["operation start time"] = df_or["ocm06opstarttm"][0] if len(df_or) > 0 else None
    op_record["operation end time"] = df_or["ocm06opendtm"][0] if len(df_or) > 0 else None

    op_record["operation name"] = df_or["cmta08opname"][8] if len(df_or) > 0 else None
    op_record["preoperative diagnosis"] = df_or["cmta08predx"][7] if len(df_or) > 0 else None
    op_record["postoperative diagnosis"] = df_or["cmta08postdx"][11] if len(df_or) > 0 else None

    op_record["operation procedures and findings"] = df_or["ocm06cmtb"][0] if len(df_or) > 0 else None
    op_record["operation notes"] = df_or["ocm06memo"][0] if len(df_or) > 0 else None
    op_record["medical treatment plan"] = df_or["ocm06mdtrplan"][0] if len(df_or) > 0 else None
    op_record["operation progress"] = df_or["ocm06opprgr"][0] if len(df_or) > 0 else None

    op_record["additional data"] = {
        "alarm": df_or["ocm06alarm"][0] if len(df_or) > 0 else None,
        "cmplyn": df_or["cmplyn"][0] if len(df_or) > 0 else None,
        "emdv" :df_or["ocm06emdv"][0] if len(df_or) > 0 else None,
        "pclr": df_or["ocm06pclr"][0] if len(df_or) > 0 else None,
        }
    
    op_record["operation check"] = {
        "tissue examination": df_or["ocm06tissueexmn"][0] if len(df_or) > 0 else None,
        "tissue examination contents": df_or["ocm06tissueexmncnts"][0] if len(df_or) > 0 else None,
        "drain pipe": df_or["ocm06drngpipe"][0] if len(df_or) > 0 else None,
        "drain pipe contents": df_or["ocm06drngpipecnts"][0] if len(df_or) > 0 else None,
        }

    op_record["report date"] = df_or["ocm06sysdat"][0] if len(df_or) > 0 else None
    op_record["report time"] = df_or["ocm06systm"][0] if len(df_or) > 0 else None

    return op_record

#
# Discharge Summary Report (퇴원요약지)
#
def fill_rt_source(patient_id, admsn_date, kwa, spth, mr_info):
    df_ae = mr_info.get("ae")
    df_ay = mr_info.get("ay")
    df_or = mr_info.get("or")
    df_pn = mr_info.get("pn")

    df_pt_r = mr_info.get("pt_r")

    df_je = mr_info.get("je")
    df_te = mr_info.get("te")
    df_ce = mr_info.get("ce")
    df_yt = mr_info.get("yt")

    rt_source = {
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

            "obsteric gpal": None if len(df_ae) > 0 else {"gravidity":base.ifnull(df_ay["ocm41ohg"][0],"<na>"), "preterm":base.ifnull(df_ay["ocm41ohp"][0],"<na>"), "abortion":base.ifnull(df_ay["ocm41oha"][0],"<na>"), "living":base.ifnull(df_ay["ocm41ohl"][0],"<na>")} if len(df_ay) > 0 else None,
            "menstrual history": None if len(df_ae) > 0 else {"last menstrual period":base.ifnull(df_ay["ocm41lmp"][0],"<na>"), "previous menstrual period":base.ifnull(df_ay["ocm41pmp"][0],"<na>"), "menstrual cycle":base.ifnull(df_ay["ocm41interval"][0],"<na>"), "menache":base.ifnull(df_ay["ocm41menache"][0],"<na>")} if len(df_ay) > 0 else None,

            "past medical history": df_ae["ocm31pmhx"][0] if len(df_ae) > 0 else df_ay["ocm41phx"][0] if len(df_ay) > 0 else None,
            "admission-operation history": None if len(df_ae) > 0 else df_ay["ocm41adm"][0] if len(df_ay) > 0 else None,

            "social history": df_ae["ocm31soc"][0] if len(df_ae) > 0 else df_ay["ocm41shx"][0] if len(df_ay) > 0 else None,
            "family history": df_ae["ocm31family"][0] if len(df_ae) > 0 else df_ay["ocm41fhx"][0] if len(df_ay) > 0 else None,
            },
        
        "objective": {
            "review of systems": None if len(df_ae) > 0 else df_ay["ocm41ros"][0] if len(df_ay) > 0 else None,
            "other review of systems": df_ae["ocm31rosother"][0] if len(df_ae) > 0 else df_ay["ocm41rosother"][0] if len(df_ay) > 0 else None,
            "lab-result": {
                "diagnostic test": df_je[['scp42odrdat', 'scp42spmdat', 'scp42sugacd', 'scp42result','scp42rstcd']].to_dict(orient="records"),
                "biopsy test": df_te[['sap06odrdat', 'sap06rstdat', 'sap06gross']].to_dict(orient="records"),
                "cytology test": df_ce[['sap08odrdat', 'sap08rstdat', 'sap08diag']].to_dict(orient="records"),
                "video reading": df_yt[['srd04odrdat', 'srd04rddat', 'srd04find', 'srd04imp']].to_dict(orient="records"),
                },
            },

        "assessment": {
            "impression": df_ae["ocm31imp"][0] if len(df_ae) > 0 else df_ay["ocm41imp"][0] if len(df_ay) > 0 else None,
            "diagnosis": [None],
            },
        
        "plan": {
            "operation name": None,
            "treatment plan": df_ae["ocm31plan"][0] if len(df_ae) > 0 else df_ay["ocm41planop"][0] if len(df_ay) > 0 else None,
            "discharge plan": df_ae["ocm31rtplan"][0] if len(df_ae) > 0 else df_ay["ocm41rtplan"][0] if len(df_ay) > 0 else None,
            "educational plan": df_ae["ocm31edu"][0] if len(df_ae) > 0 else df_ay["ocm41edct"][0] if len(df_ay) > 0 else None,
            },

        "report date": df_ae["ocm31sysdat"][0] if len(df_ae) > 0 else df_ay["ocm41sysdat"][0] if len(df_ay) > 0 else None,
        "report time": df_ae["ocm31systm"][0] if len(df_ae) > 0 else df_ay["ocm41systime"][0] if len(df_ay) > 0 else None,

        "operation": {
            "operation date": df_or["ocm06opdat"][0] if len(df_or) > 0 else None,
            "operation data": df_or["ocm06cmta"][0] if len(df_or) > 0 else None,
            "operation procedures and findings": df_or["ocm06cmtb"][0] if len(df_or) > 0 else None,
            "operation notes": df_or["ocm06memo"][0] if len(df_or) > 0 else None,
            "medical treatment plan": df_or["ocm06mdtrplan"][0] if len(df_or) > 0 else None,
            },

        "progress notes": df_pn[['odr03odrdat', 'odr03odrcmt']].to_dict(orient="records"),

        "protocols of doctor": df_pt_r.to_dict(orient="records")
    }

    return rt_source

#
# Discharge Summary (퇴원요약지)
#
def fill_rt_record_from_db(patient_id, admsn_date, mr_info):
    df_rt = mr_info.get("rt")

    rt_current = template.get_discharge_summary_template()

    if df_rt is None or len(df_rt) == 0:
        return rt_current
    
    rt_current = {
        "patient": {
            "patient id": patient_id,
            "date of admission": admsn_date,
            
            "sex": df_rt["ocm32sex"][0] if len(df_rt) > 0 else None,
            "age": df_rt["ocm32age"][0] if len(df_rt) > 0 else None,
            },
        "clinical staff": {
            "department": df_rt["ocm32kwa"][0] if len(df_rt) > 0 else None,
            "doctor in charge": df_rt["ocm32spth"][0] if len(df_rt) > 0 else None,
            "doctor assistant": str(df_rt["ocm32rgcd"][0]) if len(df_rt) > 0 else None,
        },
        "clinical dates": {
            "date of admission": df_rt["ocm32hpdat"][0] if len(df_rt) > 0 else None,
            #"date of operation": df_rt["ocm32opdat"][0] if len(df_rt) > 0 else None,
            "date of discharge": df_rt["ocm32rtdat"][0] if len(df_rt) > 0 else None,
        },
        "summary": {
            "chief complaints": df_rt["ocm32chiefcomp"][0] if len(df_rt) > 0 else None,
            "final diagnosis": df_rt["ocm32finaldx"][0] if len(df_rt) > 0 else None,
            "secondary diagnosis": df_rt["ocm32scnddx"][0] if len(df_rt) > 0 else None,
            "treatment operation": df_rt["ocm32op"][0] if len(df_rt) > 0 else None,
            "treatment medication": df_rt["ocm32medical"][0] if len(df_rt) > 0 else None,
            "abnormal findings and lab result": df_rt["ocm32problem"][0] if len(df_rt) > 0 else None,
    
            "follow-up plan": df_rt["ocm32follow"][0] if len(df_rt) > 0 else None,
            "progress summary": df_rt["ocm32other"][0] if len(df_rt) > 0 else None,
            "treatment result": df_rt["ocm32rtrstcd"][0] if len(df_rt) > 0 else None,
            "type of discharge": df_rt["ocm32rttypecd"][0] if len(df_rt) > 0 else None,
            "discharge comments": df_rt["ocm32rtcmt"][0] if len(df_rt) > 0 else None,
            "medicine": [],

            "report date": df_rt["ocm32sysdat"][0] if len(df_rt) > 0 else None,
            "report time": df_rt["ocm32systm"][0] if len(df_rt) > 0 else None,
        }
    }

    return rt_current

def call_api(prompt, data, model):
    reponses = genai.generate([prompt, data], model)
    return reponses
