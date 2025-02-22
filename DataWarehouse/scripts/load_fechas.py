from datetime import datetime
import pandas as pd
from scripts.db_connection import get_connection

def load_fechas(df):
    conn = get_connection()
    cursor = conn.cursor()

    fechas = df["Date"].unique()

    for fecha in fechas:
        fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")
        fecha_str = fecha_dt.strftime("%Y-%m-%d")

        cursor.execute("SELECT COUNT(*) FROM Dim_Fecha WHERE Fecha = ?", fecha_str)
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Dim_Fecha (Fecha, Dia, Mes, Ano, Dia_Semana) VALUES (?, ?, ?, ?, ?)",
                           fecha_str, fecha_dt.day, fecha_dt.month, fecha_dt.year, fecha_dt.strftime('%A'))

    conn.commit()
    cursor.close()
    conn.close()
