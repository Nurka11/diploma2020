import csv
import sqlite3
import pandas as pd

connection = sqlite3.connect("monitoring.db")
data = pd.read_sql_query("SELECT * FROM mon_app_competitorproduct", connection)
data.to_csv('database.csv', index=False)
