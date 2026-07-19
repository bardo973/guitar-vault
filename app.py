import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configurazione
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
            corde TEXT,
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

# --- FUNZIONI DI SUPPORTO ---
def delete_guitar(guitar_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM chitarre WHERE id = ?", (guitar_id,))
    conn.commit()
    conn.close()

# --- SIDEBAR: AGGIUNTA ---
with st.sidebar.expander("➕ Aggiungi una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra", clear_on_submit=True):
        marca = st.text_input("Marca")
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        corde = st.text_input("Corde (Marca)")
        corde = st.text_input("Corde (Scalatura)")
        data_cambio = st.date_input("Data Ultimo Cambio", datetime.now())
        submit = st.form_submit_button("Salva")
        
        if submit and modello:
            prossimo_cambio = data_cambio + timedelta(days=90)
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('INSERT INTO chitarre (modello, serie, corde, data_cambio, prossimo_cambio) VALUES (?,?,?,?,?)', 
                      (modello, serie, corde, str(data_cambio), str(prossimo_cambio)))
            conn.commit()
            conn.close()
            st.success("Aggiunta!")
            st.rerun()

# --- VISUALIZZAZIONE E AZIONI ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il vault è vuoto.")
else:
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.subheader(row['modello'])
                st.caption(f"S/N: {row['serie']}")
            
            with col2:
                st.write(f"**Corde:** {row['corde']}")
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                if data_scadenza <= datetime.now().date():
                    st.error(f"⚠️ Cambio necessario dal {row['prossimo_cambio']}")
                else:
                    st.info(f"📅 Prossimo cambio: {row['prossimo_cambio']}")
            
            with col3:
                # Bottone per aggiornare il cambio corde (reset data a oggi + 90gg)
                if st.button("Fatto! Cambio corde", key=f"btn_{row['id']}"):
                    nuovo_cambio = datetime.now().date()
                    nuova_scadenza = nuovo_cambio + timedelta(days=90)
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("UPDATE chitarre SET data_cambio = ?, prossimo_cambio = ? WHERE id = ?", 
                                 (str(nuovo_cambio), str(nuova_scadenza), row['id']))
                    conn.commit()
                    conn.close()
                    st.rerun()
                
                if st.button("Elimina", key=f"del_{row['id']}"):
                    delete_guitar(row['id'])
                    st.rerun()