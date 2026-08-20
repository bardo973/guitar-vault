import streamlit as st
import json
import os
import base64
from datetime import datetime
from PIL import Image

# 1. Configurazione Pagina
st.set_page_config(
    page_title="Guitar Rack & Vault",
    page_icon="🎸",
    layout="wide"
)

DB_FILE = "vault_data.json"
UPLOAD_DIR = "uploads"

# Nome del file immagine dello sfondo nella cartella del progetto
BG_IMAGE_PATH = "IMG_20210104_160719.jpg" 

# Crea la cartella per le immagini se non esiste
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- FUNZIONE PER SETTARE LO SFONDO DA FILE LOCALE ---
# ─── TEMA HENDRIX / PSICHEDELICO ───
# ─── TEMA ELEGANTE NERO & ARGENTO ───
def set_elegant_theme(bg_image_path=None):
    """Tema elegante nero/argento con pennellate."""

    SILVER = "#C0C0C0"
    SILVER_LIGHT = "#E8E8E8"
    SILVER_DARK = "#707070"
    GOLD_ACCENT = "#B8860B"
    BLACK = "#0a0a0a"
    CHARCOAL = "#1a1a1a"

    base_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap');

    .stApp {{
        background: linear-gradient(160deg, #0a0a0a 0%, #141414 40%, #1a1a1a 70%, #0f0f0f 100%);
        background-attachment: fixed;
    }}

    """

    if bg_image_path and os.path.exists(bg_image_path):
        with open(bg_image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        base_css += f"""
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        opacity: 0.12;
        z-index: -1;
        pointer-events: none;
        filter: grayscale(60%) contrast(1.2);
    }}
    """

    base_css += f"""
    /* Header elegante */
    [data-testid="stHeader"] {{
        background: linear-gradient(90deg, #0a0a0a, #1a1a1a, #0a0a0a) !important;
        border-bottom: 1px solid {SILVER_DARK}40 !important;
    }}

    /* Titolo principale - elegante serif */
    h1 {{
        font-family: 'Cinzel', serif !important;
        color: {SILVER_LIGHT} !important;
        text-shadow: 0 2px 10px rgba(192,192,192,0.3), 0 0 40px rgba(192,192,192,0.1) !important;
        letter-spacing: 6px !important;
        font-size: 2.6rem !important;
        text-align: center !important;
        margin-bottom: 0.3rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
    }}

    /* Sottotitolo */
    h2 {{
        font-family: 'Playfair Display', serif !important;
        color: {SILVER} !important;
        letter-spacing: 2px !important;
        font-weight: 400 !important;
        font-style: italic !important;
    }}

    h3 {{
        font-family: 'Playfair Display', serif !important;
        color: {SILVER_DARK} !important;
        letter-spacing: 1px !important;
        font-weight: 400 !important;
    }}

    /* Pennellata dietro i nomi delle chitarre (nelle card) */
    div[data-testid="stVerticalBlock"] h3,
    div[data-testid="stVerticalBlock"] h4,
    .stMarkdown h3 {{
        position: relative;
        display: inline-block;
        padding: 4px 16px;
        margin-bottom: 12px;
    }}

    div[data-testid="stVerticalBlock"] h3::before,
    div[data-testid="stVerticalBlock"] h4::before {{
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 50%;
        height: 70%;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(192,192,192,0.15) 15%, 
            rgba(192,192,192,0.25) 50%, 
            rgba(192,192,192,0.15) 85%, 
            transparent 100%);
        transform: translateY(-50%) skewX(-8deg);
        border-radius: 2px;
        z-index: -1;
        filter: blur(1px);
    }}

    /* Testo generale */
    p, label, .stMarkdown {{
        color: {SILVER_DARK} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
        letter-spacing: 0.3px !important;
    }}

    /* Metriche argento */
    div[data-testid="stMetricValue"] {{
        color: {SILVER_LIGHT} !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(192,192,192,0.2) !important;
        font-size: 1.8rem !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {SILVER_DARK} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
    }}

    /* Bottoni elegante */
    .stButton > button {{
        background: linear-gradient(145deg, #141414, #0a0a0a) !important;
        color: {SILVER} !important;
        border: 1px solid {SILVER_DARK}80 !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stButton > button:hover {{
        border-color: {SILVER} !important;
        box-shadow: 0 0 20px rgba(192,192,192,0.15), 0 4px 12px rgba(0,0,0,0.6) !important;
        color: {SILVER_LIGHT} !important;
        transform: translateY(-1px) !important;
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(145deg, #1a1a1a, #0f0f0f) !important;
        border: 1px solid {SILVER}60 !important;
    }}

    .stButton > button[kind="primary"]:hover {{
        border-color: {SILVER_LIGHT} !important;
        box-shadow: 0 0 25px rgba(192,192,192,0.2) !important;
    }}

    /* Card / Container - vetro nero */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(15, 15, 15, 0.85) !important;
        backdrop-filter: blur(20px) saturate(1.2) !important;
        border: 1px solid rgba(192,192,192,0.12) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.03) !important;
    }}

    /* Sidebar elegante */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a0a0a 0%, #111111 50%, #0a0a0a 100%) !important;
        border-right: 1px solid rgba(192,192,192,0.1) !important;
    }}

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        color: {SILVER} !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 3px !important;
    }}

    /* Input eleganti */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid rgba(192,192,192,0.15) !important;
        color: {SILVER_LIGHT} !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {SILVER} !important;
        box-shadow: 0 0 12px rgba(192,192,192,0.1) !important;
    }}

    /* File uploader */
    .stFileUploader > div {{
        background: rgba(15, 15, 15, 0.8) !important;
        border: 1px dashed rgba(192,192,192,0.2) !important;
        border-radius: 8px !important;
    }}

    /* Tabelle */
    .stDataFrame {{
        background: rgba(10, 10, 10, 0.9) !important;
    }}

    /* Scrollbar elegante */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: #0a0a0a;
    }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {SILVER_DARK}, {SILVER}40, {SILVER_DARK});
        border-radius: 3px;
    }}

    /* Divider argento sottile */
    hr {{
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(192,192,192,0.3), transparent) !important;
        margin: 2rem 0 !important;
    }}

    /* Radio buttons */
    .stRadio > div {{
        background: rgba(15, 15, 15, 0.6) !important;
        border-radius: 6px !important;
        padding: 8px !important;
        border: 1px solid rgba(192,192,192,0.08) !important;
    }}

    /* Caption */
    .stCaption {{
        color: {SILVER_DARK} !important;
        font-style: italic !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* Warning / Info / Error - toni sobri */
    .stAlert {{
        background: rgba(20, 20, 20, 0.9) !important;
        border-left: 3px solid {SILVER_DARK} !important;
    }}

    /* Immagini nelle card - bordo argento sottile */
    img {{
        border-radius: 4px !important;
        border: 1px solid rgba(192,192,192,0.1) !important;
    }}

    /* Tab selezionato */
    button[data-baseweb="tab"] {{
        color: {SILVER_DARK} !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 1px !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {SILVER_LIGHT} !important;
        border-bottom: 2px solid {SILVER} !important;
    }}
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)

# Applica il tema elegante
set_elegant_theme(BG_IMAGE_PATH)
# Dati di partenza (usati solo al primissimo avvio se non esiste vault_data.json)
DEFAULT_GUITARS = [
    {
        "id": "g-1",
        "brand": "Fender",
        "model": "American Professional II Stratocaster",
        "year": 2021,
        "serialNumber": "US210984",
        "factory": "Corona, USA",
        "condition": "Mint",
        "pricePaid": 1850,
        "marketValue": 1950,
        "body": "Alder con finitura Gloss Urethane",
        "neckWood": "Acero, Bolt-On",
        "fretboard": "Palissandro, 22 tasti",
        "pickups": "SSS - 3x V-Mod II Single-Coil",
        "hardware": "Tremolo 2 punti",
        "stringGauge": "0.010-0.046",
        "lastSetup": "2026-03-10",
        "notes": "Azione molto bassa, setup Mi Standard",
        "imagePath": ""
    }
]

# 2. Funzioni di Salvataggio e Gestione Dati
def load_data():
    if not os.path.exists(DB_FILE):
        save_data(DEFAULT_GUITARS)
        return DEFAULT_GUITARS
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_GUITARS

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_image(uploaded_file, guitar_id):
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1]
        filename = f"{guitar_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        img = Image.open(uploaded_file)
        img.thumbnail((1200, 1200))
        img.save(file_path)
        return file_path
    return ""

