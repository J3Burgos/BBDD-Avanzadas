import pandas as pd
from scripts.db_connection import get_connection

def load_temporadas(df):
    conn = get_connection()
    cursor = conn.cursor()

    temporadas = df["Season"].unique()

    for temporada in temporadas:
        try:
            ano_inicio, _ = temporada.split("-")
            ano_inicio = int(ano_inicio)
            ano_fin = ano_inicio + 1  

            cursor.execute("SELECT COUNT(*) FROM Dim_Temporada WHERE Season = ?", temporada)
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO Dim_Temporada (Season, Ano_Inicio, Ano_Fin) VALUES (?, ?, ?)", 
                               temporada, ano_inicio, ano_fin)
        except ValueError:
            print(f"Formato incorrecto de temporada {temporada}. Omitiendo.")

    conn.commit()
    cursor.close()
    conn.close()
