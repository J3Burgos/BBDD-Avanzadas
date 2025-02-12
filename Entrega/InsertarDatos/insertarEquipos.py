from .. import conectarSQL
import pandas as pd

def insertar_equipos(df):
    conn = conectarSQL.conectar()
    cursor = conn.cursor()

    equipos = set(df["HomeTeam"].unique()).union(set(df["AwayTeam"].unique()))

    for equipo in equipos:
        cursor.execute("INSERT INTO Dim_Equipos (Nombre) VALUES (?)", equipo)

    conn.commit()
    conn.close()
    print("Equipos insertados correctamente.")

if __name__ == "__main__":
    df = pd.read_csv("LaLiga_Matches.csv")
    insertar_equipos(df)
