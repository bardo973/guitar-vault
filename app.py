import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configurazione database
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
            corde_marca TEXT,
            corde_spessore TEXT,
            anno INTEGER,
            valore REAL,
            data_cambio TEXT,
            prossimo_cambio TEXT,
            foto_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Guitar Vault", layout="wide")
st.title("🎸 Il mio Guitar Vault")

# --- SEZIONE INSERIMENTO ---
with st.sidebar.expander("➕ Aggiungi una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        anno = st.number_input("Anno di costruzione", min_value=1900, max_value=2100, value=2024)
        valore = st.number_input("Valore (€)", min_value=0.0, value=0.0)
        marca_corde = st.text_input("Marca Corde")
        spessore = st.text_input("Spessore (es. 10-46)")
        data_cambio = st.date_input("Ultimo Cambio Corde", datetime.now())
        
        submit = st.form_submit_button("Salva nel Vault")
        
        if submit and modello:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO chitarre (modello, serie, anno, valore, corde_marca, corde_spessore, data_cambio, prossimo_cambio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (modello, serie, anno, valore, marca_corde, spessore, str(data_cambio), str(data_cambio + timedelta(days=90))))
            conn.commit()
            conn.close()
            st.rerun()

conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Vault vuoto. Aggiungi uno strumento!")
else:
    for _, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(f"### {row['modello']}")
                st.write(f"📅 **Anno:** {row['anno']}")
                st.write(f"💰 **Valore:** € {row['valore']:,.2f}")
            with col2:
                st.write(f"🧵 **Corde:** {row['corde_marca']} ({row['corde_spessore']})")
                st.write(f"🆔 **S/N:** {row['serie']}")
            with col3:
                # Tasto Modifica semplificato
                if st.button(f"✏️ Modifica {row['id']}", key=f"edit_{row['id']}"):
                    st.warning("Funzionalità modifica attivata nel database.")
                
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                if data_scadenza <= datetime.now().date():
                    st.error("Cambio corde necessario!")
                else:
                    st.success("Corde OK")
            st.markdown("---")