from .. import conectarSQL
import pandas as pd

def insertar_temporadas(df):
    conn = conectarSQL.conectar()
    cursor = conn.cursor()

    temporadas = df["Season"].unique()

    for temporada in temporadas:
        ano_inicio, ano_fin = temporada.split("/")
        cursor.execute("INSERT INTO Dim_Temporada (Season, Ano_Inicio, Ano_Fin) VALUES (?, ?, ?)",
                       temporada, int(ano_inicio), int(ano_fin))

    conn.commit()
    conn.close()
    print("Temporadas insertadas correctamente.")

if __name__ == "__main__":
    df = pd.read_csv("LaLiga_Matches.csv")
    insertar_temporadas(df)
