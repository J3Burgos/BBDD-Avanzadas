SELECT TOP 10 f.Fecha, t.Season, el.Nombre AS Equipo_Local, ev.Nombre AS Equipo_Visitante, 
              h.Goles_Local, h.Goles_Visitante, (h.Goles_Local + h.Goles_Visitante) AS Total_Goles
FROM HechosPartidos h
JOIN Dim_Temporada t ON h.ID_Temporada = t.ID_Temporada
JOIN Dim_Equipos el ON h.ID_Equipo_Local = el.ID_Equipo
JOIN Dim_Equipos ev ON h.ID_Equipo_Visitante = ev.ID_Equipo
JOIN Dim_Fecha f ON h.ID_Fecha = f.ID_Fecha
ORDER BY Total_Goles DESC;
