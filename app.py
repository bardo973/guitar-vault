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
    # Aggiunta colonne marca, spessore e valore se non esistono
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT,
            serie TEXT,
            marca_corde TEXT,
            spessore TEXT,
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
    # Aggiunta colonne marca, spessore se non esistono
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT,
            serie TEXT,
            marca_corde TEXT,
            spessore TEXT,
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

with st.sidebar.expander("➕ Aggiungi una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        marca_corde = st.text_input("Marca Corde")
        spessore = st.text_input("Spessore (es. 10-46)")
        data_cambio = st.date_input("Ultimo Cambio Corde", datetime.now())
        
        submit = st.form_submit_button("Salva nel Vault")
        
        if submit and modello:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO chitarre (modello, serie, marca_corde, spessore, data_cambio, prossimo_cambio)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (modello, serie, marca_corde, spessore, str(data_cambio), str(data_cambio + timedelta(days=90))))
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
            col1, col2 = st.columns([1, 4])
            with col1:
                st.subheader(row['modello'])
            with col2:
                if st.button(f"✏️ Modifica {row['modello']}", key=f"edit_{row['id']}"):
                    st.toast(f"Modifica per {row['modello']} in arrivo.")
            
            # Griglia dettagli senza anno e senza valore
            d1, d2, d3 = st.columns(3)
            d1.write(f"**Marca Corde:**\n{row['marca_corde']}")
            d2.write(f"**Spessore:**\n{row['spessore']}")
            d3.write(f"**S/N:**\n{row['serie']}")
            
            st.markdown("---")