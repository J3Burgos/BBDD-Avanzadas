import pandas as pd
from scripts.db_connection import get_connection

def load_equipos(df):
    conn = get_connection()
    cursor = conn.cursor()

    equipos = set(df["HomeTeam"].unique()).union(set(df["AwayTeam"].unique()))

    for equipo in equipos:
        cursor.execute("SELECT COUNT(*) FROM Dim_Equipos WHERE Nombre = ?", equipo)
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Dim_Equipos (Nombre) VALUES (?)", equipo)

    conn.commit()
    cursor.close()
    conn.close()
