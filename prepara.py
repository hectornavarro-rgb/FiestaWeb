import libsql
import streamlit as st

# Leer credenciales de secrets.toml
TURSO_URL = st.secrets["TURSO_URL"]
TURSO_TOKEN = st.secrets["TURSO_TOKEN"]

# Conectar con la base de datos en Turso
conn = libsql.connect("fiesta.db", sync_url=TURSO_URL, auth_token=TURSO_TOKEN)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS invitados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        telefono TEXT,
        correo TEXT,
        asistira BOOLEAN,
        numero_acompanantes INTEGER
    )
""")

conn.commit()
conn.close()

print("Base de datos y tabla creadas correctamente.")
