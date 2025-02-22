import numpy as np
from datetime import datetime
import pandas as pd
from scripts.db_connection import get_connection

def load_partidos(df):
    conn = get_connection()
    cursor = conn.cursor()

    equipos_dict = {nombre: id for id, nombre in cursor.execute("SELECT ID_Equipo, Nombre FROM Dim_Equipos").fetchall()}
    temporadas_dict = {season: id for id, season in cursor.execute("SELECT ID_Temporada, Season FROM Dim_Temporada").fetchall()}
    fechas_dict = {fecha: id for id, fecha in cursor.execute("SELECT ID_Fecha, Fecha FROM Dim_Fecha").fetchall()}
    resultados_dict = {descripcion: id for id, descripcion in cursor.execute("SELECT ID_Resultado, Descripcion FROM Dim_Resultado").fetchall()}

    for _, row in df.iterrows():
        fecha_dt = datetime.strptime(row["Date"], "%d-%m-%Y")
        fecha_str = fecha_dt.strftime("%Y-%m-%d")

        id_fecha = fechas_dict.get(fecha_str)
        id_temporada = temporadas_dict.get(row["Season"], None)
        id_equipo_local = equipos_dict.get(row["HomeTeam"], None)
        id_equipo_visitante = equipos_dict.get(row["AwayTeam"], None)
        id_resultado_final = resultados_dict.get(row["FTR"], None)
        id_resultado_ht = resultados_dict.get(row["HTR"], None)

        goles_local = int(row["FTHG"]) if not pd.isna(row["FTHG"]) else 0
        goles_visitante = int(row["FTAG"]) if not pd.isna(row["FTAG"]) else 0
        goles_ht_local = int(row["HTHG"]) if not pd.isna(row["HTHG"]) else 0
        goles_ht_visitante = int(row["HTAG"]) if not pd.isna(row["HTAG"]) else 0

        if None in [id_temporada, id_equipo_local, id_equipo_visitante, id_resultado_final, id_resultado_ht]:
            print(f"Datos faltantes en partido {row['HomeTeam']} vs {row['AwayTeam']} en {fecha_str}. Omitiendo inserción.")
            continue  

        cursor.execute("""INSERT INTO HechosPartidos (ID_Temporada, ID_Equipo_Local, ID_Equipo_Visitante, ID_Fecha, 
                                                     Goles_Local, Goles_Visitante, ID_Resultado_Final, 
                                                     Goles_HT_Local, Goles_HT_Visitante, ID_Resultado_HT) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       id_temporada, id_equipo_local, id_equipo_visitante, id_fecha,
                       goles_local, goles_visitante, id_resultado_final,
                       goles_ht_local, goles_ht_visitante, id_resultado_ht)

    conn.commit()
    cursor.close()
    conn.close()
