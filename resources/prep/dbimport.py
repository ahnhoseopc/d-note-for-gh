import utils.db as db
import pandas as pd
import logging

files = ["protocol-en.csv","protocol-gs.csv","protocol-gy.csv","protocol-ns.csv","protocol-os.csv","protocol-dis.csv"]
for file in files:
    df = pd.read_csv(f"{file}")
    df.to_sql('jain_ocs.OMTCMT24', con=db.get_sql_engine(), if_exists='append', index=False)

    logging.info(file, df.head())
