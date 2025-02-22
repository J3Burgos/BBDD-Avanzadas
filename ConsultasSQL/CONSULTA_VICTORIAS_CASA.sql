SELECT e.Nombre AS Equipo, COUNT(*) AS Victorias_Local
FROM HechosPartidos h
JOIN Dim_Equipos e ON h.ID_Equipo_Local = e.ID_Equipo
JOIN Dim_Resultado r ON h.ID_Resultado_Final = r.ID_Resultado
WHERE r.Descripcion = 'H'  -- 'H' significa victoria del equipo local
GROUP BY e.Nombre
ORDER BY Victorias_Local DESC;
