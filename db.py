import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd

# Load environment variables
load_dotenv()

# Get credentials from .env
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

def get_task():
    cursor.execute("SELECT * FROM tracker;")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]  # get column names
    df = pd.DataFrame.from_records(rows, columns=columns)
    print(df)


# Connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT @@VERSION AS version;")
    row = cursor.fetchone()
    print("✅ Connected! SQL Server version:", row.version)
    get_task()

except Exception as e:
    print("❌ Connection failed:", e)







finally:
    conn.close()
