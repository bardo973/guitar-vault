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
        "purchaseDate": "2021-11-15",
        "pricePaid": 1850,
        "marketValue": 1950,
        "body": "Alder con finitura Gloss Urethane",
        "neckWood": "Acero, Bolt-On con Micro-Tilt",
        "neckProfile": "Deep C",
        "fretboard": "Palissandro, Raggio 9.5\", 22 Narrow Tall",
        "pickups": "SSS - 3x V-Mod II Single-Coil",
        "stringGauge": "0.010-0.046",
        "lastSetup": "2025-10-10",
        "notes": "Azione molto bassa, setup Mi Standard"
    }
]

# 2. Funzioni I/O File Server
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

# Inizializzazione dati in Session State
if "guitars" not in st.session_state:
    st.session_state.guitars = load_data()

# Calcolo differenza setup (URGENTE se > 120 giorni)
def is_overdue(date_str):
    if not date_str:
        return True
    try:
        setup_date = datetime.strptime(date_str, "%Y-%m-%d")
        diff_days = (datetime.now() - setup_date).days
        return diff_days > 120
    except Exception:
        return False

# --- HEADER & STATISTICHE ---
st.title("🎸 Guitar Rack & Vault")
st.caption("Sincronizzato in Cloud — visibile e modificabile da PC e iPhone")

overdue_guitars = [g for g in st.session_state.guitars if is_overdue(g.get("lastSetup"))]

col_stat1, col_stat2 = st.columns(2)
col_stat1.metric("Totale Strumenti nel Vault", len(st.session_state.guitars))
col_stat2.metric("Cambio Corde URGENTE (>4 Mesi)", len(overdue_guitars), delta_color="inverse")

st.divider()

# --- BARRA DI FILTRO & MENU A TENDINA ---
st.subheader("🔍 Filtra e Cerca Strumenti")

f_col1, f_col2 = st.columns([1, 2])

# Menu a tendina per il tipo di filtro
filter_option = f_col1.selectbox(
    "Mostra per stato setup:",
    ["Tutti gli strumenti", "⚠️ Solo cambio corde URGENTE", "✓ Setup in regola"]
)

# Menu a tendina per selezione diretta del singolo strumento
guitar_labels = ["--- Nessuna selezione (Mostra elenco) ---"] + [
    f"{g['brand']} {g['model']} ({g.get('serialNumber', 'No Serial')})" for g in st.session_state.guitars
]
selected_guitar_label = f_col2.selectbox("Oppure seleziona uno strumento specifico:", guitar_labels)

# Applichiamo la logica di filtraggio
filtered_guitars = st.session_state.guitars

if selected_guitar_label != "--- Nessuna selezione (Mostra elenco) ---":
    # Selezionato uno strumento specifico
    idx_sel = guitar_labels.index(selected_guitar_label) - 1
    filtered_guitars = [st.session_state.guitars[idx_sel]]
elif filter_option == "⚠️ Solo cambio corde URGENTE":
    filtered_guitars = overdue_guitars
elif filter_option == "✓ Setup in regola":
    filtered_guitars = [g for g in st.session_state.guitars if not is_overdue(g.get("lastSetup"))]

st.divider()

# --- FORM AGGIUNTA NUOVA CHITARRA ---
with st.expander("➕ Aggiungi un Nuovo Strumento"):
    with st.form("add_guitar_form", clear_on_submit=True):
        st.subheader("Informazioni Base")
        c1, c2, c3 = st.columns(3)
        brand = c1.text_input("Marca *")
        model = c2.text_input("Modello *")
        year = c3.number_input("Anno", min_value=1900, max_value=2030, value=2022)
        
        c4, c5, c6 = st.columns(3)
        serial = c4.text_input("Numero di Serie")
        factory = c5.text_input("Fabbrica / Paese")
        condition = c6.selectbox("Stato", ["Mint", "Ottimo", "Buono", "Usurato / Relic", "Da restaurare"])

        st.subheader("Specifiche & Manutenzione")
        s1, s2 = st.columns(2)
        body = s1.text_input("Body")
        neck = s2.text_input("Manico / Profilo")
        
        s3, s4 = s5 = st.columns(3)
        pickups = s3.text_input("Pickups")
        gauge = s4.text_input("Scalatura Corde (es. 0.010-0.046)")
        setup_date = s5.date_input("Data Ultimo Setup", datetime.now())

        if st.form_submit_button("💾 Salva nel Vault"):
            if brand and model:
                new_g = {
                    "id": f"g-{int(datetime.now().timestamp())}",
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "serialNumber": serial,
                    "factory": factory,
                    "condition": condition,
                    "body": body,
                    "neckWood": neck,
                    "pickups": pickups,
                    "stringGauge": gauge,
                    "lastSetup": setup_date.strftime("%Y-%m-%d"),
                    "notes": ""
                }
                st.session_state.guitars.append(new_g)
                save_data(st.session_state.guitars)
                st.success("Strumento aggiunto con successo!")
                st.rerun()
            else:
                st.error("Marca e Modello sono obbligatori.")

# --- LISTA CHITARRE & MODIFICA ---
if not filtered_guitars:
    st.info("Nessuno strumento corrisponde ai filtri selezionati.")

