import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURAZIONE ---
DB_NAME = "collezione_chitarre.db"

# --- STREAMING_CHUNK: Inizializzazione database ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabella chitarre con campi corretti per prezzi e dettagli
    c.execute('''CREATE TABLE IF NOT EXISTS chitarre (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marca TEXT, modello TEXT, serie TEXT, corde TEXT,
                    marca_corde TEXT, spessore_corde TEXT, 
                    valore REAL, anno INTEGER, note_setup TEXT, foto_path TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Guitar Vault Pro", layout="wide")

# --- STREAMING_CHUNK: Interfaccia e Logica ---
st.title("🎸 Guitar Vault Pro")

# Caricamento dati
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

# Visualizzazione card
for _, row in df.iterrows():
    with st.container():
        st.markdown(f"### {row['marca']} {row['modello']}")
        
        # Righe di dati pulite (usiamo colonne native per evitare HTML rotto)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Anno", row['anno'] or "N/D")
        col2.metric("Valore", f"€ {row['valore']:,.2f}" if row['valore'] else "N/D")
        col3.markdown(f"**Corde:** {row['marca_corde'] or 'N/D'}")
        col4.markdown(f"**Spessore:** {row['spessore_corde'] or 'N/D'}")
        
        st.markdown(f"**Note:** {row['note_setup']}")
        
        # Tasto Modifica
        if st.button(f"✏️ Modifica {row['modello']}", key=f"edit_{row['id']}"):
            st.session_state.edit_id = row['id']
            st.rerun()
        
        st.divider()

# --- STREAMING_CHUNK: Gestione Modifica ---
if 'edit_id' in st.session_state:
    st.sidebar.subheader("✏️ Modifica Strumento")
    # ... Qui andrebbe il form di edit collegato a st.session_state.edit_id