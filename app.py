import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Guitar Vault", page_icon="🎸", layout="wide")

DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

# --- CSS E STILE ELEGANTE ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div.stButton > button { border-radius: 20px; transition: 0.3s; width: 100%; }
    .card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT, marca TEXT, modello TEXT, 
            serie TEXT, corde TEXT, data_cambio TEXT, prossimo_cambio TEXT, 
            foto_path TEXT, note TEXT)''')

init_db()

st.title("🎸 Guitar Vault")
st.markdown("Gestisci la tua collezione e la manutenzione dei tuoi strumenti.")

# --- SIDEBAR: AGGIUNTA ---
with st.sidebar:
    st.header("➕ Nuova Chitarra")
    with st.form("nuova_chitarra", clear_on_submit=True):
        marca = st.text_input("Marca")
        modello = st.text_input("Modello")
        serie = st.text_input("Numero di Serie")
        marca_corde = st.text_input("Marca Corde")
        scalatura_corde = st.text_input("Scalatura")
        note = st.text_area("Note / Lavorazioni eseguite")
        data_cambio = st.date_input("Data Ultimo Cambio", datetime.now())
        uploaded_file = st.file_uploader("Foto chitarra", type=['jpg', 'jpeg', 'png'])
        
        if st.form_submit_button("Aggiungi al Vault"):
            foto_path = None
            if uploaded_file:
                foto_path = os.path.join(IMG_DIR, f"{int(datetime.now().timestamp())}_{uploaded_file.name}")
                with open(foto_path, "wb") as f: f.write(uploaded_file.getbuffer())
            
            prossimo = data_cambio + timedelta(days=90)
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute('INSERT INTO chitarre VALUES (NULL,?,?,?,?,?,?,?,?)', 
                             (marca, modello, serie, f"{marca_corde} {scalatura_corde}", 
                              str(data_cambio), str(prossimo), foto_path, note))
            st.toast("Chitarra aggiunta correttamente!", icon="🎸")

# --- DASHBOARD & LISTA ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il vault è vuoto. Aggiungi la tua prima chitarra dalla sidebar!")
else:
    # Riepilogo veloce
    col_metric1, col_metric2 = st.columns(2)
    col_metric1.metric("Totale Strumenti", len(df))
    col_metric2.metric("Manutenzioni urgenti", len(df[df['prossimo_cambio'] <= str(datetime.now().date())]))

    st.divider()

    for _, row in df.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            cols = st.columns([1, 3, 1])
            
            with cols[0]:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], use_container_width=True)
                else:
                    st.write("📷")
            
            with cols[1]:
                st.subheader(f"{row['marca']} {row['modello']}")
                st.caption(f"S/N: {row['serie']}")
                st.write(f"**Corde:** {row['corde']}")
                
                # Note
                if row['note']:
                    st.info(f"📝 {row['note']}")
                
                # Data Scadenza
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                delta = (data_scadenza - datetime.now().date()).days
                
                if delta <= 0:
                    st.error(f"⚠️ Cambio corde scaduto da {abs(delta)} giorni")
                else:
                    st.write(f"📅 Prossimo cambio: **{row['prossimo_cambio']}** ({delta} giorni rimanenti)")
            
            with cols[2]:
                if st.button("✅ Cambio Eseguito", key=f"upd_{row['id']}"):
                    nuova_scadenza = datetime.now().date() + timedelta(days=90)
                    with sqlite3.connect(DB_NAME) as conn:
                        conn.execute("UPDATE chitarre SET data_cambio = ?, prossimo_cambio = ? WHERE id = ?", 
                                     (str(datetime.now().date()), str(nuova_scadenza), row['id']))
                    st.toast("Manutenzione registrata!", icon="🔧")
                    st.rerun()
                
                if st.button("🗑️ Elimina", key=f"del_{row['id']}"):
                    with sqlite3.connect(DB_NAME) as conn:
                        conn.execute("DELETE FROM chitarre WHERE id = ?", (row['id'],))
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)