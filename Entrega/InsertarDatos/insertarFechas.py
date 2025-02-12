from .. import conectarSQL
import pandas as pd
from datetime import datetime

def insertar_fechas(df):
    conn = conectarSQL.conectar()
    cursor = conn.cursor()

    fechas = df["Date"].unique()

    for fecha in fechas:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        cursor.execute("INSERT INTO Dim_Fecha (Fecha, Dia, Mes, Ano, Dia_Semana) VALUES (?, ?, ?, ?, ?)",
                       fecha_dt, fecha_dt.day, fecha_dt.month, fecha_dt.year, fecha_dt.strftime('%A'))

    conn.commit()
    conn.close()
    print("Fechas insertadas correctamente.")

if __name__ == "__main__":
    df = pd.read_csv("LaLiga_Matches.csv")
    insertar_fechas(df)
