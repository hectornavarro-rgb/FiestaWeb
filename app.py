import streamlit as st
import libsql

# Conexión a la base de datos
TURSO_URL = st.secrets["TURSO_URL"]
TURSO_TOKEN = st.secrets["TURSO_TOKEN"]
conn = libsql.connect("fiesta.db", sync_url=TURSO_URL, auth_token=TURSO_TOKEN)
cursor = conn.cursor()

st.set_page_config(page_title="Fiesta Aniversario", layout="centered")
st.title("🎉 Fiesta de Aniversario - Confirmación de Asistencia")

# --- FORMULARIO PARA AÑADIR O ACTUALIZAR INVITADOS ---
with st.form("form_invitado", clear_on_submit=True):
    st.subheader("Agregar / Actualizar invitado")
    nombre = st.text_input("Nombre", max_chars=50)
    apellidos = st.text_input("Apellidos", max_chars=50)
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    asistira = st.checkbox("¿Asistirá?")
    numero_acompanantes = st.number_input("Número de acompañantes", min_value=0, step=1)

    submitted = st.form_submit_button("Guardar")
    if submitted:
        # Verificar si ya existe
        cursor.execute("SELECT id FROM invitados WHERE correo = ?", (correo,))
        existente = cursor.fetchone()

        if existente:
            # Actualizar existente
            cursor.execute("""
                UPDATE invitados
                SET nombre = ?, apellidos = ?, telefono = ?, asistira = ?, numero_acompanantes = ?
                WHERE correo = ?
            """, (nombre, apellidos, telefono, asistira, numero_acompanantes, correo))
            conn.commit()
            st.success("Invitado actualizado correctamente.")
        else:
            # Insertar nuevo
            cursor.execute("""
                INSERT INTO invitados (nombre, apellidos, telefono, correo, asistira, numero_acompanantes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, apellidos, telefono, correo, asistira, numero_acompanantes))
            conn.commit()
            st.success("Invitado añadido correctamente.")

# --- LISTA DE INVITADOS ---
st.subheader("📋 Lista de invitados")

cursor.execute("SELECT * FROM invitados")
invitados = cursor.fetchall()

if invitados:
    for invitado in invitados:
        st.write(f"**{invitado[1]} {invitado[2]}**")
        st.write(f"📞 Teléfono: {invitado[3]}")
        st.write(f"📧 Correo: {invitado[4]}")
        st.write(f"✅ Asistirá: {'Sí' if invitado[5] else 'No'}")
        st.write(f"👥 Acompañantes: {invitado[6]}")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🗑️ Eliminar", key=f"delete_{invitado[0]}"):
                cursor.execute("DELETE FROM invitados WHERE id = ?", (invitado[0],))
                conn.commit()
                st.experimental_rerun()

        with col2:
            if st.button("✏️ Editar", key=f"edit_{invitado[0]}"):
                # Prellenar datos (no edita en el lugar, solo ayuda a ver el concepto)
                st.warning("Edición solo posible desde el formulario arriba. Ingrese el mismo correo.")
        st.markdown("---")
else:
    st.info("Aún no hay invitados registrados.")

conn.close()
