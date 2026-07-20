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

# --- STILE CSS (SFONDO HENDRIX E PERSONALIZZAZIONE) ---
hendrix_bg = "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)), url("{hendrix_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3, p, label, .stMarkdown {{
        color: #ffffff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# --- FUNZIONI DI SISTEMA ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS chitarre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_modello TEXT, modello TEXT, serie TEXT, anno TEXT,
                paese TEXT, marca_corde TEXT, spessore_corde TEXT,
                pickups TEXT, data_cambio TEXT, 
                prossimo_cambio TEXT, foto_path TEXT)""")

    # Migrazione colonne sicura per database esistenti
    cols = [
        ("tipo_modello", "TEXT"),
        ("pickups", "TEXT"),
        ("anno", "TEXT"),
        ("paese", "TEXT"),
    ]
    for col_name, col_type in cols:
        try:
            c.execute(f"ALTER TABLE chitarre ADD COLUMN {col_name} {col_type}")
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
        # Menu a tendina per il modello/tipologia principale di chitarra (inclusi Music Man e Harley Benton)
        tipo_modello = st.selectbox(
            "Tipologia Modello",
            [
                "Fender Stratocaster",
                "Fender Telecaster",
                "Gibson Les Paul",
                "Gibson SG",
                "Gibson ES-335",
                "Music Man",
                "Harley Benton",
                "Ibanez",
                "PRS",
                "Epiphone",
                "Squier",
                "Jackson",
                "ESP / LTD",
                "Acustica / Classica",
                "Altro Modello",
            ],
        )
        modello = st.text_input(
            "Nome Specifico / Edizione (es. Standard, Custom Shop)"
        )
        serie = st.text_input("Numero di Serie")
        anno = st.text_input("Anno di costruzione")
        paese = st.text_input("Paese di costruzione (es. USA, Giappone, Cina)")
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
                "INSERT INTO chitarre (tipo_modello, modello, serie, anno,"
                " paese, marca_corde, spessore_corde, pickups, data_cambio, prossimo_cambio,"
                " foto_path) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    tipo_modello,
                    modello,
                    serie,
                    anno,
                    paese,
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
    # --- MENU A TENDINA PER SELEZIONARE LA CHITARRA ---
    opzioni_chitarre = ["Tutte le chitarre"] + [
        f"{row.get('tipo_modello', 'Chitarra')} - {row['modello']} (S/N:"
        f" {row['serie']})"
        for _, row in df.iterrows()
    ]
    scelta_filtro = st.selectbox(
        "🔍 Seleziona o filtra strumento dal Vault:", opzioni_chitarre
    )

    # Filtro in base alla selezione
    if scelta_filtro != "Tutte le chitarre":
        serie_selezionata = scelta_filtro.split("S/N: ")[1].replace(")", "")
        df_filtrato = df[df["serie"] == serie_selezionata]
    else:
        df_filtrato = df

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizzazione delle chitarre filtrate
    for _, row in df_filtrato.iterrows():
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if row["foto_path"] and os.path.exists(row["foto_path"]):
                    st.image(row["foto_path"], use_container_width=True)
                else:
                    st.info("No Photo")
            with col2:
                titolo_principale = (
                    f"{row.get('tipo_modello', '')} {row['modello']}".strip()
                )
                st.subheader(f"{titolo_principale} ({row.get('anno', '-')})")
                st.write(f"**S/N:** {row['serie']}")
                st.write(
                    f"**Paese di costruzione:** {row.get('paese', '-')}"
                )
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