# Inizializzazione Session State
if "guitars" not in st.session_state:
    st.session_state.guitars = load_data()

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "editing_guitar_id" not in st.session_state:
    st.session_state.editing_guitar_id = None

# Controllo se il setup è scaduto (> 120 giorni)
def is_overdue(date_str):
    if not date_str:
        return True
    try:
        setup_date = datetime.strptime(date_str, "%Y-%m-%d")
        diff_days = (datetime.now() - setup_date).days
        return diff_days > 120
    except:
        return False

# --- SIDEBAR: BACKUP & INTEGRITÀ DATI ---
with st.sidebar:
    st.header("🎸 Gestione Vault")

    # Carica sfondo personalizzato
    st.markdown("---")
    st.subheader("🖼️ Sfondo")
    bg_upload = st.file_uploader("Carica foto sfondo (Jimi, concerto, etc.)", type=["jpg", "jpeg", "png"], key="bg_upload")
    if bg_upload is not None:
        bg_path = os.path.join(UPLOAD_DIR, "custom_bg" + os.path.splitext(bg_upload.name)[1])
        with open(bg_path, "wb") as f:
            f.write(bg_upload.read())
        st.success("Sfondo caricato! Ricarica la pagina.")
        st.rerun()

    if st.button("🎨 Tema Psichedelico (senza foto)", use_container_width=True):
        # Rimuovi sfondo custom se esiste
        for ext in [".jpg", ".jpeg", ".png"]:
            p = os.path.join(UPLOAD_DIR, "custom_bg" + ext)
            if os.path.exists(p):
                os.remove(p)
        st.rerun()

    st.markdown("---")
    
    # ─── DOWNLOAD BACKUP ZIP (JSON + FOTO) ───
    import io, zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Aggiungi JSON
        json_data = json.dumps(st.session_state.guitars, indent=4, ensure_ascii=False)
        zf.writestr("vault_data.json", json_data)
        # Aggiungi tutte le foto presenti in uploads/
        foto_count = 0
        for g in st.session_state.guitars:
            img_path = g.get("imagePath", "")
            if img_path and os.path.exists(img_path):
                zf.write(img_path, arcname=os.path.basename(img_path))
                foto_count += 1
        # Aggiungi anche eventuali foto in uploads/ non referenziate (per sicurezza)
        if os.path.exists(UPLOAD_DIR):
            for fname in os.listdir(UPLOAD_DIR):
                fpath = os.path.join(UPLOAD_DIR, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    arcname = os.path.basename(fpath)
                    # Evita duplicati
                    if arcname not in [m.filename for m in zf.infolist()]:
                        zf.write(fpath, arcname=arcname)
                        foto_count += 1
    buf.seek(0)
    st.download_button(
        label="📥 Scarica Backup ZIP (con foto)",
        data=buf,
        file_name=f"vault_backup_{datetime.now().strftime('%Y%m%d')}.zip",
        mime="application/zip",
        use_container_width=True
    )
    st.caption(f"💾 {len(st.session_state.guitars)} chitarre + {foto_count} foto incluse")

    # ─── RIPRISTINO DA BACKUP ZIP ───
    uploaded_backup = st.file_uploader("📤 Ripristina da Backup ZIP", type=["zip"])
    if uploaded_backup is not None:
        if st.button("Sostituisci Database Attuale", type="primary", use_container_width=True):
            try:
                zip_bytes = io.BytesIO(uploaded_backup.read())
                with zipfile.ZipFile(zip_bytes, 'r') as zf:
                    file_list = zf.namelist()

                    # Trova e carica il JSON
                    json_name = None
                    if "vault_data.json" in file_list:
                        json_name = "vault_data.json"
                    else:
                        json_candidates = [n for n in file_list if n.endswith('.json')]
                        if json_candidates:
                            json_name = json_candidates[0]

                    if not json_name:
                        st.error("❌ Nessun file JSON trovato nel ZIP")
                        st.stop()

                    with zf.open(json_name) as f_json:
                        new_data = json.load(f_json)

                    # Estrai tutte le immagini in uploads/
                    foto_ripristinate = 0
                    for name in file_list:
                        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            dest = os.path.join(UPLOAD_DIR, os.path.basename(name))
                            with open(dest, 'wb') as f_out:
                                f_out.write(zf.read(name))
                            foto_ripristinate += 1

                    # Aggiorna session state e salva
                    st.session_state.guitars = new_data
                    save_data(new_data)
                    st.success(f"✅ Database ripristinato! {foto_ripristinate} foto ripristinate.")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Errore durante l'importazione: {e}")
                import traceback
                st.code(traceback.format_exc())
# --- UI MAIN APP ---
st.markdown("<h1 style='text-align:center;'>🎸 Guitar Rack & Vault 🎸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#707070; font-family:Inter; font-size:0.95rem; letter-spacing:2px; text-transform:uppercase;'>Collezione · Inventario · Manutenzione</p>", unsafe_allow_html=True)

# Controllo strumenti da manutenere
overdue_guitars = [g for g in st.session_state.guitars if is_overdue(g.get("lastSetup"))]

# Calcolo totale valore e investimento
total_market_val = sum(g.get("marketValue", 0) for g in st.session_state.guitars)
total_paid = sum(g.get("pricePaid", 0) for g in st.session_state.guitars)
delta_val = total_market_val - total_paid

# HUD Statistiche e Pulsante Aggiungi
col_stat1, col_stat2, col_stat3, col_btn = st.columns([1.5, 2, 2, 1.5])
col_stat1.metric("Totale Chitarre", len(st.session_state.guitars))
col_stat2.metric("Valore Stimato Vault", f"€ {total_market_val:,}", delta=f"€ {delta_val:+,} dal pagato")
col_stat3.metric("Cambio Corde URGENTE (>4 mesi)", len(overdue_guitars), delta_color="inverse")

with col_btn:
    st.write("")
    if st.button("➕ Aggiungi Chitarra", use_container_width=True, type="primary"):
        st.session_state.show_form = True
        st.session_state.editing_guitar_id = None
        st.rerun()

st.divider()

# 3. FORM GESTIONE (Visibile solo se richiesto)
if st.session_state.show_form:
    selected_guitar = None
    selected_idx = None
    
    if st.session_state.editing_guitar_id:
        for idx, g in enumerate(st.session_state.guitars):
            if g["id"] == st.session_state.editing_guitar_id:
                selected_guitar = g
                selected_idx = idx
                break

    with st.container(border=True):
        col_hdr, col_close = st.columns([4, 1])
        col_hdr.subheader("✏️ Modifica Chitarra" if selected_guitar else "➕ Nuova Chitarra")
        if col_close.button("❌ Chiudi Form", use_container_width=True):
            st.session_state.show_form = False
            st.session_state.editing_guitar_id = None
            st.rerun()

        with st.form("guitar_form", clear_on_submit=False):
            st.markdown("#### 📷 Foto dello Strumento")
            uploaded_photo = st.file_uploader("Carica una foto (da PC o scatta da iPhone)", type=["jpg", "jpeg", "png", "webp"])
            
            c1, c2, c3 = st.columns(3)
            brand = c1.text_input("Marca *", value=selected_guitar["brand"] if selected_guitar else "")
            model = c2.text_input("Modello *", value=selected_guitar["model"] if selected_guitar else "")
            year = c3.number_input("Anno di Produzione", min_value=1900, max_value=2030, value=int(selected_guitar.get("year", 2022)) if selected_guitar else 2022)
            
            c4, c5, c6 = st.columns(3)
            serial = c4.text_input("Numero di Serie", value=selected_guitar.get("serialNumber", "") if selected_guitar else "")
            factory = c5.text_input("Fabbrica / Origine", value=selected_guitar.get("factory", "") if selected_guitar else "")
            
            conditions = ["Mint", "Ottimo", "Buono", "Relic / Usurato", "Da restaurare"]
            cond_idx = conditions.index(selected_guitar.get("condition", "Ottimo")) if selected_guitar and selected_guitar.get("condition") in conditions else 1
            condition = c6.selectbox("Stato", conditions, index=cond_idx)
            
            c7, c8 = st.columns(2)
            price = c7.number_input("Prezzo Pagato (€)", min_value=0, value=int(selected_guitar.get("pricePaid", 0)) if selected_guitar else 0)
            market_val = c8.number_input("Valore Attuale (€)", min_value=0, value=int(selected_guitar.get("marketValue", 0)) if selected_guitar else 0)

            st.markdown("#### Specifiche Tecniche")
            s1, s2 = st.columns(2)
            body = s1.text_input("Body", value=selected_guitar.get("body", "") if selected_guitar else "")
            neck = s2.text_input("Manico / Profilo", value=selected_guitar.get("neckWood", "") if selected_guitar else "")
            
            s3, s4, s5 = st.columns(3)
            fretboard = s3.text_input("Tastiera", value=selected_guitar.get("fretboard", "") if selected_guitar else "")
            pickups = s4.text_input("Pickups", value=selected_guitar.get("pickups", "") if selected_guitar else "")
            hardware = s5.text_input("Hardware / Ponte", value=selected_guitar.get("hardware", "") if selected_guitar else "")

            st.markdown("#### Manutenzione")
            m1, m2, m3 = st.columns(3)
            gauge = m1.text_input("Scalatura Corde", value=selected_guitar.get("stringGauge", "") if selected_guitar else "")
            
            default_setup_date = datetime.now().date()
            if selected_guitar and selected_guitar.get("lastSetup"):
                try:
                    default_setup_date = datetime.strptime(selected_guitar["lastSetup"], "%Y-%m-%d").date()
                except:
                    pass
            setup_date = m2.date_input("Data Ultimo Setup", value=default_setup_date)
            notes = m3.text_input("Note", value=selected_guitar.get("notes", "") if selected_guitar else "")

            btn_label = "💾 Salva Modifiche" if selected_guitar else "➕ Salva Nuova Chitarra"
            submitted = st.form_submit_button(btn_label)

            if submitted:
                if brand and model:
                    guitar_id = selected_guitar["id"] if selected_guitar else f"g-{int(datetime.now().timestamp())}"
                    
                    image_path = selected_guitar.get("imagePath", "") if selected_guitar else ""
                    if uploaded_photo is not None:
                        image_path = save_image(uploaded_photo, guitar_id)

                    updated_data = {
                        "id": guitar_id,
                        "brand": brand,
                        "model": model,
                        "year": year,
                        "serialNumber": serial,
                        "factory": factory,
                        "condition": condition,
                        "pricePaid": price,
                        "marketValue": market_val,
                        "body": body,
                        "neckWood": neck,
                        "fretboard": fretboard,
                        "pickups": pickups,
                        "hardware": hardware,
                        "stringGauge": gauge,
                        "lastSetup": setup_date.strftime("%Y-%m-%d"),
                        "notes": notes,
                        "imagePath": image_path
                    }

                    if selected_guitar:
                        st.session_state.guitars[selected_idx] = updated_data
                        st.success(f"Modifiche a {brand} {model} salvate!")
                    else:
                        st.session_state.guitars.append(updated_data)
                        st.success(f"{brand} {model} aggiunta al Vault!")

                    save_data(st.session_state.guitars)
                    st.session_state.show_form = False
                    st.session_state.editing_guitar_id = None
                    st.rerun()
                else:
                    st.error("Inserisci almeno Marca e Modello.")

    st.divider()

# 4. Filtro e Visualizzazione Vault
st.subheader("📋 Lista Strumenti")

search_col, filter_col = st.columns([2, 2])
search_query = search_col.text_input("🔍 Cerca per marca, modello o seriale...", "").lower()

filter_option = filter_col.radio(
    "Filtra stato:",
    ["Tutte le chitarre", "⚠️ Solo quelle che necessitano cambio corde"],
    horizontal=True
)

displayed_guitars = st.session_state.guitars

if filter_option == "⚠️ Solo quelle che necessitano cambio corde":
    displayed_guitars = overdue_guitars

if search_query:
    displayed_guitars = [
        g for g in displayed_guitars 
        if search_query in g.get("brand", "").lower() 
        or search_query in g.get("model", "").lower() 
        or search_query in g.get("serialNumber", "").lower()
    ]

if not displayed_guitars:
    st.info("Nessuna chitarra trovata per i criteri selezionati.")

for g in displayed_guitars:
    overdue = is_overdue(g.get("lastSetup"))
    
    with st.container(border=True):
        col_img, col_info = st.columns([1, 3])
        
        with col_img:
            img_path = g.get("imagePath")
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.caption("📷 Nessuna foto presente")
        
        with col_info:
            brand = g['brand']
            model = g['model']
            year = g.get('year', 'N/D')
            st.markdown(f"""
            <div style="margin-bottom:8px;">
                <span style="font-family:'Cinzel',serif; font-size:1.1rem; color:#C0C0C0; letter-spacing:1px;">{brand}</span>
                <span style="position:relative; display:inline-block; padding:2px 12px; margin:0 6px; font-family:'Playfair Display',serif; font-size:1.3rem; color:#0a0a0a; font-weight:700; letter-spacing:0.5px;">
                    <span style="position:absolute; left:-4px; right:-4px; top:15%; bottom:15%; background:linear-gradient(90deg, rgba(218,165,32,0.85), rgba(255,215,0,0.9), rgba(218,165,32,0.85)); transform:skewX(-10deg); border-radius:2px; z-index:0; filter:blur(0.5px);"></span>
                    <span style="position:relative; z-index:1;">{model}</span>
                </span>
                <span style="font-family:'Cinzel',serif; font-size:0.9rem; color:#707070;">({year})</span>
            </div>
            """, unsafe_allow_html=True)
            
            if overdue:
                st.warning(f"⚠️ **Cambio corde/setup consigliato!** Ultimo: {g.get('lastSetup', 'Mai')}")
            else:
                st.success(f"✓ Setup in regola. Ultimo: {g.get('lastSetup', 'Mai')}")

            t1, t2, t3 = st.tabs(["Info & Valore", "Specifiche", "Manutenzione & Note"])
            
            with t1:
                st.write(f"**Serial Number:** `{g.get('serialNumber', 'N/D')}` | **Origine:** {g.get('factory', 'N/D')}")
                st.write(f"**Stato:** {g.get('condition')} | **Prezzo:** €{g.get('pricePaid')} | **Valore Stimato:** €{g.get('marketValue')}")
                
            with t2:
                st.write(f"**Body:** {g.get('body', 'N/D')}")
                st.write(f"**Manico:** {g.get('neckWood', 'N/D')}")
                st.write(f"**Tastiera:** {g.get('fretboard', 'N/D')}")
                st.write(f"**Pickups:** {g.get('pickups', 'N/D')}")
                st.write(f"**Hardware:** {g.get('hardware', 'N/D')}")
                
            with t3:
                st.write(f"**Scalatura Corde:** `{g.get('stringGauge', 'N/D')}`")
                st.write(f"**Note:** {g.get('notes', 'Nessuna nota')}")

            col_act1, col_act2, col_act3 = st.columns(3)
            
            if col_act1.button("✏️ Modifica", key=f"edit_{g['id']}"):
                st.session_state.show_form = True
                st.session_state.editing_guitar_id = g["id"]
                st.rerun()

            if col_act2.button("🔄 Segna Setup Oggi", key=f"setup_{g['id']}"):
                for item in st.session_state.guitars:
                    if item["id"] == g["id"]:
                        item["lastSetup"] = datetime.now().strftime("%Y-%m-%d")
                        break
                save_data(st.session_state.guitars)
                st.success("Setup aggiornato a oggi!")
                st.rerun()

            if col_act3.button("🗑️ Elimina", key=f"del_{g['id']}", type="primary"):
                if g.get("imagePath") and os.path.exists(g["imagePath"]):
                    try:
                        os.remove(g["imagePath"])
                    except:
                        pass
                st.session_state.guitars = [item for item in st.session_state.guitars if item["id"] != g["id"]]
                save_data(st.session_state.guitars)
                st.rerun()