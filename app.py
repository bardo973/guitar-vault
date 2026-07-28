import streamlit as st
import json
import os
import base64
import subprocess
from datetime import datetime
from PIL import Image

# 1. Configurazione Pagina
st.set_page_config(
    page_title="Digital Gear Vault & Rack",
    page_icon="🎸",
    layout="wide"
)

DB_FILE = "vault_data.json"
UPLOAD_DIR = "uploads"
BG_IMAGE_PATH = "IMG_20210104_160719.jpg" 

# Crea la cartella per le immagini se non esiste
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- FUNZIONE PER SETTARE LO SFONDO DA FILE LOCALE ---
def set_custom_background(image_file):
    target_file = image_file if os.path.exists(image_file) else "background.jpg"
    if os.path.exists(target_file):
        with open(target_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        
        css = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0) !important; }}
        .stMarkdown, p, h1, h2, h3, label {{ color: #ffffff !important; }}
        div[data-testid="stMetricValue"] {{ color: #f0a500 !important; }}
        .stTabs [data-baseweb="tab"] {{ color: #ffffff !important; }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

set_custom_background(BG_IMAGE_PATH)

# Dati di partenza universali (Chitarre, Amplificatori, Modeller, Effetti)
DEFAULT_GEAR = [
    {
        "id": "g-1",
        "category": "🎸 Chitarre",
        "brand": "Fender",
        "model": "American Professional II Stratocaster",
        "year": 2021,
        "serialNumber": "US210984",
        "factory": "Corona, USA",
        "condition": "Mint",
        "pricePaid": 1850,
        "marketValue": 1950,
        "spec_1": "SSS - 3x V-Mod II Single-Coil",
        "spec_2": "Palissandro, 22 tasti",
        "lastSetup": "2026-03-10",
        "notes": "Azione molto bassa, setup Mi Standard",
        "imagePath": ""
    },
    {
        "id": "a-1",
        "category": "🔊 Amplificatori",
        "brand": "Marshall",
        "model": "JCM800 2203 (Testata)",
        "year": 1985,
        "serialNumber": "M12345",
        "factory": "UK",
        "condition": "Ottimo",
        "pricePaid": 1500,
        "marketValue": 2200,
        "spec_1": "Valvolare (EL34)",
        "spec_2": "100 Watt",
        "lastSetup": "2025-11-20",
        "notes": "Rivalvolata completamente a fine 2025",
        "imagePath": ""
    }
]

# 2. Funzioni di Salvataggio e Gestione Dati (Con Auto-Push su GitHub)
def load_data():
    if not os.path.exists(DB_FILE):
        save_data(DEFAULT_GEAR)
        return DEFAULT_GEAR
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_GEAR

def save_data(data):
    # 1. Salva localmente sul server Streamlit temporaneo
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    # 2. Git Push Automatico su GitHub per non perdere i dati al riavvio
    try:
        subprocess.run(["git", "config", "user.name", "Streamlit Gear Bot"], check=True)
        subprocess.run(["git", "config", "user.email", "bot@streamlit.com"], check=True)
        subprocess.run(["git", "add", DB_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update gear database [skip ci]"], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception as e:
        pass # Ignora gli errori se eseguito in locale senza Git configurato

def save_image(uploaded_file, gear_id):
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1]
        filename = f"{gear_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        img = Image.open(uploaded_file)
        img.thumbnail((1200, 1200))
        img.save(file_path)
        return file_path
    return ""

# Inizializzazione Session State
if "gear" not in st.session_state:
    st.session_state.gear = load_data()

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "editing_gear_id" not in st.session_state:
    st.session_state.editing_gear_id = None

def is_overdue(date_str):
    if not date_str: return True
    try:
        setup_date = datetime.strptime(str(date_str), "%Y-%m-%d")
        return (datetime.now() - setup_date).days > 120
    except:
        return False

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Gestione Hub")
    json_data = json.dumps(st.session_state.gear, indent=4, ensure_ascii=False)
    st.download_button(
        label="📥 Scarica Backup JSON",
        data=json_data,
        file_name=f"gear_backup_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )
    
    uploaded_backup = st.file_uploader("📤 Ripristina Backup JSON", type=["json"])
    if uploaded_backup is not None:
        if st.button("Sostituisci Database", type="primary", use_container_width=True):
            try:
                new_data = json.load(uploaded_backup)
                st.session_state.gear = new_data
                save_data(new_data)
                st.success("Database aggiornato!")
                st.rerun()
            except Exception as e:
                st.error(f"Errore: {e}")

# --- UI MAIN APP ---
st.title("🎸 Digital Gear Rack & Vault")
st.caption("Gestione inventario centralizzata per Chitarre, Amplificatori, Modeller e Pedalini")

overdue_items = [g for g in st.session_state.gear if is_overdue(g.get("lastSetup"))]
total_market_val = sum(g.get("marketValue", 0) for g in st.session_state.gear)
total_paid = sum(g.get("pricePaid", 0) for g in st.session_state.gear)
delta_val = total_market_val - total_paid

col_stat1, col_stat2, col_stat3, col_btn = st.columns([1.5, 2, 2, 1.5])
col_stat1.metric("Totale Strumenti", len(st.session_state.gear))
col_stat2.metric("Valore Totale Gear", f"€ {total_market_val:,}", delta=f"€ {delta_val:+,} dal pagato")
col_stat3.metric("Manutenzioni Scadute (>4 mesi)", len(overdue_items), delta_color="inverse")

with col_btn:
    st.write("")
    if st.button("➕ Aggiungi Strumento", use_container_width=True, type="primary"):
        st.session_state.show_form = True
        st.session_state.editing_gear_id = None
        st.rerun()

st.divider()

# 3. FORM GESTIONE DINAMICO
if st.session_state.show_form:
    selected_gear = None
    selected_idx = None
    
    if st.session_state.editing_gear_id:
        for idx, g in enumerate(st.session_state.gear):
            if g["id"] == st.session_state.editing_gear_id:
                selected_gear = g
                selected_idx = idx
                break

    with st.container(border=True):
        col_hdr, col_close = st.columns([4, 1])
        col_hdr.subheader("✏️ Modifica Strumento" if selected_gear else "➕ Inserisci Nuovo Strumento nel Rack")
        if col_close.button("❌ Chiudi Form", use_container_width=True):
            st.session_state.show_form = False
            st.session_state.editing_gear_id = None
            st.rerun()

        # Selezione categoria fuori dal form per rendere reattive le etichette delle specifiche
        categorie_lista = ["🎸 Chitarre", "🔊 Amplificatori", "🎛️ Modeller & Profiler", "🦶 Pedalini & Effetti"]
        cat_default_idx = categorie_lista.index(selected_gear["category"]) if selected_gear else 0
        category = st.selectbox("Categoria Strumento *", options=categorie_lista, index=cat_default_idx)

        # Adattamento etichette dinamiche
        if "Chitarre" in category:
            l_spec1, l_spec2, l_setup = "Configurazione Pickup", "Legno Tastiera / Manico", "Ultimo Setup / Cambio Corde"
        elif "Amplificatori" in category:
            l_spec1, l_spec2, l_setup = "Tipo Valvole o Stato Solido", "Potenza (Watt) / Coni", "Ultimo Cambio Valvole / Bias"
        elif "Modeller" in category:
            l_spec1, l_spec2, l_setup = "Tipo Hardware (Floor/Rack)", "Versione Firmware Installata", "Ultimo Aggiornamento Firmware / Backup"
        else:
            l_spec1, l_spec2, l_setup = "Tipo Effetto (Delay, OD, ecc.)", "Alimentazione Richiesta (V / mA)", "Ultima Verifica Cablaggio"

        with st.form("gear_form"):
            uploaded_photo = st.file_uploader("Carica una foto", type=["jpg", "jpeg", "png", "webp"])
            
            c1, c2, c3 = st.columns(3)
            brand = c1.text_input("Marca *", value=selected_gear["brand"] if selected_gear else "")
            model = c2.text_input("Modello *", value=selected_gear["model"] if selected_gear else "")
            year = c3.number_input("Anno", min_value=1900, max_value=2030, value=int(selected_gear.get("year", 2026)) if selected_gear else 2026)
            
            c4, c5 = st.columns(2)
            spec_1 = c4.text_input(l_spec1, value=selected_gear.get("spec_1", "") if selected_gear else "")
            spec_2 = c5.text_input(l_spec2, value=selected_gear.get("spec_2", "") if selected_gear else "")

            c6, c7, c8 = st.columns(3)
            serial = c6.text_input("Numero di Serie", value=selected_gear.get("serialNumber", "") if selected_gear else "")
            factory = c7.text_input("Fabbrica / Origine", value=selected_gear.get("factory", "") if selected_gear else "")
            condition = c8.selectbox("Condizioni", ["Mint", "Ottimo", "Buono", "Usurato", "Da riparare"], index=0)
            
            c9, c10, c11 = st.columns(3)
            price_paid = c9.number_input("Prezzo Pagato (€)", min_value=0, value=int(selected_gear.get("pricePaid", 0)) if selected_gear else 0)
