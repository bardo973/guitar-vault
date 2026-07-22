import streamlit as st
import json
import os
from datetime import datetime

# 1. Configurazione Pagina
st.set_page_config(
    page_title="Guitar Rack & Vault",
    page_icon="🎸",
    layout="wide"
)

DB_FILE = "vault_data.json"

# Dati di partenza se il file non esiste
DEFAULT_GUITARS = [
    {
        "id": "g-1",
        "brand": "Fender",
        "model": "American Professional II Stratocaster",
        "year": 2021,
        "serialNumber": "US210984",
        "factory": "Corona, USA",
        "condition": "Mint",
        "purchaseDate": "2021-11-15",
        "pricePaid": 1850,
        "marketValue": 1950,
        "body": "Alder con finitura Gloss Urethane",
        "neckWood": "Acero, Bolt-On con Micro-Tilt",
        "neckProfile": "Deep C",
        "fretboard": "Palissandro, Raggio 9.5\", 22 Narrow Tall",
        "scaleLength": "25.5\"",
        "hardware": "Tremolo Sincronizzato 2-Punti, Meccaniche Autobloccanti",
        "pickups": "SSS - 3x V-Mod II Single-Coil",
        "stringGauge": "0.010-0.046",
        "stringBrand": "Ernie Ball Regular Slinky",
        "lastSetup": "2025-10-10",
        "lastFretboardClean": "2025-10-10",
        "mods": "Schermatura cavità controlli con foglia di rame",
        "lutherieWork": "Capotasto in osso sagomato a mano",
        "notes": "Azione molto bassa, setup Mi Standard"
    }
]

# 2. Funzioni di Caricamento e Salvataggio su Server
def load_data():
    if not os.path.exists(DB_FILE):
        save_data(DEFAULT_GUITARS)
        return DEFAULT_GUITARS
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Inizializzazione Session State
if "guitars" not in st.session_state:
    st.session_state.guitars = load_data()

# Utility per calcolo mesi dal setup
def is_overdue(date_str):
    if not date_str:
        return True
    try:
        setup_date = datetime.strptime(date_str, "%Y-%m-%d")
        diff_days = (datetime.now() - setup_date).days
        return diff_days > 120  # Più di 4 mesi (120 giorni)
    except:
        return False

# --- UI INTERFACCIA ---
st.title("🎸 Guitar Rack & Vault")
st.caption("Gestione inventario, specifiche tecniche e manutenzione sincronizzata in Cloud")

# HUD Statistiche
col1, col2, col3, col4 = st.columns(4)
total_guitars = len(st.session_state.guitars)
overdue_count = sum(1 for g in st.session_state.guitars if is_overdue(g.get("lastSetup")))

col1.metric("Totale Strumenti", total_guitars)
col2.metric("Cambio Corde URGENTE (>4 Mesi)", overdue_count, delta_color="inverse")

# 3. Form Inserimento / Nuova Chitarra
with st.expander("➕ Aggiungi un Nuovo Strumento al Vault"):
    with st.form("add_guitar_form", clear_on_submit=True):
        st.subheader("1. Dati Anagrafici")
        c1, c2, c3 = st.columns(3)
        brand = c1.text_input("Marca *")
        model = c2.text_input("Modello *")
        year = c3.number_input("Anno di Produzione", min_value=1900, max_value=2030, value=2022)
        
        c4, c5, c6 = st.columns(3)
        serial = c4.text_input("Numero di Serie")
        factory = c5.text_input("Fabbrica / Paese")
        condition = c6.selectbox("Stato", ["Mint", "Ottimo", "Buono", "Relic / Usurato", "Da restaurare"])
        
        c7, c8 = st.columns(2)
        price = c7.number_input("Prezzo Pagato (€)", min_value=0, value=0)
        market_val = c8.number_input("Valore Attuale (€)", min_value=0, value=0)

        st.subheader("2. Specifiche Tecniche")
        spec1, spec2 = st.columns(2)
        body = spec1.text_input("Body")
        neck = spec2.text_input("Manico / Profilo")
        
        spec3, spec4 = st.columns(2)
        fretboard = spec3.text_input("Tastiera")
        pickups = spec4.text_input("Pickups / Elettronica")

        st.subheader("3. Manutenzione")
        m1, m2, m3 = st.columns(3)
        gauge = m1.text_input("Scalatura Corde (es. 0.010-0.046)")
        setup_date = m2.date_input("Data Ultimo Setup", datetime.now())
        notes = m3.text_input("Note particolari")

        submitted = st.form_submit_button("Salva nel Vault Cloud")
        if submitted:
            if brand and model:
                new_guitar = {
                    "id": f"g-{int(datetime.now().timestamp())}",
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
                    "stringGauge": gauge,
                    "lastSetup": setup_date.strftime("%Y-%m-%d"),
                    "notes": notes
                }
                st.session_state.guitars.append(new_guitar)
                save_data(st.session_state.guitars)
                st.success(f"{brand} {model} aggiunta con successo!")
                st.rerun()
            else:
                st.error("Inserisci almeno Marca e Modello.")

st.divider()

# 4. Lista e Visualizzazione Strumenti
st.subheader("📋 I tuoi Strumenti")

for idx, g in enumerate(st.session_state.guitars):
    overdue = is_overdue(g.get("lastSetup"))
    status_badge = "⚠️ CAMBIO CORDE NECESSARIO" if overdue else "✓ OK"
    
    with st.container(border=True):
        col_title, col_btn = st.columns([4, 1])
        col_title.markdown(f"### {g['brand']} {g['model']} ({g.get('year', 'N/D')})")
        
        if overdue:
            col_title.warning(f"Ultimo setup: {g.get('lastSetup', 'Mai')} — {status_badge}")
        else:
            col_title.info(f"Ultimo setup: {g.get('lastSetup', 'Mai')}")

        t1, t2, t3 = st.tabs(["Anagrafica & Valore", "Specifiche", "Manutenzione & Note"])
        
        with t1:
            st.write(f"**Serial Number:** `{g.get('serialNumber', 'N/D')}` | **Origine:** {g.get('factory', 'N/D')}")
            st.write(f"**Stato:** {g.get('condition')} | **Prezzo:** €{g.get('pricePaid')} | **Valore Stimato:** €{g.get('marketValue')}")
            
        with t2:
            st.write(f"**Body:** {g.get('body', 'N/D')}")
            st.write(f"**Manico:** {g.get('neckWood', 'N/D')}")
            st.write(f"**Tastiera:** {g.get('fretboard', 'N/D')}")
            st.write(f"**Pickups:** {g.get('pickups', 'N/D')}")
            
        with t3:
            st.write(f"**Scalatura Corde:** `{g.get('stringGauge', 'N/D')}`")
            st.write(f"**Note:** {g.get('notes', 'Nessuna note')}")

        # Pulsanti d'azione
        b1, b2 = st.columns([1, 1])
        if b1.button("🔄 Segna Setup Oggi", key=f"setup_{g['id']}"):
            g['lastSetup'] = datetime.now().strftime("%Y-%m-%d")
            save_data(st.session_state.guitars)
            st.rerun()
            
        if b2.button("🗑️ Elimina", key=f"del_{g['id']}", type="primary"):
            st.session_state.guitars.pop(idx)
            save_data(st.session_state.guitars)
            st.rerun()