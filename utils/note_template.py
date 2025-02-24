import copy

MEDICAL_RECORD_TEMPLATE = {
    "patient": {
        "patient id": "",
        "date of admission": "",

        "sex": "",
        "age": "",
        },
    "clinical staff": {
        "department": "",
        "doctor in charge": "",
        },

    "subjective": {
        "chief complaints": "",
        "pain": "",
        "onset": "",
        "present illness": "",

        "obsteric gpal": "",
        "menstrual history": "",
        "admission-operation history": "",

        "past medical history": "",
        "social history": "",
        "family history": "",
        },
    
    "objective": {
        "review of systems": "",
        "other review of systems": "",
        "lab-result": {
            "biopsy test": [{"order date": "", "result date": "", "test result": "", "test note": ""}],
            "cytology test": [{"order date": "", "result date": "", "test result": ""}],
            "diagnostic test": [{"order date": "", "result date": "", "test code": "", "test name": "", "test result": "", "test upper limit":"", "test lower limit":"", "test unit":""}],
            "vital signs": [{"reading date":"", "reading time": "", "temperature": "", "pulse": "", "heart rate": "", "respiratory rate": "", "systolic blood pressure": "", "diastolic blood pressure": ""}],
            "video reading": [{"order date": "", "reading date": "", "findings": "", "impression": ""}],
            },
        },

    "assessment": {
        "impression": "",
        "diagnosis": [{"icd_code":"", "diagnosis": ""}],
        },
    
    "plan": {
        "operation plan": "",
        "treatment plan": "",
        "discharge plan": "",
        "educational plan": "",
        },

    "operation records": [{
        "surgeon": "",
        "assistant": "",
        "nurse": "",
        "anesthesiologist": "",
        "method of anesthesia": "",

        "operation date": "",
        "operation start time": "",
        "operation end time": "",

        "operation name": "",
        "preoperative diagnosis": "",
        "postoperative diagnosis": "",

        "operation procedures and findings": "",
        "operation notes": "",
        "medical treatment plan": "",
        "operation progress": "",

        "additional data": {
            "alarm": "",
            "cmplyn": "",
            "emdv": "",
            "pclr": ""
            },
        
        "operation check": {
            "tissue examination": "",
            "tissue examination contents": "",
            "drain pipe": "",
            "drain pipe contents": ""
            },

        "report date": "",
        "report time": "",
        }],

    "progress notes": [{
        "order date": "",
        "order note": "",

        "report date": "",
        "report time": "",
        }],

    "discharge summary": {
        "date of discharge": "",

        "chief complaints": "",
        "final diagnosis": "",
        "secondary diagnosis": "",
        "treatment operation": "",
        "treatment medication": "",
        "abnormal findings and lab result": "",

        "follow-up plan": "",
        "progress summary": "",
        "treatment result": "",
        "type of discharge": "",
        "discharge comments": "",
        "medicine": [],

        "report date": "",
        "report time": "",
    }
}

def get_medical_record_template():
    return copy.deepcopy(MEDICAL_RECORD_TEMPLATE)
