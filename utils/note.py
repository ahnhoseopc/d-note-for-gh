import utils.config as config
import utils.base as base
import utils.db as db

def run_sql(query_sql):
    df_query = db.run_sql(query_sql)
    return df_query

def call_db_patient_record(query_name, patient_id, admission_date):
    admsn_date = admission_date.strftime("%Y%m%d")
    query = config.get_query(query_name)
    query = query.replace("$patient_id", patient_id)
    query = query.replace("$admsn_date", admsn_date)

    print(query)
    result = run_sql(query)
    return result

def call_api(prompt, key):
    # Replace this with your actual API call
    # For demonstration purposes, we'll just return a random string
    result = base.get_random_string(100)
    return result
