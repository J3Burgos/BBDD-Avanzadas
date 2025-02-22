SELECT e.Nombre AS Equipo,
       SUM(h.Goles_Local) + SUM(h.Goles_Visitante) AS Total_Goles
FROM HechosPartidos h
JOIN Dim_Equipos e ON h.ID_Equipo_Local = e.ID_Equipo
GROUP BY e.Nombre
ORDER BY Total_Goles DESC;
