WITH Racha_Local AS (
    SELECT 
        e.Nombre AS Equipo,
        f.Fecha,
        CASE 
            WHEN r.Descripcion = 'H' THEN 1  -- Victoria como local
            ELSE 0  -- No victoria
        END AS Victoria_Local,
        ROW_NUMBER() OVER (PARTITION BY e.Nombre ORDER BY f.Fecha) AS RowNum
    FROM HechosPartidos h
    JOIN Dim_Equipos e ON h.ID_Equipo_Local = e.ID_Equipo
    JOIN Dim_Resultado r ON h.ID_Resultado_Final = r.ID_Resultado
    JOIN Dim_Fecha f ON h.ID_Fecha = f.ID_Fecha
	WHERE e.Nombre = 'Albacete'
),
Rachas_Completas AS (
    SELECT 
        Equipo,
        Fecha,
        Victoria_Local,
        RowNum,
        RowNum - ROW_NUMBER() OVER (PARTITION BY Equipo ORDER BY Fecha) AS Racha_Segmento
    FROM Racha_Local  -- Usamos la CTE aquí para que las columnas sean reconocidas
    WHERE Victoria_Local = 1  -- Solo victorias
)
-- Ahora agrupamos y calculamos la longitud de las rachas
SELECT TOP 1
    Equipo,
    COUNT(*) AS Max_Racha_Local
FROM Rachas_Completas
GROUP BY Equipo, Racha_Segmento
ORDER BY Max_Racha_Local DESC;
