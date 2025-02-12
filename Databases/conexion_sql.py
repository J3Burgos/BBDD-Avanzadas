import pyodbc

# Configurar la conexión a SQL Server
server = "JORGE\\J_3_BURGOS"  # Asegúrate de que este nombre es correcto
database = "LaLigaDW"  # Puedes cambiarlo a tu base de datos específica
conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Ejecutar una consulta de prueba
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Conexión exitosa a SQL Server")
    print("Versión:", row[0])
    
    # Cerrar la conexión
    cursor.close()
    conn.close()
    
except Exception as e:
    print("Error al conectar con SQL Server:", e)
