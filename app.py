import streamlit as st
import json
import os
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

# Crea la cartella per le immagini se non esiste
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Dati di partenza
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
        "lastSetup": "2025-10-10",
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
        
        # Apri e ridimensiona leggermente l'immagine per ottimizzare lo spazio
        img = Image.open(uploaded_file)
        img.thumbnail((1200, 1200))
        img.save(file_path)
        return file_path
    return ""

# Inizializzazione Session State
if "guitars" not in st.session_state:
    st.session_state.guitars = load_data()

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

# --- UI APP ---
st.title("🎸 Guitar Rack & Vault")
st.caption("Gestione inventario, foto, specifiche e manutenzione sincronizzata")

# Controllo strumenti da manutenere
overdue_guitars = [g for g in st.session_state.guitars if is_overdue(g.get("lastSetup"))]

# HUD Statistiche
col1, col2 = st.columns(2)
col1.metric("Totale Chitarre nel Vault", len(st.session_state.guitars))
col2.metric("Cambio Corde URGENTE (>4 mesi)", len(overdue_guitars), delta_color="inverse")

st.divider()

# 3. Form Gestione: Aggiungi o Modifica Chitarra
st.subheader("⚙️ Gestione Chitarre (Aggiungi / Modifica)")

guitar_options = ["➕ Aggiungi Nuova Chitarra"] + [f"{g['brand']} {g['model']} (SN: {g.get('serialNumber', 'N/D')})" for g in st.session_state.guitars]
selected_option = st.selectbox("Seleziona uno strumento da modificare o aggiungine uno nuovo:", guitar_options)

selected_guitar = None
if selected_option != "➕ Aggiungi Nuova Chitarra":
    selected_idx = guitar_options.index(selected_option) - 1
    selected_guitar = st.session_state.guitars[selected_idx]

with st.form("guitar_form", clear_on_submit=False):
    st.write("### " + ("Modifica Chitarra" if selected_guitar else "Nuova Chitarra"))
    
    # Campo Foto
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
            
            # Gestione file immagine
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
            st.rerun()
        else:
            st.error("Inserisci almeno Marca e Modello.")

st.divider()

# 4. Filtro e Visualizzazione Vault
st.subheader("📋 Lista Strumenti")

filter_option = st.radio(
    "Filtra la vista:",
    ["Tutte le chitarre", "⚠️ Solo quelle che necessitano cambio corde"],
    horizontal=True
)

displayed_guitars = st.session_state.guitars
if filter_option == "⚠️ Solo quelle che necessitano cambio corde":
    displayed_guitars = overdue_guitars

if not displayed_guitars:
    st.info("Nessuna chitarra trovata per questo filtro.")

for g in displayed_guitars:
    overdue = is_overdue(g.get("lastSetup"))
    
    with st.container(border=True):
        col_img, col_info = st.columns([1, 3])
        
        # Colonna Foto
        with col_img:
            img_path = g.get("imagePath")
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.caption("📷 Nessuna foto presente")
        
        # Colonna Dettagli
        with col_info:
            st.markdown(f"### {g['brand']} {g['model']} ({g.get('year', 'N/D')})")
            
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

            col_act1, col_act2 = st.columns(2)
            if col_act1.button("🔄 Segna Setup/Cambio Corde Oggi", key=f"setup_{g['id']}"):
                for item in st.session_state.guitars:
                    if item["id"] == g["id"]:
                        item["lastSetup"] = datetime.now().strftime("%Y-%m-%d")
                        break
                save_data(st.session_state.guitars)
                st.success("Setup aggiornato a oggi!")
                st.rerun()

            if col_act2.button("🗑️ Elimina", key=f"del_{g['id']}", type="primary"):
                # Rimuovi l'immagine se esiste
                if g.get("imagePath") and os.path.exists(g["imagePath"]):
                    try:
                        os.remove(g["imagePath"])
                    except:
                        pass
                st.session_state.guitars = [item for item in st.session_state.guitars if item["id"] != g["id"]]
                save_data(st.session_state.guitars)
                st.rerun()