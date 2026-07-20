from datetime import datetime, timedelta
import os
import sqlite3
import pandas as pd
import streamlit as st

# Configurazione pagina
st.set_page_config(
    page_title="Guitar Vault", layout="wide", initial_sidebar_state="expanded"
)

# Configurazione database e cartelle
DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"
if not os.path.exists(IMG_DIR):
  os.makedirs(IMG_DIR)


# --- FUNZIONI DI SISTEMA ---
def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute("""CREATE TABLE IF NOT EXISTS chitarre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modello TEXT, serie TEXT, anno TEXT,
                marca_corde TEXT, spessore_corde TEXT,
                pickups TEXT, data_cambio TEXT, 
                prossimo_cambio TEXT, foto_path TEXT)""")

  # Migrazione colonne sicura
  cols = ["pickups", "anno"]
  for col in cols:
    try:
      c.execute(f"ALTER TABLE chitarre ADD COLUMN {col} TEXT")
    except:
      pass
  conn.commit()
  conn.close()


init_db()

# --- SIDEBAR (INPUT) ---
with st.sidebar:
  if os.path.exists("logo.png"):
    st.image("logo.png", width=200)
  st.markdown("## 🎸 Nuovo Strumento")
  with st.form("nuova_chitarra", clear_on_submit=True):
    modello = st.text_input("Modello")
    serie = st.text_input("Numero di Serie")
    anno = st.text_input("Anno di costruzione")
    marca = st.text_input("Marca Corde")
    spessore = st.selectbox(
        "Scalatura Corde",
        ["008", "009", "010", "011", "012", "013", "Altro"],
    )
    pickups = st.text_input("Pick-up montati")
    data_cambio = st.date_input("Data ultimo cambio", datetime.now())
    foto = st.file_uploader("Carica Foto", type=["jpg", "png", "jpeg"])

    if st.form_submit_button("Salva nel Vault"):
      foto_path = ""
      if foto:
        foto_path = os.path.join(IMG_DIR, f"{serie}_{foto.name}")
        with open(foto_path, "wb") as f:
          f.write(foto.getbuffer())

      conn = sqlite3.connect(DB_NAME)
      c = conn.cursor()
      prossimo = data_cambio + timedelta(days=90)
      c.execute(
          "INSERT INTO chitarre (modello, serie, anno, marca_corde,"
          " spessore_corde, pickups, data_cambio, prossimo_cambio, foto_path)"
          " VALUES (?,?,?,?,?,?,?,?,?)",
          (
              modello,
              serie,
              anno,
              marca,
              spessore,
              pickups,
              str(data_cambio),
              str(prossimo),
              foto_path,
          ),
      )
      conn.commit()
      conn.close()
      st.rerun()

# --- INTERFACCIA PRINCIPALE ---
st.title("🎸 Guitar Vault Premium")
st.markdown("---")

conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if not df.empty:
  for _, row in df.iterrows():
    # Creiamo un container elegante per ogni chitarra
    with st.container(border=True):
      col1, col2, col3 = st.columns([1, 2, 1])
      with col1:
        if row["foto_path"] and os.path.exists(row["foto_path"]):
          st.image(row["foto_path"], use_container_width=True)
        else:
          st.info("No Photo")
      with col2:
        st.subheader(f"{row['modello']} ({row.get('anno', '-')})")
        st.write(f"**S/N:** {row['serie']}")
        st.write(
            f"**Corde:** {row.get('marca_corde', '-')} |"
            f" {row.get('spessore_corde', '-')}"
        )
        st.write(f"**Pick-up:** {row.get('pickups', '-')}")
      with col3:
        scadenza = datetime.strptime(
            row["prossimo_cambio"], "%Y-%m-%d"
        ).date()
        if scadenza <= datetime.now().date():
          st.error(f"⚠️ Cambio corde scaduto: {row['prossimo_cambio']}")
        else:
          st.success(f"📅 Cambio previsto: {row['prossimo_cambio']}")

        if st.button(f"🗑️ Rimuovi chitarra", key=f"del_{row['id']}"):
          if row["foto_path"] and os.path.exists(row["foto_path"]):
            os.remove(row["foto_path"])
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute("DELETE FROM chitarre WHERE id = ?", (row["id"],))
          conn.commit()
          conn.close()
          st.rerun()
else:
  st.markdown("### Il tuo Vault è vuoto")
  st.write("Usa la barra laterale a sinistra per aggiungere la tua prima chitarra!")