for g in filtered_guitars:
    # Cerchiamo l'indice reale nell'elenco principale
    real_idx = next(i for i, item in enumerate(st.session_state.guitars) if item["id"] == g["id"])
    overdue = is_overdue(g.get("lastSetup"))
    
    with st.container(border=True):
        header_col, action_col = st.columns([3, 1])
        
        title_prefix = "⚠️ " if overdue else "🎸 "
        header_col.markdown(f"### {title_prefix}{g['brand']} {g['model']} ({g.get('year', 'N/D')})")
        
        if overdue:
            header_col.warning(f"Ultimo Cambio Corde / Setup: **{g.get('lastSetup', 'Mai')}** — Necessario intervento!")
        else:
            header_col.success(f"Ultimo Cambio Corde / Setup: **{g.get('lastSetup', 'Mai')}**")

        # Scheda Dettagli / Modifica
        tab_view, tab_edit = st.tabs(["👁️ Dettagli Strumento", "✏️ Modifica Scheda"])
        
        with tab_view:
            v1, v2, v3 = st.columns(3)
            v1.write(f"**Serial Number:** `{g.get('serialNumber', 'N/D')}`")
            v1.write(f"**Origine:** {g.get('factory', 'N/D')}")
            v1.write(f"**Condizione:** {g.get('condition', 'N/D')}")
            
            v2.write(f"**Body:** {g.get('body', 'N/D')}")
            v2.write(f"**Manico:** {g.get('neckWood', 'N/D')}")
            v2.write(f"**Pickups:** {g.get('pickups', 'N/D')}")
            
            v3.write(f"**Scalatura Corde:** `{g.get('stringGauge', 'N/D')}`")
            v3.write(f"**Prezzo Pagato:** €{g.get('pricePaid', 0)}")
            v3.write(f"**Valore di Mercato:** €{g.get('marketValue', 0)}")
            
            if g.get("notes"):
                st.info(f"**Note:** {g.get('notes')}")

            # Pulsanti Rapidi
            btn_col1, btn_col2 = st.columns([1, 1])
            if btn_col1.button("🔄 Segna Cambio Corde Oggi", key=f"quick_setup_{g['id']}"):
                st.session_state.guitars[real_idx]['lastSetup'] = datetime.now().strftime("%Y-%m-%d")
                save_data(st.session_state.guitars)
                st.success("Setup aggiornato a oggi!")
                st.rerun()

            if btn_col2.button("🗑️ Elimina", key=f"del_{g['id']}", type="primary"):
                st.session_state.guitars.pop(real_idx)
                save_data(st.session_state.guitars)
                st.rerun()

        # FORM DI MODIFICA COMPLETA
        with tab_edit:
            with st.form(f"edit_form_{g['id']}"):
                st.subheader("Modifica Specifiche dello Strumento")
                
                ec1, ec2, ec3 = st.columns(3)
                edit_brand = ec1.text_input("Marca", value=g.get("brand", ""))
                edit_model = ec2.text_input("Modello", value=g.get("model", ""))
                edit_year = ec3.number_input("Anno", min_value=1900, max_value=2030, value=int(g.get("year", 2022)))

                ec4, ec5, ec6 = st.columns(3)
                edit_serial = ec4.text_input("Serial Number", value=g.get("serialNumber", ""))
                edit_factory = ec5.text_input("Fabbrica / Paese", value=g.get("factory", ""))
                
                cond_list = ["Mint", "Ottimo", "Buono", "Usurato / Relic", "Da restaurare"]
                curr_cond_idx = cond_list.index(g.get("condition")) if g.get("condition") in cond_list else 0
                edit_condition = ec6.selectbox("Condizione", cond_list, index=curr_cond_idx)

                es1, es2 = st.columns(2)
                edit_body = es1.text_input("Body", value=g.get("body", ""))
                edit_neck = es2.text_input("Manico / Profilo", value=g.get("neckWood", ""))

                es3, es4, es5 = st.columns(3)
                edit_pickups = es3.text_input("Pickups", value=g.get("pickups", ""))
                edit_gauge = es4.text_input("Scalatura Corde", value=g.get("stringGauge", ""))
                
                # Parsing data per il date_input
                try:
                    default_date = datetime.strptime(g.get("lastSetup"), "%Y-%m-%d")
                except Exception:
                    default_date = datetime.now()
                edit_setup_date = es5.date_input("Data Ultimo Setup", default_date)

                edit_notes = st.text_area("Note / Modifiche effettuate", value=g.get("notes", ""))

                if st.form_submit_button("💾 Salva Modifiche"):
                    st.session_state.guitars[real_idx].update({
                        "brand": edit_brand,
                        "model": edit_model,
                        "year": edit_year,
                        "serialNumber": edit_serial,
                        "factory": edit_factory,
                        "condition": edit_condition,
                        "body": edit_body,
                        "neckWood": edit_neck,
                        "pickups": edit_pickups,
                        "stringGauge": edit_gauge,
                        "lastSetup": edit_setup_date.strftime("%Y-%m-%d"),
                        "notes": edit_notes
                    })
                    save_data(st.session_state.guitars)
                    st.success("Modifiche salvate con successo!")
                    st.rerun()