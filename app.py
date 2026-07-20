import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configurazione database e directory
DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT,
            serie TEXT,
            anno TEXT,
            marca_corde TEXT,
            spessore_corde TEXT,
            data_cambio TEXT,
            prossimo_cambio TEXT,
            foto_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Guitar Vault", layout="wide")
st.title("🎸 Guitar Vault")

with st.sidebar.expander("➕ Aggiungi Chitarra", expanded=True):
    with st.form("nuova_chitarra", clear_on_submit=True):
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        anno = st.text_input("Anno")
        marca = st.text_input("Marca Corde")
        spessore = st.text_input("Spessore Corde")
        data_cambio = st.date_input("Ultimo Cambio", datetime.now())
        foto = st.file_uploader("Foto", type=["jpg", "png", "jpeg"])
        
        if st.form_submit_button("Salva nel Vault"):
            foto_path = ""
            if foto:
                foto_path = os.path.join(IMG_DIR, f"{serie}_{foto.name}")
                with open(foto_path, "wb") as f: f.write(foto.getbuffer())
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO chitarre (modello, serie, anno, marca_corde, spessore_corde, data_cambio, prossimo_cambio, foto_path) VALUES (?,?,?,?,?,?,?,?)",
                      (modello, serie, anno, marca, spessore, str(data_cambio), str(data_cambio + timedelta(days=90)), foto_path))
            conn.commit()
            conn.close()
            st.rerun()

conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if not df.empty:
    for _, row in df.iterrows():
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if row['foto_path'] and os.path.exists(row['foto_path']):
                # Corretto l'uso di width='stretch' per le nuove versioni di Streamlit
                st.image(row['foto_path'], width='stretch')
            else:
                st.write("📷 No Photo")
        
        with col2:
            st.subheader(row['modello'])
            st.write(f"**S/N:** {row['serie']} | **Anno:** {row.get('anno', '-')}")
            st.write(f"**Corde:** {row.get('marca_corde', '-')} | **Spessore:** {row.get('spessore_corde', '-')}")
            
        with col3:
            if st.button(f"🗑️ Elimina", key=f"del_{row['id']}"):
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    os.remove(row['foto_path'])
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM chitarre WHERE id = ?", (row['id'],))
                conn.commit()
                conn.close()
                st.rerun()
else:
    st.info("Vault vuoto. Aggiungi il tuo primo strumento!")