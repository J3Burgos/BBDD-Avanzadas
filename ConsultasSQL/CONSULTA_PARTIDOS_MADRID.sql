--Muestra los partidos donde Real Madrid jugó como local o visitante.
--Ordenados por fecha más reciente primero.
SELECT h.ID_Partido, f.Fecha, t.Season, el.Nombre AS Equipo_Local, ev.Nombre AS Equipo_Visitante, 
       h.Goles_Local, h.Goles_Visitante, r.Descripcion AS Resultado_Final
FROM HechosPartidos h
JOIN Dim_Temporada t ON h.ID_Temporada = t.ID_Temporada
JOIN Dim_Equipos el ON h.ID_Equipo_Local = el.ID_Equipo
JOIN Dim_Equipos ev ON h.ID_Equipo_Visitante = ev.ID_Equipo
JOIN Dim_Fecha f ON h.ID_Fecha = f.ID_Fecha
JOIN Dim_Resultado r ON h.ID_Resultado_Final = r.ID_Resultado
WHERE el.Nombre = 'Real Madrid' OR ev.Nombre = 'Real Madrid'
ORDER BY f.Fecha DESC;