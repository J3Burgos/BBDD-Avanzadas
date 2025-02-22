import pyodbc
from config import config

def get_connection():
    conn = pyodbc.connect(
        f'DRIVER={{SQL Server}};SERVER={config.server};DATABASE={config.database};Trusted_Connection=yes'
    )
    return conn
