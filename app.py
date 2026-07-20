import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Creazione tabella con le colonne necessarie
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
    # Migrazione automatica: aggiunge colonne se mancanti
    cols = [col[1] for col in c.execute("PRAGMA table_info(chitarre)").fetchall()]
    if 'anno' not in cols: c.execute("ALTER TABLE chitarre ADD COLUMN anno TEXT")
    if 'marca_corde' not in cols: c.execute("ALTER TABLE chitarre ADD COLUMN marca_corde TEXT")
    if 'spessore_corde' not in cols: c.execute("ALTER TABLE chitarre ADD COLUMN spessore_corde TEXT")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Guitar Vault", layout="wide")
st.title("🎸 Guitar Vault")

with st.sidebar.expander("➕ Aggiungi Chitarra", expanded=True):
    with st.form("nuova_chitarra", clear_on_submit=True):
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        anno = st.text_input("Anno di Costruzione")
        marca = st.text_input("Marca Corde")
        spessore = st.text_input("Spessore Corde")
        data_cambio = st.date_input("Ultimo Cambio", datetime.now())
        foto = st.file_uploader("Foto", type=["jpg", "png"])
        
        if st.form_submit_button("Salva"):
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
        col1, col2 = st.columns([1, 3])
        with col1:
            if row['foto_path'] and os.path.exists(row['foto_path']):
                st.image(row['foto_path'], use_column_width=True)
            else:
                st.write("📷 No Photo")
        with col2:
            st.subheader(row['modello'])
            st.write(f"**S/N:** {row['serie']} | **Anno:** {row.get('anno', 'N/A')}")
            st.write(f"**Corde:** {row.get('marca_corde', 'N/A')} - **Spessore:** {row.get('spessore_corde', 'N/A')}")
            
            # Pulsante modifica (logica placeholder)
            if st.button(f"✏️ Modifica {row['modello']}", key=f"edit_{row['id']}"):
                st.info("Funzionalità modifica in manutenzione.")