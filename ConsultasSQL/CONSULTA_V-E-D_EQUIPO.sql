SELECT e.Nombre AS Equipo,
       SUM(CASE WHEN h.ID_Resultado_Final = rH.ID_Resultado THEN 1 ELSE 0 END) AS Victorias,
       SUM(CASE WHEN h.ID_Resultado_Final = rD.ID_Resultado THEN 1 ELSE 0 END) AS Empates,
       SUM(CASE WHEN h.ID_Resultado_Final = rA.ID_Resultado THEN 1 ELSE 0 END) AS Derrotas
FROM HechosPartidos h
JOIN Dim_Equipos e ON h.ID_Equipo_Local = e.ID_Equipo
LEFT JOIN Dim_Resultado rH ON rH.Descripcion = 'H'
LEFT JOIN Dim_Resultado rD ON rD.Descripcion = 'D'
LEFT JOIN Dim_Resultado rA ON rA.Descripcion = 'A'
GROUP BY e.Nombre
ORDER BY Victorias DESC;
