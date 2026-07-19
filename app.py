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
st.subheader("Gestisci la tua collezione e la manutenzione delle tue chitarre")

# --- SEZIONE INSERIMENTO ---
with st.sidebar.expander("➕ Aggiungi una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        modello = st.text_input("Modello della Chitarra")
        serie = st.text_input("Numero di Serie")
        corde = st.text_input("Corde Montate (Marca/Scalatura)")
        data_cambio = st.date_input("Data Ultimo Cambio Corde", datetime.now())
        
        # Calcolo automatico suggerito a 3 mesi di distanza
        prossimo_suggerito = data_cambio + timedelta(days=90)
        prossimo_cambio = st.date_input("Data Prossimo Cambio", prossimo_suggerito)
        
        foto = st.file_uploader("Carica una fotografia", type=["jpg", "jpeg", "png"])
        
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
                INSERT INTO chitarre (modello, serie, corde, data_cambio, prossimo_cambio, foto_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (modello, serie, corde, str(data_cambio), str(prossimo_cambio), foto_path))
            conn.commit()
            conn.close()
            st.success(f"{modello} aggiunta con successo!")
            st.rerun()

# --- SEZIONE VISUALIZZAZIONE ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il tuo vault è vuoto. Aggiungi la tua prima chitarra dal menu a sinistra!")
else:
    # Mostra le chitarre in una griglia di card
    for index, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], use_column_width=True)
                else:
                    st.image("https://via.placeholder.com/300x200.png?text=Nessuna+Foto", use_column_width=True)
            
            with col2:
                st.markdown(f"### {row['modello']}")
                st.markdown(f"**Serial Number:** `{row['serie']}`")
                st.markdown(f"**Corde attuali:** {row['corde']}")
            
            with col3:
                st.markdown("📅 **Manutenzione**")
                st.caption(f"Ultimo cambio: {row['data_cambio']}")
                
                # Evidenzia se le corde sono da cambiare
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                if data_scadenza <= datetime.now().date():
                    st.error(f"Cambiare corde entro il: {row['prossimo_cambio']}")
                else:
                    st.success(f"Prossimo cambio: {row['prossimo_cambio']}")
            
            st.markdown("---")