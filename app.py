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
    # Aggiunto campo spessore
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT, serie TEXT, corde TEXT, 
            spessore TEXT, data_cambio TEXT, 
            prossimo_cambio TEXT, foto_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Guitar Vault Pro", layout="wide")
st.title("🎸 Guitar Vault Pro")

# --- LOGICA SALVATAGGIO ---
def save_guitar(modello, serie, corde, spessore, data_cambio, foto, guitar_id=None):
    foto_path = None
    if foto:
        foto_path = os.path.join(IMG_DIR, f"{serie}_{foto.name}")
        with open(foto_path, "wb") as f:
            f.write(foto.getbuffer())
            
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    prossimo = data_cambio + timedelta(days=90)
    
    if guitar_id:
        c.execute("UPDATE chitarre SET modello=?, serie=?, corde=?, spessore=?, data_cambio=?, prossimo_cambio=? WHERE id=?",
                  (modello, serie, corde, spessore, str(data_cambio), str(prossimo), guitar_id))
    else:
        c.execute("INSERT INTO chitarre (modello, serie, corde, spessore, data_cambio, prossimo_cambio, foto_path) VALUES (?,?,?,?,?,?,?)",
                  (modello, serie, corde, spessore, str(data_cambio), str(prossimo), foto_path))
    conn.commit()
    conn.close()

# --- SIDEBAR: AGGIUNTA ---
with st.sidebar.expander("➕ Nuova Chitarra"):
    with st.form("nuovo_form", clear_on_submit=True):
        m = st.text_input("Modello")
        s = st.text_input("S/N")
        c = st.text_input("Marca Corde")
        sp = st.text_input("Spessore (es. .010-.046)")
        d = st.date_input("Ultimo Cambio")
        f = st.file_uploader("Foto", type=["jpg", "png"])
        if st.form_submit_button("Salva"):
            save_guitar(m, s, c, sp, d, f)
            st.rerun()

# --- VISUALIZZAZIONE ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

for _, row in df.iterrows():
    with st.container(border=True):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if row['foto_path'] and os.path.exists(row['foto_path']):
                st.image(row['foto_path'], width=200)
        with c2:
            st.subheader(row['modello'])
            st.write(f"**S/N:** {row['serie']} | **Corde:** {row['corde']} ({row['spessore']})")
            st.caption(f"Ultimo cambio: {row['data_cambio']}")
        with c3:
            # Tasto Modifica
            with st.popover("⚙️ Modifica"):
                with st.form(f"edit_{row['id']}"):
                    new_m = st.text_input("Modello", value=row['modello'])
                    new_s = st.text_input("S/N", value=row['serie'])
                    new_c = st.text_input("Corde", value=row['corde'])
                    new_sp = st.text_input("Spessore", value=row['spessore'])
                    if st.form_submit_button("Aggiorna"):
                        save_guitar(new_m, new_s, new_c, new_sp, datetime.now(), None, guitar_id=row['id'])
                        st.rerun()
            
            if st.button("Rimuovi", key=f"del_{row['id']}"):
                conn = sqlite3.connect(DB_NAME)
                conn.execute("DELETE FROM chitarre WHERE id=?", (row['id'],))
                conn.commit()
                conn.close()
                st.rerun()