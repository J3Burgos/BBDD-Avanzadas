from .. import conectarSQL
import pandas as pd

def insertar_partidos(df):
    conn = conectarSQL.conectar()
    cursor = conn.cursor()

    equipos_dict = {nombre: id for id, nombre in cursor.execute("SELECT ID_Equipo, Nombre FROM Dim_Equipos").fetchall()}
    temporadas_dict = {season: id for id, season in cursor.execute("SELECT ID_Temporada, Season FROM Dim_Temporada").fetchall()}
    fechas_dict = {fecha: id for id, fecha in cursor.execute("SELECT ID_Fecha, Fecha FROM Dim_Fecha").fetchall()}

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO HechosPartidos (ID_Temporada, ID_Equipo_Local, ID_Equipo_Visitante, ID_Fecha, 
                                        Goles_Local, Goles_Visitante, Resultado_Final, 
                                        Goles_HT_Local, Goles_HT_Visitante, Resultado_HT) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       temporadas_dict[row["Season"]],
                       equipos_dict[row["HomeTeam"]],
                       equipos_dict[row["AwayTeam"]],
                       fechas_dict[row["Date"]],
                       row["FTHG"], row["FTAG"], row["FTR"],
                       row["HTHG"], row["HTAG"], row["HTR"])

    conn.commit()
    conn.close()
    print("Partidos insertados correctamente.")

if __name__ == "__main__":
    df = pd.read_csv("LaLiga_Matches.csv")
    insertar_partidos(df)
