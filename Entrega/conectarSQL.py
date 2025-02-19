
import pandas as pd
import pyodbc


df = pd.read_csv("..\RAW\LaLiga_Matches.csv")


# Mostrar las primeras filas para verificar la estructura
print(df.head())
    
server = 'JORGE\\J_3_BURGOS'  # Cambia si es necesario
database = 'LaLigaDW'  # Cambia por el nombre real
# Conectar a SQL Server
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
cursor = conn.cursor()

print("Conexión exitosa a SQL Server")





# Extraer temporadas únicas
temporadas = df["Season"].unique()

# Insertarlas en la base de datos solo si no existen
for temporada in temporadas:
    try:
        # Convertir "1995-96" en 1995 y 1996
        ano_inicio, ano_fin = temporada.split("-")
        ano_inicio = int(ano_inicio)
        ano_fin = ano_inicio + 1  # Porque "1995-96" se refiere a la temporada 1995/1996
        
        # Verificar si la temporada ya existe en la base de datos
        cursor.execute("SELECT COUNT(*) FROM Dim_Temporada WHERE Season = ?", temporada)
        if cursor.fetchone()[0] == 0:  # Si no existe, se inserta
            cursor.execute("INSERT INTO Dim_Temporada (Season, Ano_Inicio, Ano_Fin) VALUES (?, ?, ?)", temporada, ano_inicio, ano_fin)
        else:
            print(f"La temporada {temporada} ya está en la base de datos.")
    except ValueError:
        print(f"Advertencia: El formato de temporada {temporada} no es válido.")
        continue  # Si el formato no es válido, pasa al siguiente valor

conn.commit()
print("Temporadas insertadas correctamente.")





# Extraer equipos únicos
equipos = set(df["HomeTeam"].unique()).union(set(df["AwayTeam"].unique()))

# Insertarlos en la base de datos solo si no existen
for equipo in equipos:
    # Verificar si el equipo ya existe en la base de datos
    cursor.execute("SELECT COUNT(*) FROM Dim_Equipos WHERE Nombre = ?", equipo)
    if cursor.fetchone()[0] == 0:  # Si no existe, se inserta
        cursor.execute("INSERT INTO Dim_Equipos (Nombre) VALUES (?)", equipo)
    else:
        print(f"El equipo {equipo} ya está en la base de datos.")

conn.commit()
print("Equipos insertados correctamente.")


from datetime import datetime

# Extraer fechas únicas
fechas = df["Date"].unique()

# Insertarlas en la base de datos, pero solo si no existen ya
for fecha in fechas:
    fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")  # Convertir a formato fecha con guiones
    fecha_str = fecha_dt.strftime("%Y-%m-%d")  # Formatear la fecha para que sea consistente en YYYY-MM-DD

    # Verificar si la fecha ya existe en la tabla Dim_Fecha
    cursor.execute("SELECT COUNT(*) FROM Dim_Fecha WHERE Fecha = ?", fecha_str)
    if cursor.fetchone()[0] > 0:
        print(f"Fecha {fecha_str} ya existe en Dim_Fecha. Omitiendo inserción.")
    else:
        cursor.execute("INSERT INTO Dim_Fecha (Fecha, Dia, Mes, Ano, Dia_Semana) VALUES (?, ?, ?, ?, ?)",
                       fecha_str, fecha_dt.day, fecha_dt.month, fecha_dt.year, fecha_dt.strftime('%A'))

conn.commit()
print("Fechas insertadas correctamente.")





# Obtener los IDs de equipos y fechas desde la base de datos
equipos_dict = {nombre: id for id, nombre in cursor.execute("SELECT ID_Equipo, Nombre FROM Dim_Equipos").fetchall()}
temporadas_dict = {season: id for id, season in cursor.execute("SELECT ID_Temporada, Season FROM Dim_Temporada").fetchall()}
fechas_dict = {fecha: id for id, fecha in cursor.execute("SELECT ID_Fecha, Fecha FROM Dim_Fecha").fetchall()}
# Obtener los ID de los resultados desde la base de datos
resultados_dict = {descripcion: id for id, descripcion in cursor.execute("SELECT ID_Resultado, Descripcion FROM Dim_Resultado").fetchall()}
id_resultado_desconocido = resultados_dict.get("Desconocido", None)  # Obtener ID de 'Desconocido' si existe

import numpy as np  # Asegurarnos de manejar valores NaN correctamente

for _, row in df.iterrows():
    fecha_dt = datetime.strptime(row["Date"], "%d-%m-%Y")
    fecha_str = fecha_dt.strftime("%Y-%m-%d")

    id_fecha = fechas_dict.get(fecha_str)
    if id_fecha is None:
        print(f"Advertencia: La fecha {fecha_str} no está en Dim_Fecha.")
        continue  

    id_temporada = temporadas_dict.get(row["Season"], None)
    id_equipo_local = equipos_dict.get(row["HomeTeam"], None)
    id_equipo_visitante = equipos_dict.get(row["AwayTeam"], None)

    id_resultado_final = resultados_dict.get(row["FTR"], None)
    id_resultado_ht = resultados_dict.get(row["HTR"], None)

    # Convertir a enteros, reemplazando NaN con 0
    goles_local = int(row["FTHG"]) if not pd.isna(row["FTHG"]) else 0
    goles_visitante = int(row["FTAG"]) if not pd.isna(row["FTAG"]) else 0
    goles_ht_local = int(row["HTHG"]) if not pd.isna(row["HTHG"]) else 0
    goles_ht_visitante = int(row["HTAG"]) if not pd.isna(row["HTAG"]) else 0

    if None in [id_temporada, id_equipo_local, id_equipo_visitante, id_resultado_final, id_resultado_ht]:
        print(f"Advertencia: Datos faltantes en partido {row['HomeTeam']} vs {row['AwayTeam']} en {fecha_str}. Omitiendo inserción.")
        continue  # Evita insertar si falta algún ID clave

    cursor.execute("""
        INSERT INTO HechosPartidos (ID_Temporada, ID_Equipo_Local, ID_Equipo_Visitante, ID_Fecha, 
                                    Goles_Local, Goles_Visitante, ID_Resultado_Final, 
                                    Goles_HT_Local, Goles_HT_Visitante, ID_Resultado_HT) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   id_temporada, id_equipo_local, id_equipo_visitante, id_fecha,
                   goles_local, goles_visitante, id_resultado_final,
                   goles_ht_local, goles_ht_visitante, id_resultado_ht)

conn.commit()
print("Partidos insertados correctamente.")





cursor.close()
conn.close()
print("Conexión cerrada.")
