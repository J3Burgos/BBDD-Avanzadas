-- Creación de la Dimensión Temporada
CREATE TABLE Dim_Temporada (
    ID_Temporada INT IDENTITY(1,1) PRIMARY KEY,
    Season VARCHAR(10) UNIQUE NOT NULL,
    Ano_Inicio INT NOT NULL,
    Ano_Fin INT NOT NULL
);

-- Índice para mejorar la búsqueda de temporadas
CREATE INDEX idx_Season ON Dim_Temporada(Season);

-- Creación de la Dimensión Equipos
CREATE TABLE Dim_Equipos (
    ID_Equipo INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Creación de la Dimensión Fecha
CREATE TABLE Dim_Fecha (
    ID_Fecha INT IDENTITY(1,1) PRIMARY KEY,
    Fecha DATE NOT NULL UNIQUE,
    Dia INT NOT NULL,
    Mes INT NOT NULL,
    Ano INT NOT NULL,
    Dia_Semana VARCHAR(10) NOT NULL
);

-- Validaciones en la tabla de fechas
ALTER TABLE Dim_Fecha ADD CONSTRAINT chk_mes CHECK (Mes BETWEEN 1 AND 12);
ALTER TABLE Dim_Fecha ADD CONSTRAINT chk_dia CHECK (Dia BETWEEN 1 AND 31);
ALTER TABLE Dim_Fecha ADD CONSTRAINT chk_ano CHECK (Ano >= 1900);

-- Creación de la Dimensión Resultado (Nueva tabla para almacenar el resultado del partido)
CREATE TABLE Dim_Resultado (
    ID_Resultado INT IDENTITY(1,1) PRIMARY KEY,
    Descripcion VARCHAR(10) UNIQUE NOT NULL -- Ej: 'Victoria', 'Empate', 'Derrota'
);

-- Creación de la Tabla de Hechos
CREATE TABLE HechosPartidos (
    ID_Partido INT IDENTITY(1,1) PRIMARY KEY,
    ID_Temporada INT NOT NULL,
    ID_Equipo_Local INT NOT NULL,
    ID_Equipo_Visitante INT NOT NULL,
    ID_Fecha INT NOT NULL,
    Goles_Local INT NOT NULL,
    Goles_Visitante INT NOT NULL,
    ID_Resultado_Final INT NOT NULL,  -- Referencia a Dim_Resultado
    Goles_HT_Local INT NOT NULL,
    Goles_HT_Visitante INT NOT NULL,
    ID_Resultado_HT INT NOT NULL,  -- Referencia a Dim_Resultado
    FOREIGN KEY (ID_Temporada) REFERENCES Dim_Temporada(ID_Temporada),
    FOREIGN KEY (ID_Equipo_Local) REFERENCES Dim_Equipos(ID_Equipo),
    FOREIGN KEY (ID_Equipo_Visitante) REFERENCES Dim_Equipos(ID_Equipo),
    FOREIGN KEY (ID_Fecha) REFERENCES Dim_Fecha(ID_Fecha),
    FOREIGN KEY (ID_Resultado_Final) REFERENCES Dim_Resultado(ID_Resultado),
    FOREIGN KEY (ID_Resultado_HT) REFERENCES Dim_Resultado(ID_Resultado)
);

-- Índices en claves foráneas para mejorar la performance de los JOINs
CREATE INDEX idx_Hechos_Temporada ON HechosPartidos(ID_Temporada);
CREATE INDEX idx_Hechos_Equipo_Local ON HechosPartidos(ID_Equipo_Local);
CREATE INDEX idx_Hechos_Equipo_Visitante ON HechosPartidos(ID_Equipo_Visitante);
CREATE INDEX idx_Hechos_Fecha ON HechosPartidos(ID_Fecha);
CREATE INDEX idx_Hechos_Resultado_Final ON HechosPartidos(ID_Resultado_Final);
CREATE INDEX idx_Hechos_Resultado_HT ON HechosPartidos(ID_Resultado_HT);

SELECT * FROM Dim_Resultado;

INSERT INTO Dim_Resultado (Descripcion) VALUES ('H'); -- Victoria local
INSERT INTO Dim_Resultado (Descripcion) VALUES ('A'); -- Victoria visitante
INSERT INTO Dim_Resultado (Descripcion) VALUES ('D'); -- Empate

