import pandas as pd
from scripts.load_temporadas import load_temporadas
from scripts.load_equipos import load_equipos
from scripts.load_fechas import load_fechas
from scripts.load_partidos import load_partidos

df = pd.read_csv("data/LaLiga_Matches.csv")

load_temporadas(df)
load_equipos(df)
load_fechas(df)
load_partidos(df)

print("Carga de datos completada.")
