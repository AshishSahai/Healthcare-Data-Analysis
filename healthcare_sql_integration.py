import pandas as pd
from healthcare import load_data
import sqlite3


healthcare_raw_data = pd.read_csv("healthcare_dataset.csv")
conn = sqlite3.connect("healthcare.db")
healthcare_raw_data.to_sql("Patients", conn, if_exists= "replace", index = False)

query = """SELECT Hospital, AVG("Billing Amount") AS AvgBilling FROM Patients GROUP BY Hospital;"""
result = pd.read_sql_query(query, conn)
conn.close()
print(result)