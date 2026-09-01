import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64
import io, zipfile
from datetime import datetime, timedelta
from PIL import Image

# ═══════════════════════════════════════════════════════════
#  CONFIGURAZIONE PAGINA
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Guitar Rack & Vault Pro",
    page_icon="🎸",
    layout="wide"
)

DB_FILE = "vault_data.json"
UPLOAD_DIR = "uploads"
BG_IMAGE_PATH = "IMG_20210104_160719.jpg"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ═══════════════════════════════════════════════════════════
#  TEMA — CARATTERE VINTAGE / ROCK MIGLIORATO
# ═══════════════════════════════════════════════════════════
def set_rock_theme(bg_image_path=None):
    # Palette
    SILVER = "#C0C0C0"
    SILVER_LIGHT = "#E8E8E8"
    SILVER_DARK = "#707070"
    GOLD = "#B8860B"
    BLACK = "#0a0a0a"
    CRIMSON = "#8B0000"
    IVORY = "#FFFFF0"

    base_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&family=Roboto+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

    .stApp {{
        background: linear-gradient(160deg, #0a0a0a 0%, #111111 40%, #181818 70%, #0f0f0f 100%);
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
        opacity: 0.10;
        z-index: -1;
        pointer-events: none;
        filter: grayscale(50%) contrast(1.1) brightness(0.8);
    }}
    """

    base_css += f"""
    /* SCANLINE OVERLAY — look vintage amplificatore */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.08),
            rgba(0, 0, 0, 0.08) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 9999;
        opacity: 0.35;
    }}
    
    /* Keyframes */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes pulseRed {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4); }}
        50% {{ box-shadow: 0 0 0 10px rgba(244, 67, 54, 0); }}
    }}
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    @keyframes glowPulse {{
        0%, 100% {{ text-shadow: 0 0 10px rgba(192,192,192,0.3), 0 0 20px rgba(192,192,192,0.1); }}
        50% {{ text-shadow: 0 0 20px rgba(192,192,192,0.6), 0 0 40px rgba(192,192,192,0.2); }}
    }}

    [data-testid="stHeader"] {{
        background: linear-gradient(90deg, #0a0a0a, #151515, #0a0a0a) !important;
        border-bottom: 1px solid {SILVER_DARK}40 !important;
    }}
    
    /* TITOLI — Oswald bold, uppercase, spaziatura ampia, glow animato */
    h1 {{
        font-family: 'Oswald', sans-serif !important;
        color: {IVORY} !important;
        text-shadow: 0 2px 12px rgba(255,255,240,0.25), 0 0 50px rgba(255,255,240,0.08) !important;
        letter-spacing: 8px !important;
        font-size: 2.8rem !important;
        text-align: center !important;
        margin-bottom: 0.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        animation: glowPulse 3s ease-in-out infinite !important;
    }}
    h2 {{
        font-family: 'Oswald', sans-serif !important;
        color: {SILVER} !important;
        letter-spacing: 4px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        font-size: 1.4rem !important;
        animation: fadeInUp 0.6s ease-out !important;
    }}
    h3 {{
        font-family: 'Oswald', sans-serif !important;
        color: {SILVER_DARK} !important;
        letter-spacing: 3px !important;
        font-weight: 400 !important;
        text-transform: uppercase !important;
        font-size: 1.1rem !important;
    }}
    
    /* Pennellata dietro i nomi */
    div[data-testid="stVerticalBlock"] h3::before,
    div[data-testid="stVerticalBlock"] h4::before {{
        content: "";
        position: absolute;
        left: 0; right: 0; top: 50%;
        height: 70%;
        background: linear-gradient(90deg, transparent 0%, rgba(192,192,192,0.12) 15%, rgba(192,192,192,0.22) 50%, rgba(192,192,192,0.12) 85%, transparent 100%);
        transform: translateY(-50%) skewX(-8deg);
        border-radius: 2px;
        z-index: -1;
        filter: blur(1px);
    }}
    
    /* Testo generale — Inter pulito */
    p, label, .stMarkdown {{
        color: {SILVER_DARK} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
        letter-spacing: 0.3px !important;
        line-height: 1.6 !important;
    }}
    
    /* Metriche — Roboto Mono per look tecnico */
    div[data-testid="stMetricValue"] {{
        color: {SILVER_LIGHT} !important;
        font-family: 'Roboto Mono', monospace !important;
        font-weight: 500 !important;
        text-shadow: 0 0 15px rgba(192,192,192,0.2) !important;
        font-size: 1.8rem !important;
        letter-spacing: -1px !important;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {SILVER_DARK} !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 400 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
    }}
    
    /* Bottoni — stile vintage/rock con effetto pressione */
    .stButton > button {{
        background: linear-gradient(145deg, #141414, #0a0a0a) !important;
        color: {SILVER} !important;
        border: 1px solid {SILVER_DARK}80 !important;
        border-radius: 2px !important;
        font-family: 'Oswald', sans-serif !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }}
    .stButton > button::after {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
        transform: rotate(30deg);
        transition: all 0.5s;
    }}
    .stButton > button:hover::after {{
        left: 100%;
    }}
    .stButton > button:hover {{
        border-color: {SILVER_LIGHT} !important;
        box-shadow: 0 0 25px rgba(192,192,192,0.15), 0 6px 16px rgba(0,0,0,0.7) !important;
        color: {IVORY} !important;
        transform: translateY(-2px) !important;
    }}
    .stButton > button:active {{
        transform: translateY(1px) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.6) !important;
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(145deg, #1a1a1a, #0f0f0f) !important;
        border: 1px solid {SILVER}60 !important;
        box-shadow: 0 0 15px rgba(192,192,192,0.08) !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        box-shadow: 0 0 25px rgba(192,192,192,0.2), 0 6px 16px rgba(0,0,0,0.7) !important;
        border-color: {SILVER_LIGHT} !important;
    }}
    
    /* Card / Container — vetro scuro con animazione ingresso */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(15, 15, 15, 0.88) !important;
        backdrop-filter: blur(20px) saturate(1.2) !important;
        border: 1px solid rgba(192,192,192,0.10) !important;
        border-radius: 4px !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.02) !important;
        animation: fadeInUp 0.5s ease-out !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.7), 0 0 20px rgba(192,192,192,0.05), inset 0 1px 0 rgba(255,255,255,0.03) !important;
        border-color: rgba(192,192,192,0.18) !important;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a0a0a 0%, #111111 50%, #0a0a0a 100%) !important;
        border-right: 1px solid rgba(192,192,192,0.08) !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        color: {SILVER} !important;
        font-family: 'Oswald', sans-serif !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
    }}
    
    /* Input */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid rgba(192,192,192,0.12) !important;
        color: {SILVER_LIGHT} !important;
        border-radius: 2px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }}
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {SILVER}60 !important;
        box-shadow: 0 0 10px rgba(192,192,192,0.1) !important;
    }}
    .stFileUploader > div {{
        background: rgba(15, 15, 15, 0.8) !important;
        border: 1px dashed rgba(192,192,192,0.18) !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
    }}
    .stFileUploader > div:hover {{
        border-color: {SILVER}40 !important;
        background: rgba(20, 20, 20, 0.9) !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: #0a0a0a; }}
    ::-webkit-scrollbar-thumb {{ background: linear-gradient(180deg, {SILVER_DARK}, {SILVER}40, {SILVER_DARK}); border-radius: 3px; }}
    
    hr {{
        border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(192,192,192,0.25), transparent) !important;
        margin: 2rem 0 !important;
    }}
    
    /* Tabs */
    button[data-baseweb="tab"] {{ 
        color: {SILVER_DARK} !important; 
        font-family: 'Oswald', sans-serif !important; 
        letter-spacing: 2px !important; 
        text-transform: uppercase !important; 
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        position: relative;
    }}
    button[data-baseweb="tab"]:hover {{
        color: {SILVER} !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{ 
        color: {SILVER_LIGHT} !important; 
        border-bottom: 2px solid {SILVER} !important;
        text-shadow: 0 0 10px rgba(192,192,192,0.3) !important;
    }}
    
    /* Immagini */
    img {{ 
        border-radius: 2px !important; 
        border: 1px solid rgba(192,192,192,0.08) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    img:hover {{
        transform: scale(1.02);
        box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
        border-color: rgba(192,192,192,0.15) !important;
    }}
    
    /* Badge categorie migliorati */
    .cat-badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-family: 'Oswald', sans-serif;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 500;
        border: 1px solid;
        backdrop-filter: blur(4px);
        animation: fadeInUp 0.4s ease-out;
    }}
    
    /* Progress bar animata */
    .setup-bar-container {{
        width: 100%;
        height: 4px;
        background: #1a1a1a;
        border-radius: 2px;
        overflow: hidden;
        position: relative;
    }}
    .setup-bar-fill {{
        height: 100%;
        border-radius: 2px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .setup-bar-fill::after {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }}
    
    /* Alert metriche */
    .metric-urgent {{
        animation: pulseRed 2s infinite;
        border-radius: 4px;
        padding: 4px 8px;
    }}
    
    /* Galleria effetto Polaroid */
    .polaroid {{
        background: #141414;
        padding: 8px 8px 20px 8px;
        border-radius: 2px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(192,192,192,0.05);
    }}
    .polaroid:hover {{
        transform: translateY(-6px) rotate(0.5deg);
        box-shadow: 0 12px 32px rgba(0,0,0,0.6), 0 0 20px rgba(192,192,192,0.05);
    }}
    
    /* Wishlist card priority glow */
    .priority-high {{ box-shadow: 0 0 15px rgba(244, 67, 54, 0.15) !important; border-color: rgba(244, 67, 54, 0.3) !important; }}
    .priority-medium {{ box-shadow: 0 0 15px rgba(255, 193, 7, 0.1) !important; border-color: rgba(255, 193, 7, 0.2) !important; }}
    .priority-low {{ box-shadow: 0 0 15px rgba(76, 175, 80, 0.1) !important; border-color: rgba(76, 175, 80, 0.2) !important; }}
    
    /* Stagger animation per liste */
    .stagger-1 {{ animation-delay: 0.05s !important; }}
    .stagger-2 {{ animation-delay: 0.1s !important; }}
    .stagger-3 {{ animation-delay: 0.15s !important; }}
    .stagger-4 {{ animation-delay: 0.2s !important; }}
    .stagger-5 {{ animation-delay: 0.25s !important; }}
    .stagger-6 {{ animation-delay: 0.3s !important; }}
    
    /* Form container */
    div[data-testid="stForm"] {{
        background: rgba(10, 10, 10, 0.6) !important;
        border: 1px solid rgba(192,192,192,0.08) !important;
        border-radius: 4px !important;
        padding: 1rem !important;
    }}
    
    /* Expander */
    details {{
        background: rgba(15, 15, 15, 0.5) !important;
        border: 1px solid rgba(192,192,192,0.06) !important;
        border-radius: 2px !important;
    }}

    /* === CARD ANIMATE E LUCCICANTI === */
    @keyframes shimmerSpin {{ to {{ transform: rotate(360deg); }} }}
    .shimmer-card {{ position: relative; border-radius: 16px; padding: 2px; overflow: hidden; background: rgba(15,15,15,0.9); }}
    .shimmer-card::before {{ content: ""; position: absolute; inset: -100%; background: conic-gradient(from 0deg, transparent 0%, #f5d78e 12%, #fffbe8 20%, #c8c8d0 32%, transparent 45%, transparent 100%); opacity: 0; transition: opacity 0.5s; animation: shimmerSpin 3.5s linear infinite; }}
    .shimmer-card:hover::before {{ opacity: 1; }}
    .shimmer-card-inner {{ position: relative; border-radius: 14px; background: rgba(10,10,10,0.95); padding: 32px; border: 1px solid rgba(192,192,192,0.1); }}
    .spotlight-card {{ position: relative; overflow: hidden; border-radius: 16px; border: 1px solid rgba(192,192,192,0.1); background: rgba(10,10,10,0.95); padding: 32px; transition: border-color 0.5s; }}
    .spotlight-card:hover {{ border-color: rgba(255,255,255,0.25); }}
    .spotlight-card::before {{ content: ""; position: absolute; inset: 0; background: radial-gradient(340px circle at var(--mx, 50%) var(--my, 50%), rgba(245,215,142,0.18), rgba(255,255,255,0.06) 40%, transparent 70%); opacity: 0; transition: opacity 0.3s; pointer-events: none; }}
    .spotlight-card:hover::before {{ opacity: 1; }}
    @keyframes sparklePulse {{ 0%, 100% {{ opacity: 0; transform: scale(0.4); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}
    .sparkle-card {{ position: relative; overflow: hidden; border-radius: 16px; border: 1px solid rgba(192,192,192,0.1); background: rgba(10,10,10,0.95); padding: 32px; transition: border-color 0.5s; }}
    .sparkle-card:hover {{ border-color: rgba(255,255,255,0.25); }}
    .sparkle-particle {{ position: absolute; border-radius: 50%; background: #f5d78e; box-shadow: 0 0 8px 2px rgba(245,215,142,0.7); animation: sparklePulse 2s ease-in-out infinite paused; }}
    .sparkle-card:hover .sparkle-particle {{ animation-play-state: running; }}
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)

set_rock_theme(BG_IMAGE_PATH)

# ═══════════════════════════════════════════════════════════
#  DATI DEFAULT & MIGRAZIONE
# ═══════════════════════════════════════════════════════════
DEFAULT_GUITARS = [
    {
        "id": "g-1",
        "brand": "Fender",
        "model": "American Professional II Stratocaster",
        "category": "Elettrica",
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
        "imagePath": "",
        "maintenanceLog": []
    }
]

DEFAULT_WISHLIST = []

# ─── Gestione Dati con Migrazione Legacy ───
def load_data():
    if not os.path.exists(DB_FILE):
        payload = {"guitars": DEFAULT_GUITARS, "wishlist": DEFAULT_WISHLIST}
        save_data(payload)
        return payload
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            for g in raw:
                if "category" not in g: g["category"] = "Elettrica"
                if "maintenanceLog" not in g: g["maintenanceLog"] = []
            payload = {"guitars": raw, "wishlist": DEFAULT_WISHLIST}
            save_data(payload)
            return payload
        if "guitars" not in raw: raw["guitars"] = []
        if "wishlist" not in raw: raw["wishlist"] = []
        for g in raw["guitars"]:
            if "category" not in g: g["category"] = "Elettrica"
            if "maintenanceLog" not in g: g["maintenanceLog"] = []
        for w in raw.get("wishlist", []):
            if "imagePath" not in w: w["imagePath"] = ""
        return raw
    except Exception:
        return {"guitars": DEFAULT_GUITARS, "wishlist": DEFAULT_WISHLIST}

def save_data(payload):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)

def save_image(uploaded_file, item_id, prefix=""):
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1]
        filename = f"{prefix}{item_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        img = Image.open(uploaded_file)
        img.thumbnail((1200, 1200))
        img.save(file_path)
        return file_path
    return ""

# Inizializzazione Session State
if "db" not in st.session_state:
    st.session_state.db = load_data()
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "editing_guitar_id" not in st.session_state:
    st.session_state.editing_guitar_id = None
if "show_wishlist_form" not in st.session_state:
    st.session_state.show_wishlist_form = False
if "editing_wish_id" not in st.session_state:
    st.session_state.editing_wish_id = None

def get_guitars():
    return st.session_state.db.get("guitars", [])

def get_wishlist():
    return st.session_state.db.get("wishlist", [])

def set_guitars(glist):
    st.session_state.db["guitars"] = glist
    save_data(st.session_state.db)

def set_wishlist(wlist):
    st.session_state.db["wishlist"] = wlist
    save_data(st.session_state.db)

# ═══════════════════════════════════════════════════════════
#  UTILITÀ
# ═══════════════════════════════════════════════════════════
CATEGORY_COLORS = {
    "Elettrica": "#C0C0C0",
    "Acustica": "#D2691E",
    "Classica": "#CD853F",
    "Basso": "#4682B4",
    "Altro": "#808080"
}
CATEGORY_EMOJI = {
    "Elettrica": "⚡", "Acustica": "🎵", "Classica": "🎼", "Basso": "🎶", "Altro": "🎹"
}

def is_overdue(date_str, threshold=120):
    if not date_str:
        return True
    try:
        setup_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - setup_date).days > threshold
    except:
        return False

def days_since(date_str):
    if not date_str:
        return 999
    try:
        return (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d")).days
    except:
        return 999

def maintenance_status(g):
    d = days_since(g.get("lastSetup"))
    if d > 120:
        return "overdue", d
    elif d > 90:
        return "warning", d
    return "ok", d

def fmt_currency(v):
    return f"€ {int(v):,}"

# ═══════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.header("🎸 Gestione Vault")

    st.markdown("---")
    st.subheader("🖼️ Sfondo")
    bg_upload = st.file_uploader("Carica foto sfondo", type=["jpg", "jpeg", "png"], key="bg_upload")
    if bg_upload is not None:
        bg_path = os.path.join(UPLOAD_DIR, "custom_bg" + os.path.splitext(bg_upload.name)[1])
        with open(bg_path, "wb") as f:
            f.write(bg_upload.read())
        st.success("Sfondo caricato! Ricarica la pagina.")
        st.rerun()
    if st.button("🎨 Tema base (senza foto)", use_container_width=True):
        for ext in [".jpg", ".jpeg", ".png"]:
            p = os.path.join(UPLOAD_DIR, "custom_bg" + ext)
            if os.path.exists(p): os.remove(p)
        st.rerun()

    st.markdown("---")

    guitars = get_guitars()
    total_val = sum(g.get("marketValue", 0) for g in guitars)
    total_paid = sum(g.get("pricePaid", 0) for g in guitars)
    overdue = [g for g in guitars if is_overdue(g.get("lastSetup"))]

    c1, c2 = st.columns(2)
    c1.metric("Chitarre", len(guitars))
    c2.metric("Valore Vault", fmt_currency(total_val), delta=fmt_currency(total_val - total_paid))
    
    urgent_col = st.container()
    with urgent_col:
        if len(overdue) > 0:
            st.markdown(f'<div class="metric-urgent">', unsafe_allow_html=True)
        st.metric("🔴 Setup urgente", len(overdue))
        if len(overdue) > 0:
            st.markdown('</div>', unsafe_allow_html=True)

    # Chart categorie HTML/CSS
    if guitars:
        st.markdown("---")
        st.caption("📊 Distribuzione Categorie")
        cats = {}
        for g in guitars:
            c = g.get("category", "Elettrica")
            cats[c] = cats.get(c, 0) + 1
        total_c = sum(cats.values())
        chart_html = "<div style='margin-bottom:12px;'>"
        for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
            pct = count / total_c * 100
            col = CATEGORY_COLORS.get(cat, "#808080")
            chart_html += f"""
            <div style="margin-bottom:8px; animation: fadeInUp 0.5s ease-out;">
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#C0C0C0; margin-bottom:3px; font-family:Oswald,sans-serif; letter-spacing:1px;">
                    <span>{CATEGORY_EMOJI.get(cat, '🎸')} {cat.upper()}</span>
                    <span>{count} ({pct:.0f}%)</span>
                </div>
                <div style="width:100%; height:6px; background:#1a1a1a; border-radius:3px; overflow:hidden; box-shadow: inset 0 1px 2px rgba(0,0,0,0.5);">
                    <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, {col}88, {col}); border-radius:3px; transition: width 1s ease-out;"></div>
                </div>
            </div>
            """
        chart_html += "</div>"
        st.markdown(chart_html, unsafe_allow_html=True)

        # Chart valore per marca
        st.caption("📊 Valore per Marca")
        brands = {}
        for g in guitars:
            b = g.get("brand", "Altro")
            brands[b] = brands.get(b, 0) + g.get("marketValue", 0)
        max_val = max(brands.values()) if brands else 1
        bchart_html = "<div style='margin-bottom:12px;'>"
        for i, (brand, val) in enumerate(sorted(brands.items(), key=lambda x: -x[1])):
            pct = val / max_val * 100
            bchart_html += f"""
            <div style="margin-bottom:8px; animation: fadeInUp 0.5s ease-out; animation-delay: {round(i*0.1, 1)}s;">
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#C0C0C0; margin-bottom:3px; font-family:Oswald,sans-serif; letter-spacing:1px;">
                    <span>{brand.upper()}</span>
                    <span>{fmt_currency(val)}</span>
                </div>
                <div style="width:100%; height:6px; background:#1a1a1a; border-radius:3px; overflow:hidden; box-shadow: inset 0 1px 2px rgba(0,0,0,0.5);">
                    <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, #707070, #C0C0C0, #E8E8E8); border-radius:3px; transition: width 1s ease-out;"></div>
                </div>
            </div>
            """
        bchart_html += "</div>"
        st.markdown(bchart_html, unsafe_allow_html=True)

    st.markdown("---")

    # Backup ZIP
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("vault_data.json", json.dumps(st.session_state.db, indent=4, ensure_ascii=False))
        foto_count = 0
        for g in guitars:
            ip = g.get("imagePath", "")
            if ip and os.path.exists(ip):
                zf.write(ip, arcname=os.path.basename(ip))
                foto_count += 1
        for w in get_wishlist():
            ip = w.get("imagePath", "")
            if ip and os.path.exists(ip):
                zf.write(ip, arcname=os.path.basename(ip))
                foto_count += 1
        if os.path.exists(UPLOAD_DIR):
            for fname in os.listdir(UPLOAD_DIR):
                fpath = os.path.join(UPLOAD_DIR, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.jpg','.jpeg','.png','.webp')):
                    arc = os.path.basename(fpath)
                    if arc not in [m.filename for m in zf.infolist()]:
                        zf.write(fpath, arcname=arc)
                        foto_count += 1
    buf.seek(0)
    st.download_button("📥 Backup ZIP", data=buf,
                       file_name=f"vault_backup_{datetime.now().strftime('%Y%m%d')}.zip",
                       mime="application/zip", use_container_width=True)
    st.caption(f"💾 {len(guitars)} chitarre + foto")

    # Ripristino
    up_bak = st.file_uploader("📤 Ripristina ZIP", type=["zip"])
    if up_bak is not None and st.button("Sostituisci Database", type="primary", use_container_width=True):
        try:
            zb = io.BytesIO(up_bak.read())
            with zipfile.ZipFile(zb, 'r') as zf:
                fl = zf.namelist()
                jname = "vault_data.json" if "vault_data.json" in fl else [n for n in fl if n.endswith('.json')][0]
                new_data = json.load(zf.open(jname))
                if isinstance(new_data, list):
                    new_data = {"guitars": new_data, "wishlist": []}
                for g in new_data.get("guitars", []):
                    if "category" not in g: g["category"] = "Elettrica"
                    if "maintenanceLog" not in g: g["maintenanceLog"] = []
                for w in new_data.get("wishlist", []):
                    if "imagePath" not in w: w["imagePath"] = ""
                for name in fl:
                    if name.lower().endswith(('.jpg','.jpeg','.png','.webp')):
                        with open(os.path.join(UPLOAD_DIR, os.path.basename(name)), 'wb') as fo:
                            fo.write(zf.read(name))
                st.session_state.db = new_data
                save_data(new_data)
                st.success("✅ Ripristinato!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Errore: {e}")

# ═══════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════
st.markdown("<h1 style='text-align:center;'>🎸 Guitar Rack & Vault Pro 🎸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#707070; font-family:Inter; font-size:0.95rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:2rem;'>Collezione · Inventario · Manutenzione · Wishlist</p>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  TABS PRINCIPALI
# ═══════════════════════════════════════════════════════════
tab_rack, tab_gallery, tab_wishlist, tab_compare, tab_chicche = st.tabs([
    "🎸 Rack & Manutenzione", "🖼️ Galleria", "💭 Wishlist", "⚖️ Confronto", "✨ Chicche"
])

with tab_rack:
    guitars = get_guitars()

    c1, c2, c3, c4 = st.columns([1.5,2,2,1.5])
    c1.metric("Totale", len(guitars))
    c2.metric("Valore", fmt_currency(sum(g.get("marketValue",0) for g in guitars)), 
              delta=fmt_currency(sum(g.get("marketValue",0) for g in guitars) - sum(g.get("pricePaid",0) for g in guitars)))
    
    with c3:
        urgent_count = len([g for g in guitars if is_overdue(g.get("lastSetup"))])
        if urgent_count > 0:
            st.markdown('<div class="metric-urgent">', unsafe_allow_html=True)
        st.metric("🔴 Urgenti", urgent_count, delta_color="inverse")
        if urgent_count > 0:
            st.markdown('</div>', unsafe_allow_html=True)
            
    with c4:
        st.write("")
        if st.button("➕ Aggiungi Chitarra", use_container_width=True, type="primary"):
            st.session_state.show_form = True
            st.session_state.editing_guitar_id = None
            st.rerun()

    st.divider()

    # FORM CHITARRA
    if st.session_state.show_form:
        sel = None
        idx = None
        if st.session_state.editing_guitar_id:
            for i, g in enumerate(guitars):
                if g["id"] == st.session_state.editing_guitar_id:
                    sel, idx = g, i
                    break
        with st.container(border=True):
            ch, cl = st.columns([4,1])
            ch.subheader("✏️ Modifica" if sel else "➕ Nuova Chitarra")
            if cl.button("❌ Chiudi", use_container_width=True):
                st.session_state.show_form = False
                st.session_state.editing_guitar_id = None
                st.rerun()

            with st.form("guitar_form"):
                uploaded_photo = st.file_uploader("📷 Foto", type=["jpg","jpeg","png","webp"])

                c1, c2, c3 = st.columns(3)
                brand = c1.text_input("Marca *", value=sel["brand"] if sel else "")
                model = c2.text_input("Modello *", value=sel["model"] if sel else "")
                cats = ["Elettrica", "Acustica", "Classica", "Basso", "Altro"]
                cat_idx = cats.index(sel.get("category","Elettrica")) if sel and sel.get("category") in cats else 0
                category = c3.selectbox("Categoria", cats, index=cat_idx)

                c4, c5, c6 = st.columns(3)
                year = c4.number_input("Anno", 1900, 2030, value=int(sel.get("year",2022)) if sel else 2022)
                serial = c5.text_input("Seriale", value=sel.get("serialNumber","") if sel else "")
                factory = c6.text_input("Fabbrica", value=sel.get("factory","") if sel else "")

                c7, c8, c9 = st.columns(3)
                conds = ["Mint", "Ottimo", "Buono", "Relic / Usurato", "Da restaurare"]
                cond_idx = conds.index(sel.get("condition","Ottimo")) if sel and sel.get("condition") in conds else 1
                condition = c7.selectbox("Stato", conds, index=cond_idx)
                price = c8.number_input("Prezzo Pagato €", 0, value=int(sel.get("pricePaid",0)) if sel else 0)
                market_val = c9.number_input("Valore Attuale €", 0, value=int(sel.get("marketValue",0)) if sel else 0)

                st.markdown("#### Specifiche Tecniche")
                s1, s2 = st.columns(2)
                body = s1.text_input("Body", value=sel.get("body","") if sel else "")
                neck = s2.text_input("Manico / Profilo", value=sel.get("neckWood","") if sel else "")
                s3, s4, s5 = st.columns(3)
                fretboard = s3.text_input("Tastiera", value=sel.get("fretboard","") if sel else "")
                pickups = s4.text_input("Pickups", value=sel.get("pickups","") if sel else "")
                hardware = s5.text_input("Hardware / Ponte", value=sel.get("hardware","") if sel else "")

                st.markdown("#### Manutenzione")
                m1, m2, m3 = st.columns(3)
                gauge = m1.text_input("Scalatura Corde", value=sel.get("stringGauge","") if sel else "")
                default_setup = datetime.now().date()
                if sel and sel.get("lastSetup"):
                    try: default_setup = datetime.strptime(sel["lastSetup"], "%Y-%m-%d").date()
                    except: pass
                setup_date = m2.date_input("Data Ultimo Setup", value=default_setup)
                notes = m3.text_input("Note", value=sel.get("notes","") if sel else "")

                submitted = st.form_submit_button("💾 Salva" if sel else "➕ Aggiungi")
                if submitted:
                    if brand and model:
                        gid = sel["id"] if sel else f"g-{int(datetime.now().timestamp())}"
                        img_path = sel.get("imagePath","") if sel else ""
                        if uploaded_photo is not None:
                            img_path = save_image(uploaded_photo, gid, prefix="g_")
                        new_g = {
                            "id": gid, "brand": brand, "model": model, "category": category,
                            "year": year, "serialNumber": serial, "factory": factory,
                            "condition": condition, "pricePaid": price, "marketValue": market_val,
                            "body": body, "neckWood": neck, "fretboard": fretboard,
                            "pickups": pickups, "hardware": hardware, "stringGauge": gauge,
                            "lastSetup": setup_date.strftime("%Y-%m-%d"), "notes": notes,
                            "imagePath": img_path,
                            "maintenanceLog": sel.get("maintenanceLog", []) if sel else []
                        }
                        if sel:
                            guitars[idx] = new_g
                            st.success(f"Modifiche a {brand} {model} salvate!")
                        else:
                            guitars.append(new_g)
                            st.success(f"{brand} {model} aggiunta!")
                        set_guitars(guitars)
                        st.session_state.show_form = False
                        st.session_state.editing_guitar_id = None
                        st.rerun()
                    else:
                        st.error("Inserisci almeno Marca e Modello.")
        st.divider()

    # FILTRI
    f1, f2, f3 = st.columns([2,2,2])
    search_q = f1.text_input("🔍 Cerca marca/modello/seriale...", "").lower()
    filter_cat = f2.multiselect("🏷️ Categorie", ["Elettrica","Acustica","Classica","Basso","Altro"], default=[])
    filter_alert = f3.radio("Stato Setup", ["Tutte", "⚠️ Urgenti (>4 mesi)", "✅ In regola"], horizontal=True)

    displayed = guitars[:]
    if search_q:
        displayed = [g for g in displayed if search_q in g.get("brand","").lower() or search_q in g.get("model","").lower() or search_q in g.get("serialNumber","").lower()]
    if filter_cat:
        displayed = [g for g in displayed if g.get("category","Elettrica") in filter_cat]
    if filter_alert == "⚠️ Urgenti (>4 mesi)":
        displayed = [g for g in displayed if is_overdue(g.get("lastSetup"))]
    elif filter_alert == "✅ In regola":
        displayed = [g for g in displayed if not is_overdue(g.get("lastSetup"))]

    if not displayed:
        st.info("Nessuna chitarra trovata.")

    for i, g in enumerate(displayed):
        status, days = maintenance_status(g)
        cat = g.get("category", "Elettrica")
        cat_color = CATEGORY_COLORS.get(cat, "#808080")
        cat_emoji = CATEGORY_EMOJI.get(cat, "🎸")
        stagger_class = f"stagger-{(i % 6) + 1}"

        with st.container(border=True):
            # Aggiungi classe per stagger animation
            st.markdown(f'<div class="{stagger_class}">', unsafe_allow_html=True)
            
            cimg, cinfo = st.columns([1, 3])
            with cimg:
                ip = g.get("imagePath")
                if ip and os.path.exists(ip):
                    st.image(ip, use_container_width=True)
                else:
                    st.markdown("""
                    <div style='height:180px; background:linear-gradient(145deg, #141414, #0f0f0f); border-radius:4px; display:flex; align-items:center; justify-content:center; color:#505050; font-size:0.8rem; border:1px dashed rgba(192,192,192,0.1);'>
                        <span style="font-size:2rem; opacity:0.3;">🎸</span>
                    </div>""", unsafe_allow_html=True)

            with cinfo:
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <span class="cat-badge" style="background:{cat_color}15; color:{cat_color}; border-color:{cat_color}50;">
                        {cat_emoji} {cat}
                    </span>
                </div>
                <div style="margin-bottom:12px;">
                    <span style="font-family:'Oswald',sans-serif; font-size:1.2rem; color:#FFFFF0; letter-spacing:2px; text-transform:uppercase;">{g['brand']}</span>
                    <span style="position:relative; display:inline-block; padding:2px 12px; margin:0 6px; font-family:'Oswald',sans-serif; font-size:1.3rem; color:#0a0a0a; font-weight:700; letter-spacing:1px; text-transform:uppercase;">
                        <span style="position:absolute; left:-4px; right:-4px; top:15%; bottom:15%; background:linear-gradient(90deg, rgba(218,165,32,0.85), rgba(255,215,0,0.9), rgba(218,165,32,0.85)); transform:skewX(-10deg); border-radius:2px; z-index:0; filter:blur(0.5px);"></span>
                        <span style="position:relative; z-index:1;">{g['model']}</span>
                    </span>
                    <span style="font-family:'Roboto Mono',monospace; font-size:0.85rem; color:#707070;">({g.get('year','N/D')})</span>
                </div>
                """, unsafe_allow_html=True)

                progress = min(days / 120.0, 1.0)
                bar_color = "#4CAF50" if status == "ok" else ("#FFC107" if status == "warning" else "#F44336")
                
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#707070; margin-bottom:4px; font-family:'Roboto Mono',monospace;">
                        <span>SETUP: {g.get('lastSetup','MAI')}</span>
                        <span style="color:{bar_color}; font-weight:600;">{days} GIORNI FA</span>
                    </div>
                    <div class="setup-bar-container">
                        <div class="setup-bar-fill" style="width:{progress*100}%; background:{bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                t1, t2, t3, t4 = st.tabs(["Info & Valore", "Specifiche", "Manutenzione", "🔧 Log"])
                with t1:
                    c1, c2 = st.columns(2)
                    c1.write(f"**Seriale:** `{g.get('serialNumber','N/D')}`")
                    c1.write(f"**Origine:** {g.get('factory','N/D')}")
                    c2.write(f"**Stato:** {g.get('condition')}")
                    c2.write(f"**Prezzo:** {fmt_currency(g.get('pricePaid',0))} → **Valore:** {fmt_currency(g.get('marketValue',0))}")
                with t2:
                    st.write(f"**Body:** {g.get('body','N/D')} | **Manico:** {g.get('neckWood','N/D')} | **Tastiera:** {g.get('fretboard','N/D')}")
                    st.write(f"**Pickups:** {g.get('pickups','N/D')} | **Hardware:** {g.get('hardware','N/D')}")
                with t3:
                    st.write(f"**Corde:** `{g.get('stringGauge','N/D')}`")
                    st.write(f"**Note:** {g.get('notes','Nessuna')}")
                with t4:
                    log = g.get("maintenanceLog", [])
                    if log:
                        for entry in sorted(log, key=lambda x: x.get("date",""), reverse=True):
                            st.markdown(f"""
                            <div style="border-left:2px solid #707070; padding-left:10px; margin-bottom:8px; animation: slideInLeft 0.4s ease-out;">
                                <span style="color:#FFFFF0; font-family:'Oswald',sans-serif; font-size:0.85rem; letter-spacing:1px;"><b>{entry.get('date')}</b> — {entry.get('type','Intervento').upper()}</span><br/>
                                <span style="color:#707070; font-size:0.8rem;">{entry.get('notes','')}</span>
                                {f'<br/><span style="color:#B8860B; font-family:Roboto Mono,monospace; font-size:0.8rem;">€ {entry.get("cost",0)}</span>' if entry.get('cost') else ''}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("Nessun intervento registrato.")

                    with st.expander("➕ Aggiungi intervento"):
                        with st.form(key=f"log_form_{g['id']}"):
                            l1, l2, l3 = st.columns(3)
                            log_date = l1.date_input("Data", value=datetime.now().date(), key=f"ld_{g['id']}")
                            log_type = l2.text_input("Tipo (es. Setup, Cambio corde)", value="Setup", key=f"lt_{g['id']}")
                            log_cost = l3.number_input("Costo €", 0, value=0, key=f"lc_{g['id']}")
                            log_notes = st.text_area("Note dettagliate", key=f"ln_{g['id']}")
                            if st.form_submit_button("Aggiungi al log"):
                                new_entry = {
                                    "date": log_date.strftime("%Y-%m-%d"),
                                    "type": log_type,
                                    "cost": log_cost,
                                    "notes": log_notes
                                }
                                g["maintenanceLog"].append(new_entry)
                                if "setup" in log_type.lower() or "corde" in log_type.lower():
                                    g["lastSetup"] = log_date.strftime("%Y-%m-%d")
                                set_guitars(guitars)
                                st.success("Intervento aggiunto!")
                                st.rerun()

                a1, a2, a3, a4 = st.columns(4)
                if a1.button("✏️ Modifica", key=f"edit_{g['id']}"):
                    st.session_state.show_form = True
                    st.session_state.editing_guitar_id = g["id"]
                    st.rerun()
                if a2.button("🔄 Setup Oggi", key=f"setup_{g['id']}"):
                    g["lastSetup"] = datetime.now().strftime("%Y-%m-%d")
                    g["maintenanceLog"].append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "Setup rapido",
                        "cost": 0,
                        "notes": "Segnato come fatto oggi"
                    })
                    set_guitars(guitars)
                    st.success("Setup aggiornato!")
                    st.rerun()
                if a3.button("📄 Scheda", key=f"card_{g['id']}"):
                    st.download_button("Scarica JSON", data=json.dumps(g, indent=2, ensure_ascii=False),
                                       file_name=f"{g['brand']}_{g['model']}.json", mime="application/json",
                                       key=f"dl_{g['id']}")
                if a4.button("🗑️ Elimina", key=f"del_{g['id']}", type="primary"):
                    if g.get("imagePath") and os.path.exists(g["imagePath"]):
                        try: os.remove(g["imagePath"])
                        except: pass
                    set_guitars([x for x in guitars if x["id"] != g["id"]])
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  TAB 2: GALLERIA
# ═══════════════════════════════════════════════════════════
with tab_gallery:
    guitars = get_guitars()
    st.subheader("🖼️ Galleria Collezione")
    if not guitars:
        st.info("Nessuna chitarra da mostrare.")
    else:
        gcat = st.multiselect("Filtra categoria", ["Elettrica","Acustica","Classica","Basso","Altro"], default=[], key="gal_cat")
        gal_items = guitars
        if gcat:
            gal_items = [g for g in gal_items if g.get("category","Elettrica") in gcat]

        cols_per_row = 4
        rows = [gal_items[i:i+cols_per_row] for i in range(0, len(gal_items), cols_per_row)]
        for row_idx, row in enumerate(rows):
            cols = st.columns(cols_per_row)
            for col_idx, (col, g) in enumerate(zip(cols, row)):
                with col:
                    ip = g.get("imagePath")
                    has_img = ip and os.path.exists(ip)
                    
                    # Effetto polaroid
                    st.markdown(f'<div class="polaroid stagger-{(col_idx % 6) + 1}">', unsafe_allow_html=True)
                    
                    if has_img:
                        st.image(ip, use_container_width=True)
                    else:
                        st.markdown("""
                        <div style='height:160px; background:linear-gradient(145deg, #1a1a1a, #141414); display:flex; align-items:center; justify-content:center; color:#505050; font-size:0.8rem;'>
                            <span style="font-size:2.5rem; opacity:0.2;">🎸</span>
                        </div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <center style="margin-top:8px;">
                        <b style='color:#FFFFF0; font-family:Oswald,sans-serif; font-size:0.85rem; letter-spacing:1px; text-transform:uppercase;'>{g['brand']}</b><br/>
                        <span style='color:#707070; font-size:0.8rem; font-family:Inter;'>{g['model']}</span><br/>
                        <span class="cat-badge" style="background:{CATEGORY_COLORS.get(g.get('category','Elettrica'), '#808080')}15; color:{CATEGORY_COLORS.get(g.get('category','Elettrica'), '#808080')}; border-color:{CATEGORY_COLORS.get(g.get('category','Elettrica'), '#808080')}50; margin-top:4px; display:inline-block;">
                            {CATEGORY_EMOJI.get(g.get('category','Elettrica'), '🎸')} {g.get('category','Elettrica')}
                        </span>
                    </center>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  TAB 3: WISHLIST (con foto)
# ═══════════════════════════════════════════════════════════
with tab_wishlist:
    wishlist = get_wishlist()
    st.subheader("💭 Gear Wanted")

    c1, c2 = st.columns([3,1])
    c1.markdown("Traccia gli strumenti che vorresti acquistare.")
    with c2:
        if st.button("➕ Aggiungi Desiderio", use_container_width=True):
            st.session_state.show_wishlist_form = True
            st.session_state.editing_wish_id = None
            st.rerun()

    if st.session_state.show_wishlist_form:
        wsel = None
        widx = None
        if st.session_state.editing_wish_id:
            for i, w in enumerate(wishlist):
                if w["id"] == st.session_state.editing_wish_id:
                    wsel, widx = w, i
                    break
        with st.container(border=True):
            ch, cl = st.columns([4,1])
            ch.subheader("✏️ Modifica Desiderio" if wsel else "➕ Nuovo Desiderio")
            if cl.button("❌ Chiudi", key="close_wish"):
                st.session_state.show_wishlist_form = False
                st.session_state.editing_wish_id = None
                st.rerun()

            with st.form("wish_form"):
                w_upload = st.file_uploader("📷 Foto dello strumento desiderato", type=["jpg","jpeg","png","webp"])

                w1, w2, w3 = st.columns(3)
                w_brand = w1.text_input("Marca *", value=wsel["brand"] if wsel else "")
                w_model = w2.text_input("Modello *", value=wsel["model"] if wsel else "")
                w_cat = w3.selectbox("Categoria", ["Elettrica","Acustica","Classica","Basso","Altro"],
                                     index=["Elettrica","Acustica","Classica","Basso","Altro"].index(wsel.get("category","Elettrica")) if wsel else 0)
                w4, w5, w6 = st.columns(3)
                w_budget = w4.number_input("Budget €", 0, value=int(wsel.get("budget",0)) if wsel else 0)
                w_priority = w5.selectbox("Priorità", ["Alta","Media","Bassa"],
                                          index=["Alta","Media","Bassa"].index(wsel.get("priority","Media")) if wsel else 1)
                w_year = w6.number_input("Anno", 1900, 2030, value=int(wsel.get("year","")) if wsel and wsel.get("year") else 2024)
                w_notes = st.text_area("Note / Link", value=wsel.get("notes","") if wsel else "")

                if st.form_submit_button("💾 Salva"):
                    if w_brand and w_model:
                        wid = wsel["id"] if wsel else f"w-{int(datetime.now().timestamp())}"
                        w_img = wsel.get("imagePath","") if wsel else ""
                        if w_upload is not None:
                            w_img = save_image(w_upload, wid, prefix="w_")
                        new_w = {
                            "id": wid, "brand": w_brand, "model": w_model, "category": w_cat,
                            "budget": w_budget, "priority": w_priority, "year": w_year,
                            "notes": w_notes, "imagePath": w_img
                        }
                        if wsel:
                            wishlist[widx] = new_w
                        else:
                            wishlist.append(new_w)
                        set_wishlist(wishlist)
                        st.session_state.show_wishlist_form = False
                        st.session_state.editing_wish_id = None
                        st.rerun()
                    else:
                        st.error("Inserisci Marca e Modello.")
        st.divider()

    if not wishlist:
        st.info("La wishlist è vuota.")
    else:
        prio_order = {"Alta":0, "Media":1, "Bassa":2}
        wishlist.sort(key=lambda x: prio_order.get(x.get("priority","Media"), 1))

        for i, w in enumerate(wishlist):
            pcol = {"Alta":"#F44336", "Media":"#FFC107", "Bassa":"#4CAF50"}.get(w.get("priority","Media"), "#707070")
            prio_class = {"Alta":"priority-high", "Media":"priority-medium", "Bassa":"priority-low"}.get(w.get("priority","Media"), "")
            
            with st.container(border=True):
                st.markdown(f'<div class="{prio_class} stagger-{(i % 6) + 1}" style="padding: 4px; border-radius: 4px;">', unsafe_allow_html=True)
                
                has_img = w.get("imagePath") and os.path.exists(w.get("imagePath"))
                if has_img:
                    cimg, cinfo = st.columns([1, 3])
                    with cimg:
                        st.image(w["imagePath"], use_container_width=True)
                else:
                    cimg, cinfo = st.columns([1, 3])
                    with cimg:
                        st.markdown("""
                        <div style='height:140px; background:linear-gradient(145deg, #141414, #0f0f0f); border-radius:4px; display:flex; align-items:center; justify-content:center; color:#505050; font-size:0.75rem; border:1px dashed rgba(192,192,192,0.1);'>
                            <span style="font-size:2rem; opacity:0.3;">💭</span>
                        </div>""", unsafe_allow_html=True)

                with cinfo:
                    st.markdown(f"""
                    <b style="color:#FFFFF0; font-family:Oswald,sans-serif; font-size:1.1rem; letter-spacing:2px; text-transform:uppercase;">{w['brand']} {w['model']}</b>
                    <span class="cat-badge" style="background:{pcol}22; color:{pcol}; border-color:{pcol}66; margin-left:8px;">
                        {w.get('priority','MEDIA')}
                    </span>
                    <br/><span style="color:#707070; font-size:0.8rem; font-family:Inter;">{w.get('category','Elettrica')} · Budget {fmt_currency(w.get('budget',0))} · Anno {w.get('year','N/D')}</span>
                    """, unsafe_allow_html=True)
                    if w.get("notes"):
                        st.caption(w["notes"])

                    a1, a2, a3 = st.columns([1,1,1])
                    if a1.button("✏️ Modifica", key=f"wedit_{w['id']}"):
                        st.session_state.show_wishlist_form = True
                        st.session_state.editing_wish_id = w["id"]
                        st.rerun()
                    if a2.button("🗑️ Elimina", key=f"wdel_{w['id']}", type="primary"):
                        if w.get("imagePath") and os.path.exists(w["imagePath"]):
                            try: os.remove(w["imagePath"])
                            except: pass
                        set_wishlist([x for x in wishlist if x["id"] != w["id"]])
                        st.rerun()
                    # Pulsante "Acquistato" per spostare in collezione
                    if a3.button("🛒 Acquistato!", key=f"wbuy_{w['id']}"):
                        # Sposta in collezione con dati base
                        new_g = {
                            "id": f"g-{int(datetime.now().timestamp())}",
                            "brand": w["brand"],
                            "model": w["model"],
                            "category": w.get("category", "Elettrica"),
                            "year": w.get("year", 2024),
                            "serialNumber": "",
                            "factory": "",
                            "condition": "Ottimo",
                            "pricePaid": w.get("budget", 0),
                            "marketValue": w.get("budget", 0),
                            "body": "", "neckWood": "", "fretboard": "",
                            "pickups": "", "hardware": "",
                            "stringGauge": "",
                            "lastSetup": datetime.now().strftime("%Y-%m-%d"),
                            "notes": f"Acquistato dalla wishlist. {w.get('notes','')}",
                            "imagePath": w.get("imagePath", ""),
                            "maintenanceLog": []
                        }
                        guitars = get_guitars()
                        guitars.append(new_g)
                        set_guitars(guitars)
                        # Rimuovi da wishlist
                        set_wishlist([x for x in wishlist if x["id"] != w["id"]])
                        st.success(f"🎸 {w['brand']} {w['model']} aggiunto alla collezione!")
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  TAB 4: CONFRONTO
# ═══════════════════════════════════════════════════════════
with tab_compare:
    st.subheader("⚖️ Confronta due strumenti")
    guitars = get_guitars()
    if len(guitars) < 2:
        st.info("Aggiungi almeno 2 chitarre per usare il confronto.")
    else:
        opts = {f"{g['brand']} {g['model']} ({g.get('year','')})": g for g in guitars}
        c1, c2 = st.columns(2)
        sel1 = c1.selectbox("Strumento 1", list(opts.keys()), index=0)
        sel2 = c2.selectbox("Strumento 2", list(opts.keys()), index=min(1, len(opts)-1))

        if sel1 and sel2 and sel1 != sel2:
            g1, g2 = opts[sel1], opts[sel2]

            f1, f2 = st.columns(2)
            for col, g in zip([f1, f2], [g1, g2]):
                with col:
                    ip = g.get("imagePath")
                    if ip and os.path.exists(ip):
                        st.markdown(f'<div style="border-radius:4px; overflow:hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
                        st.image(ip, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='height:240px; background:linear-gradient(145deg, #141414, #0f0f0f); border-radius:4px; display:flex; align-items:center; justify-content:center; color:#505050; font-size:0.9rem; border:1px dashed rgba(192,192,192,0.1);'>
                            <span style="font-size:3rem; opacity:0.2;"></span>
                        </div>""", unsafe_allow_html=True)

            fields = [
                ("Categoria", "category"), ("Anno", "year"), ("Seriale", "serialNumber"),
                ("Fabbrica", "factory"), ("Stato", "condition"), ("Prezzo Pagato", "pricePaid"),
                ("Valore Attuale", "marketValue"), ("Body", "body"), ("Manico", "neckWood"),
                ("Tastiera", "fretboard"), ("Pickups", "pickups"), ("Hardware", "hardware"),
                ("Corde", "stringGauge"), ("Ultimo Setup", "lastSetup"), ("Note", "notes")
            ]

            st.markdown("<br/>", unsafe_allow_html=True)
            for label, key in fields:
                v1 = g1.get(key, "N/D")
                v2 = g2.get(key, "N/D")
                if key in ["pricePaid", "marketValue"]:
                    v1 = fmt_currency(v1) if v1 else "N/D"
                    v2 = fmt_currency(v2) if v2 else "N/D"
                col_l, col_v1, col_v2 = st.columns([1,2,2])
                col_l.markdown(f"<span style='color:#707070; font-size:0.85rem; font-family:Oswald,sans-serif; letter-spacing:1px; text-transform:uppercase;'>{label}</span>", unsafe_allow_html=True)
                col_v1.markdown(f"<span style='color:#FFFFF0; font-size:0.9rem;'>{v1}</span>", unsafe_allow_html=True)
                col_v2.markdown(f"<span style='color:#FFFFF0; font-size:0.9rem;'>{v2}</span>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; border:none; height:1px; background:linear-gradient(90deg,transparent,rgba(192,192,192,0.1),transparent);'>", unsafe_allow_html=True)
        else:
            st.warning("Seleziona due strumenti diversi.")


# ═══════════════════════════════════════════════════════════
#  TAB 5: BASSMAN VINTAGE AMP
# ═══════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════
#  TAB 5: CHICCHE GRAFICHE INTERATTIVE
# ═══════════════════════════════════════════════════════════
with tab_chicche:
    st.subheader("✨ Chicche Grafiche")
    st.markdown("<p style='color:#707070; font-size:0.9rem; margin-bottom:1.5rem;'>Pedalboard virtuale, amp head interattivo, visualizzatore corde e equalizzatore animato.</p>", unsafe_allow_html=True)

    # ── SEZIONE 1: PEDALBOARD VIRTUALE ──
    st.markdown("#### 🎛️ Pedalboard Virtuale")
    st.caption("Clicca sui pedali per attivarli/disattivarli")

    pedalboard_html = """
    <style>
    .pb-wrapper { font-family: 'Oswald', sans-serif; }
    .pb-row {
        display: flex; gap: 14px; flex-wrap: wrap; justify-content: center;
        padding: 24px 16px; background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
        border-radius: 8px; border: 1px solid rgba(192,192,192,0.08);
        position: relative; overflow: hidden;
    }
    .pb-row::before {
        content: ""; position: absolute; inset: 0;
        background: repeating-linear-gradient(90deg, transparent 0px, transparent 39px, rgba(192,192,192,0.02) 39px, rgba(192,192,192,0.02) 40px);
        pointer-events: none;
    }
    .pedal {
        width: 90px; height: 150px; border-radius: 8px;
        position: relative; cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex; flex-direction: column; align-items: center; justify-content: space-between;
        padding: 10px 6px; border: 2px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 12px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);
        user-select: none;
    }
    .pedal:hover { transform: translateY(-5px) scale(1.04); box-shadow: 0 10px 24px rgba(0,0,0,0.6), 0 0 16px rgba(255,255,255,0.04); }
    .pedal.on { border-color: rgba(255,255,255,0.2); box-shadow: 0 0 16px rgba(255,255,255,0.06), 0 4px 16px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08); }
    .pedal.on .p-led { animation: ledPulse 1.5s ease-in-out infinite; background: #ff4444; border-color: #ff6666; }
    .pedal.pressed { animation: pedalPress 0.15s ease-out; }
    .p-led { width: 7px; height: 7px; border-radius: 50%; background: #333; border: 1px solid #555; transition: all 0.3s; }
    .p-knobs { display: flex; gap: 3px; margin: 6px 0; }
    .p-knob { width: 16px; height: 16px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #555, #222); border: 1px solid #666; position: relative; }
    .p-knob::after { content: ""; position: absolute; top: 2px; left: 50%; width: 2px; height: 5px; background: #aaa; transform: translateX(-50%); border-radius: 1px; }
    .p-name { font-size: 8px; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(255,255,255,0.55); text-align: center; line-height: 1.2; }
    .p-sw { width: 28px; height: 28px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #444, #1a1a1a); border: 2px solid #555; box-shadow: 0 2px 6px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; font-size: 9px; color: #888; transition: all 0.1s; }
    .pedal.on .p-sw { background: radial-gradient(circle at 35% 35%, #555, #222); box-shadow: 0 1px 3px rgba(0,0,0,0.5), inset 0 2px 4px rgba(0,0,0,0.3); }
    @keyframes ledPulse { 0%,100%{opacity:0.6;box-shadow:0 0 4px currentColor} 50%{opacity:1;box-shadow:0 0 10px currentColor,0 0 20px currentColor} }
    @keyframes pedalPress { 0%{transform:translateY(0)} 50%{transform:translateY(3px)} 100%{transform:translateY(0)} }
    </style>
    <div class="pb-wrapper">
      <div class="pb-row" id="pbRow">
        <div class="pedal" style="background:linear-gradient(180deg,#2a1a1a,#1a0a0a);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div><div class="p-knob"></div><div class="p-knob"></div></div>
          <div class="p-name">Overdrive</div>
          <div class="p-sw">BYPASS</div>
        </div>
        <div class="pedal" style="background:linear-gradient(180deg,#1a2a1a,#0a1a0a);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div><div class="p-knob"></div></div>
          <div class="p-name">Chorus</div>
          <div class="p-sw">BYPASS</div>
        </div>
        <div class="pedal" style="background:linear-gradient(180deg,#1a1a2a,#0a0a1a);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div><div class="p-knob"></div><div class="p-knob"></div><div class="p-knob"></div></div>
          <div class="p-name">Delay</div>
          <div class="p-sw">BYPASS</div>
        </div>
        <div class="pedal" style="background:linear-gradient(180deg,#2a2a1a,#1a1a0a);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div><div class="p-knob"></div></div>
          <div class="p-name">Fuzz</div>
          <div class="p-sw">BYPASS</div>
        </div>
        <div class="pedal" style="background:linear-gradient(180deg,#1a2a2a,#0a1a1a);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div></div>
          <div class="p-name">Boost</div>
          <div class="p-sw">BYPASS</div>
        </div>
        <div class="pedal" style="background:linear-gradient(180deg,#2a1a2a,#1a0a1a);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div><div class="p-knob"></div><div class="p-knob"></div></div>
          <div class="p-name">Reverb</div>
          <div class="p-sw">BYPASS</div>
        </div>
        <div class="pedal" style="background:linear-gradient(180deg,#2a2520,#1a1510);" onclick="togglePedal(this)">
          <div class="p-led"></div>
          <div class="p-knobs"><div class="p-knob"></div><div class="p-knob"></div></div>
          <div class="p-name">Wah</div>
          <div class="p-sw">BYPASS</div>
        </div>
      </div>
    </div>
    <script>
    function togglePedal(el) {
      el.classList.toggle('on');
      el.classList.add('pressed');
      setTimeout(() => el.classList.remove('pressed'), 150);
      const sw = el.querySelector('.p-sw');
      sw.textContent = el.classList.contains('on') ? 'ACTIVE' : 'BYPASS';
      updateChain();
    }
    function updateChain() {
      const active = document.querySelectorAll('.pedal.on').length;
      const readout = document.getElementById('chainReadout');
      if (readout) readout.textContent = active + ' pedali attivi nella catena';
    }
    </script>
    <div id="chainReadout" style="text-align:center; margin-top:10px; color:#707070; font-family:Oswald,sans-serif; font-size:0.8rem; letter-spacing:1px;">0 pedali attivi nella catena</div>
    """
    components.html(pedalboard_html, height=260, scrolling=False)

    st.divider()

    # ── SEZIONE 2: AMP HEAD VIRTUALE ──
    st.markdown("#### 🔥 Amp Head Virtuale")
    st.caption("Gira i knob, accendi l'amplificatore e guarda il VU meter")

    amp_html = """
    <style>
    .amp-wrap { font-family: 'Oswald', sans-serif; display: flex; flex-direction: column; align-items: center; gap: 12px; }
    .amp-box {
      width: 480px; max-width: 100%; background: linear-gradient(180deg, #1e1e1e 0%, #0f0f0f 100%);
      border-radius: 12px; padding: 20px; border: 2px solid rgba(192,192,192,0.1);
      box-shadow: 0 8px 32px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.04);
      position: relative; overflow: hidden;
    }
    .amp-box::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, rgba(192,192,192,0.25), transparent); }
    .amp-grille {
      background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.25) 3px, rgba(0,0,0,0.25) 4px),
                  repeating-linear-gradient(90deg, transparent, transparent 3px, rgba(0,0,0,0.25) 3px, rgba(0,0,0,0.25) 4px),
                  linear-gradient(180deg, #2a2a2a, #1a1a1a);
      border-radius: 4px; padding: 14px; margin: 8px 0; border: 1px solid rgba(192,192,192,0.06);
      display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;
    }
    .ak { display: flex; flex-direction: column; align-items: center; gap: 6px; }
    .ak-dial {
      width: 48px; height: 48px; border-radius: 50%;
      background: radial-gradient(circle at 35% 35%, #444, #1a1a1a);
      border: 2px solid #555; box-shadow: 0 4px 8px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.06);
      position: relative; cursor: grab; transition: all 0.2s;
    }
    .ak-dial:hover { box-shadow: 0 0 12px rgba(192,192,192,0.08), 0 4px 8px rgba(0,0,0,0.5); }
    .ak-dial::after { content: ""; position: absolute; top: 5px; left: 50%; width: 2.5px; height: 14px; background: #aaa; transform: translateX(-50%); border-radius: 2px; box-shadow: 0 0 3px rgba(255,255,255,0.15); }
    .ak-lbl { font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #888; }
    .ak-val { font-family: 'Roboto Mono', monospace; font-size: 10px; color: #C0C0C0; }
    .amp-vu { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 8px; padding-top: 10px; border-top: 1px solid #333; }
    .amp-led { width: 10px; height: 10px; border-radius: 50%; background: #331111; border: 1px solid #553333; transition: all 0.5s; }
    .amp-led.on { background: #ff4422; border-color: #ff6644; box-shadow: 0 0 8px #ff4422, 0 0 16px #ff4422aa; animation: ledPulse 2s ease-in-out infinite; }
    .amp-sw { display: flex; align-items: center; gap: 6px; cursor: pointer; padding: 3px 8px; border-radius: 6px; transition: background 0.2s; user-select: none; }
    .amp-sw:hover { background: rgba(255,255,255,0.04); }
    .sw-track { width: 32px; height: 16px; background: #333; border-radius: 8px; position: relative; transition: background 0.3s; border: 1px solid #444; }
    .sw-track.on { background: #4a7c3f; }
    .sw-thumb { width: 12px; height: 12px; background: #ccc; border-radius: 50%; position: absolute; top: 1px; left: 2px; transition: left 0.3s cubic-bezier(0.4,0,0.2,1); box-shadow: 0 1px 3px rgba(0,0,0,0.4); }
    .sw-track.on .sw-thumb { left: 17px; background: #fff; }
    .sw-lbl { font-size: 10px; color: #888; letter-spacing: 1px; text-transform: uppercase; font-weight: 500; transition: color 0.3s; }
    .sw-lbl.on { color: #7cb87c; }
    .warm { position: absolute; inset: 0; border-radius: 12px; pointer-events: none; opacity: 0; transition: opacity 0.6s ease; background: radial-gradient(ellipse at 50% 30%, rgba(255,140,50,0.05) 0%, transparent 70%); }
    .warm.on { opacity: 1; }
    .amp-badge { text-align: center; margin-top: 6px; }
    .amp-badge h4 { font-size: 16px; font-weight: 600; color: #C0C0C0; letter-spacing: 4px; text-transform: uppercase; margin: 0; }
    .amp-badge p { font-size: 10px; color: #707070; letter-spacing: 2px; margin: 2px 0 0; text-transform: uppercase; }
    .tone-desc { margin-top: 10px; padding: 8px 12px; background: rgba(0,0,0,0.15); border-radius: 6px; font-size: 12px; color: #707070; text-align: center; letter-spacing: 0.5px; min-height: 18px; font-family: 'Inter', sans-serif; }
    @keyframes ledPulse { 0%,100%{opacity:0.8} 50%{opacity:1} }
    </style>
    <div class="amp-wrap">
      <div class="amp-box">
        <div class="warm" id="warm"></div>
        <div class="amp-grille">
          <div class="ak"><div class="ak-dial" id="k0" style="transform:rotate(0deg);" onmousedown="startKnob(event,0)"></div><div class="ak-lbl">Gain</div><div class="ak-val" id="v0">5</div></div>
          <div class="ak"><div class="ak-dial" id="k1" style="transform:rotate(0deg);" onmousedown="startKnob(event,1)"></div><div class="ak-lbl">Bass</div><div class="ak-val" id="v1">5</div></div>
          <div class="ak"><div class="ak-dial" id="k2" style="transform:rotate(0deg);" onmousedown="startKnob(event,2)"></div><div class="ak-lbl">Mid</div><div class="ak-val" id="v2">5</div></div>
          <div class="ak"><div class="ak-dial" id="k3" style="transform:rotate(0deg);" onmousedown="startKnob(event,3)"></div><div class="ak-lbl">Treble</div><div class="ak-val" id="v3">5</div></div>
          <div class="ak"><div class="ak-dial" id="k4" style="transform:rotate(0deg);" onmousedown="startKnob(event,4)"></div><div class="ak-lbl">Presence</div><div class="ak-val" id="v4">3</div></div>
          <div class="ak"><div class="ak-dial" id="k5" style="transform:rotate(0deg);" onmousedown="startKnob(event,5)"></div><div class="ak-lbl">Master</div><div class="ak-val" id="v5">6</div></div>
        </div>
        <div class="amp-vu">
          <div class="amp-led" id="pilot"></div>
          <svg width="100" height="50" viewBox="0 0 100 50">
            <path d="M 8 46 A 38 38 0 0 1 92 46" fill="none" stroke="#333" stroke-width="6" stroke-linecap="round"/>
            <path d="M 12 46 A 34 34 0 0 1 36 18" fill="none" stroke="#2d5a27" stroke-width="4.5" stroke-linecap="round"/>
            <path d="M 36 18 A 34 34 0 0 1 64 18" fill="none" stroke="#8a7a20" stroke-width="4.5" stroke-linecap="round"/>
            <path d="M 64 18 A 34 34 0 0 1 88 46" fill="none" stroke="#5a1a1a" stroke-width="4.5" stroke-linecap="round"/>
            <g id="needle" transform="rotate(-45, 50, 46)">
              <line x1="50" y1="46" x2="50" y2="14" stroke="#e8d5b5" stroke-width="1.2" stroke-linecap="round"/>
              <circle cx="50" cy="46" r="2.5" fill="#888"/>
            </g>
          </svg>
          <div class="amp-sw" id="pwrSw" onclick="toggleAmp()">
            <div class="sw-track" id="swTrk"><div class="sw-thumb"></div></div>
            <span class="sw-lbl" id="swLbl">Off</span>
          </div>
        </div>
        <div class="amp-badge"><h4>Vault Head</h4><p>Tube Amplifier · All-Tube Preamp</p></div>
      </div>
      <div class="tone-desc" id="toneDesc">Amp is off. Flip the switch to warm up the tubes.</div>
    </div>
    <script>
    const knobs = [
      {name:'gain', val:5, min:0, max:10},
      {name:'bass', val:5, min:0, max:10},
      {name:'mid', val:5, min:0, max:10},
      {name:'treble', val:5, min:0, max:10},
      {name:'presence', val:3, min:0, max:10},
      {name:'master', val:6, min:0, max:10}
    ];
    let ampOn = false; let vuInt = null; let nAng = -45; let tAng = -45; let dragIdx = null, dragY0 = 0, dragV0 = 0;
    function setKnob(i, v) {
      knobs[i].val = v;
      const ang = -135 + (v / knobs[i].max) * 270;
      document.getElementById('k'+i).style.transform = 'rotate('+ang+'deg)';
      document.getElementById('v'+i).textContent = v;
      updateTone();
    }
    function startKnob(e, i) { e.preventDefault(); dragIdx = i; dragY0 = e.clientY; dragV0 = knobs[i].val; document.addEventListener('mousemove', onKnob); document.addEventListener('mouseup', endKnob); }
    function onKnob(e) { if(dragIdx===null) return; const dy = (dragY0 - e.clientY) * 0.06; let nv = Math.round(Math.max(knobs[dragIdx].min, Math.min(knobs[dragIdx].max, dragV0 + dy))); setKnob(dragIdx, nv); }
    function endKnob() { dragIdx = null; document.removeEventListener('mousemove', onKnob); document.removeEventListener('mouseup', endKnob); }
    function toggleAmp() {
      ampOn = !ampOn;
      document.getElementById('swTrk').classList.toggle('on', ampOn);
      document.getElementById('swLbl').classList.toggle('on', ampOn);
      document.getElementById('swLbl').textContent = ampOn ? 'On' : 'Off';
      document.getElementById('pilot').classList.toggle('on', ampOn);
      document.getElementById('warm').classList.toggle('on', ampOn);
      if (ampOn) {
        vuInt = setInterval(() => { const intensity = (knobs[0].val + knobs[5].val) / 20; tAng = -45 + Math.random() * 85 * intensity; }, 90);
        updateTone();
      } else { clearInterval(vuInt); tAng = -45; document.getElementById('toneDesc').textContent = 'Amp is off. Flip the switch to warm up the tubes.'; }
    }
    function animNeedle() { nAng += (tAng - nAng) * 0.12; document.getElementById('needle').setAttribute('transform', 'rotate('+nAng+', 50, 46)'); requestAnimationFrame(animNeedle); }
    animNeedle();
    function updateTone() {
      if(!ampOn) return;
      const g = knobs[0].val, b = knobs[1].val, m = knobs[2].val, t = knobs[3].val, p = knobs[4].val, ma = knobs[5].val;
      let d = [];
      if(g >= 7) d.push('crunchy'); else if(g >= 4) d.push('clean'); else d.push('mellow');
      if(t >= 7) d.push('bright'); if(b >= 7) d.push('thumpy'); if(m >= 7) d.push('punchy'); if(p >= 6) d.push('airy');
      document.getElementById('toneDesc').textContent = 'Tone: ' + d.join(' · ') + ' — Gain ' + g + ' · Master ' + ma;
    }
    knobs.forEach((k,i) => setKnob(i, k.val));
    </script>
    """
    components.html(amp_html, height=340, scrolling=False)

    st.divider()

    # ── SEZIONE 3: VISUALIZZATORE CORDE ──
    st.markdown("#### 🎸 Visualizzatore Corde")
    st.caption("Clicca sulle corde per farle vibrare")

    strings_html = """
    <style>
    .str-wrap { font-family: 'Oswald', sans-serif; background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%); border-radius: 8px; padding: 20px; border: 1px solid rgba(192,192,192,0.08); position: relative; overflow: hidden; }
    .str-wrap::before { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, transparent 0px, transparent 29px, rgba(192,192,192,0.015) 29px, rgba(192,192,192,0.015) 30px); pointer-events: none; }
    .gstr { height: 32px; display: flex; align-items: center; position: relative; cursor: pointer; transition: all 0.2s; border-radius: 4px; }
    .gstr:hover { background: rgba(255,255,255,0.02); }
    .gstr.vib { animation: stringVibrate 0.5s ease-out; }
    .snote { font-family: 'Roboto Mono', monospace; font-size: 13px; color: #C0C0C0; width: 32px; text-align: center; letter-spacing: 1px; font-weight: 500; }
    .sline { flex: 1; height: 2px; background: linear-gradient(90deg, #888, #aaa, #888); border-radius: 1px; position: relative; transition: all 0.3s; margin: 0 12px; }
    .gstr:hover .sline { height: 3px; box-shadow: 0 0 8px rgba(255,255,255,0.25); }
    .sfret { position: absolute; right: 0; top: 0; bottom: 0; display: flex; align-items: center; gap: 40px; padding-right: 20px; }
    .fdot { width: 7px; height: 7px; border-radius: 50%; background: rgba(192,192,192,0.12); transition: all 0.3s; }
    .gstr:hover .fdot { background: rgba(192,192,192,0.35); box-shadow: 0 0 6px rgba(192,192,192,0.15); }
    .sgauge { font-family: 'Roboto Mono', monospace; font-size: 9px; color: #505050; width: 50px; text-align: right; }
    @keyframes stringVibrate { 0%{transform:translateX(0)} 10%{transform:translateX(-2px)} 20%{transform:translateX(2px)} 30%{transform:translateX(-1.5px)} 40%{transform:translateX(1.5px)} 50%{transform:translateX(-1px)} 60%{transform:translateX(1px)} 70%{transform:translateX(-0.5px)} 80%{transform:translateX(0.5px)} 90%{transform:translateX(-0.3px)} 100%{transform:translateX(0)} }
    </style>
    <div class="str-wrap">
      <div class="gstr" onclick="pluck(this)"><span class="snote">E</span><div class="sline" style="height:3px;"></div><span class="sgauge">.046</span><div class="sfret"><div class="fdot"></div><div class="fdot"></div><div class="fdot" style="background:rgba(192,192,192,0.25);"></div><div class="fdot"></div><div class="fdot"></div></div></div>
      <div class="gstr" onclick="pluck(this)"><span class="snote">A</span><div class="sline" style="height:2.5px;"></div><span class="sgauge">.036</span><div class="sfret"><div class="fdot"></div><div class="fdot"></div><div class="fdot"></div><div class="fdot" style="background:rgba(192,192,192,0.25);"></div><div class="fdot"></div></div></div>
      <div class="gstr" onclick="pluck(this)"><span class="snote">D</span><div class="sline" style="height:2px;"></div><span class="sgauge">.026</span><div class="sfret"><div class="fdot"></div><div class="fdot" style="background:rgba(192,192,192,0.25);"></div><div class="fdot"></div><div class="fdot"></div><div class="fdot"></div></div></div>
      <div class="gstr" onclick="pluck(this)"><span class="snote">G</span><div class="sline" style="height:1.8px;"></div><span class="sgauge">.017</span><div class="sfret"><div class="fdot"></div><div class="fdot"></div><div class="fdot"></div><div class="fdot" style="background:rgba(192,192,192,0.25);"></div><div class="fdot"></div></div></div>
      <div class="gstr" onclick="pluck(this)"><span class="snote">B</span><div class="sline" style="height:1.5px;"></div><span class="sgauge">.013</span><div class="sfret"><div class="fdot"></div><div class="fdot"></div><div class="fdot" style="background:rgba(192,192,192,0.25);"></div><div class="fdot"></div><div class="fdot"></div></div></div>
      <div class="gstr" onclick="pluck(this)"><span class="snote">e</span><div class="sline" style="height:1.2px;"></div><span class="sgauge">.010</span><div class="sfret"><div class="fdot"></div><div class="fdot"></div><div class="fdot"></div><div class="fdot"></div><div class="fdot" style="background:rgba(192,192,192,0.25);"></div></div></div>
    </div>
    <script>
    function pluck(el) {
      el.classList.remove('vib');
      void el.offsetWidth;
      el.classList.add('vib');
      setTimeout(() => el.classList.remove('vib'), 500);
    }
    </script>
    """
    components.html(strings_html, height=240, scrolling=False)

    st.divider()

    # ── SEZIONE 4: EQUALIZZATORE ANIMATO ──
    st.markdown("#### 📊 Equalizzatore Animato")
    st.caption("Equalizzatore grafico a 9 bande con animazione reattiva e preset")

    eq_html = """
    <style>
    .eq-wrap { font-family: 'Oswald', sans-serif; background: linear-gradient(180deg, #1a1a1a, #0f0f0f); border-radius: 8px; padding: 20px; border: 1px solid rgba(192,192,192,0.08); }
    .eq-row { display: flex; align-items: flex-end; justify-content: center; gap: 8px; height: 140px; padding: 16px 12px 0; }
    .eq-col { display: flex; flex-direction: column; align-items: center; gap: 6px; }
    .eq-bar-track { width: 18px; height: 100px; background: rgba(0,0,0,0.3); border-radius: 3px; position: relative; overflow: hidden; }
    .eq-bar-fill { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(180deg, #C0C0C0, #707070); border-radius: 0 0 3px 3px; transition: height 0.4s cubic-bezier(0.4,0,0.2,1); }
    .eq-bar-fill::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: rgba(255,255,255,0.35); border-radius: 2px; }
    .eq-lbl { font-family: 'Roboto Mono', monospace; font-size: 8px; color: #707070; text-align: center; letter-spacing: 1px; }
    .eq-ctrl { display: flex; justify-content: center; gap: 12px; margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(192,192,192,0.06); }
    .eq-btn { padding: 6px 16px; background: linear-gradient(145deg, #1a1a1a, #0f0f0f); border: 1px solid rgba(192,192,192,0.12); border-radius: 3px; color: #C0C0C0; font-family: 'Oswald', sans-serif; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; cursor: pointer; transition: all 0.2s; }
    .eq-btn:hover { border-color: rgba(192,192,192,0.3); box-shadow: 0 0 12px rgba(192,192,192,0.06); }
    .eq-btn.on { border-color: rgba(192,192,192,0.25); background: linear-gradient(145deg, #222, #151515); }
    </style>
    <div class="eq-wrap">
      <div class="eq-row" id="eqRow">
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b0" style="height:30%"></div></div><div class="eq-lbl">63Hz</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b1" style="height:45%"></div></div><div class="eq-lbl">125</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b2" style="height:60%"></div></div><div class="eq-lbl">250</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b3" style="height:50%"></div></div><div class="eq-lbl">500</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b4" style="height:70%"></div></div><div class="eq-lbl">1k</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b5" style="height:55%"></div></div><div class="eq-lbl">2k</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b6" style="height:40%"></div></div><div class="eq-lbl">4k</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b7" style="height:35%"></div></div><div class="eq-lbl">8k</div></div>
        <div class="eq-col"><div class="eq-bar-track"><div class="eq-bar-fill" id="b8" style="height:25%"></div></div><div class="eq-lbl">16k</div></div>
      </div>
      <div class="eq-ctrl">
        <div class="eq-btn on" id="btnPlay" onclick="toggleEQ()">▶ Play</div>
        <div class="eq-btn" onclick="resetEQ()">↺ Reset</div>
        <div class="eq-btn" onclick="presetRock()">🎸 Rock</div>
        <div class="eq-btn" onclick="presetJazz()">🎷 Jazz</div>
      </div>
    </div>
    <script>
    let eqPlaying = true; let eqInt = null;
    const base = [30,45,60,50,70,55,40,35,25];
    function setBars(vals) { vals.forEach((v,i) => { document.getElementById('b'+i).style.height = v+'%'; }); }
    function animateEQ() {
      const nv = base.map(v => Math.max(8, Math.min(95, v + (Math.random()-0.5)*40)));
      setBars(nv);
    }
    function toggleEQ() {
      eqPlaying = !eqPlaying;
      document.getElementById('btnPlay').classList.toggle('on', eqPlaying);
      document.getElementById('btnPlay').textContent = eqPlaying ? '▶ Play' : '⏸ Pause';
      if(eqPlaying) { eqInt = setInterval(animateEQ, 180); } else { clearInterval(eqInt); }
    }
    function resetEQ() { clearInterval(eqInt); setBars(base); eqPlaying = false; document.getElementById('btnPlay').classList.remove('on'); document.getElementById('btnPlay').textContent = '▶ Play'; }
    function presetRock() { clearInterval(eqInt); setBars([55,50,45,40,65,70,60,45,30]); eqPlaying = false; document.getElementById('btnPlay').classList.remove('on'); document.getElementById('btnPlay').textContent = '▶ Play'; }
    function presetJazz() { clearInterval(eqInt); setBars([25,30,40,55,60,50,35,25,20]); eqPlaying = false; document.getElementById('btnPlay').classList.remove('on'); document.getElementById('btnPlay').textContent = '▶ Play'; }
    eqInt = setInterval(animateEQ, 180);
    </script>
    """
    components.html(eq_html, height=240, scrolling=False)

    st.markdown("<br/><p style='text-align:center; color:#505050; font-size:0.8rem; font-family:Inter;'>Tutti i controlli sono interattivi. Clicca, trascina e sperimenta!</p>", unsafe_allow_html=True)
