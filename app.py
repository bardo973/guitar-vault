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
    # Aggiornamento schema per includere marca e spessore
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT,
            serie TEXT,
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
st.title("🎸 Il mio Guitar Vault")

# --- SEZIONE INSERIMENTO ---
with st.sidebar.expander("➕ Aggiungi una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        marca = st.text_input("Marca Corde")
        spessore = st.text_input("Spessore Corde (es. 10-46)")
        data_cambio = st.date_input("Data Ultimo Cambio", datetime.now())
        prossimo_cambio = st.date_input("Data Prossimo Cambio", data_cambio + timedelta(days=90))
        foto = st.file_uploader("Foto", type=["jpg", "jpeg", "png"])
        
        submit = st.form_submit_button("Salva nel Vault")
        
        if submit and modello:
            foto_path = ""
            if foto is not None:
                foto_path = os.path.join(IMG_DIR, f"{serie}_{foto.name}")
                with open(foto_path, "wb") as f:
                    f.write(foto.getbuffer())
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO chitarre (modello, serie, marca_corde, spessore_corde, data_cambio, prossimo_cambio, foto_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (modello, serie, marca, spessore, str(data_cambio), str(prossimo_cambio), foto_path))
            conn.commit()
            conn.close()
            st.rerun()

# --- VISUALIZZAZIONE ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Vault vuoto. Aggiungi la tua prima chitarra!")
else:
    for index, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], use_column_width=True)
            with col2:
                st.subheader(row['modello'])
                st.write(f"**Serial:** {row['serie']}")
                
                # Visualizzazione nativa dei dettagli corde
                c1, c2, c3 = st.columns(3)
                c1.metric("Marca Corde", row['marca_corde'] or "-")
                c2.metric("Spessore", row['spessore_corde'] or "-")
                c3.caption(f"Ultimo cambio: {row['data_cambio']}")
                
                if st.button(f"✏️ Modifica {row['modello']}", key=f"edit_{row['id']}"):
                    st.warning("Funzione modifica in arrivo!")
            st.divider()