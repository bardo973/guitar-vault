import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from PIL import Image
import streamlit.components.v1 as components

CARTELLA_IMG = "guitar_valute"
if not os.path.exists(CARTELLA_IMG):
    os.makedirs(CARTELLA_IMG)

# Nome del file CSV per la collezione
FILE_CSV = "collezione.csv"

st.title("🎸 La mia Collezione di Chitarre")

def carica_dati():
    if os.path.exists(FILE_CSV):
        return pd.read_csv(FILE_CSV)
    return pd.DataFrame(columns=["Marca", "Modello", "Anno", "Valore", "Foto", "Note"])

df = carica_dati()

# --- GESTIONE SIDEBAR PER AGGIUNGERE / MODIFICARE ---
st.sidebar.header(" gestione Chitarre")
azione = st.sidebar.radio("Scegli un'azione", ["Visualizza Collezione", "Aggiungi Nuova Chitarra"])

if azione == "Aggiungi Nuova Chitarra":
    st.sidebar.subheader("Inserisci i dati della nuova chitarra")
    with st.sidebar.form("form_aggiungi"):
        marca = st.text_input("Marca")
        modello = st.text_input("Modello")
        anno = st.number_input("Anno", min_value=1900, max_value=datetime.now().year, value=2020, step=1)
        valore = st.number_input("Valore (€)", min_value=0.0, value=500.0, step=50.0)
        note = st.text_area("Note / Modifiche")
        foto_file = st.file_uploader("Carica Foto", type=["jpg", "png", "jpeg"])
        
        submit_btn = st.form_submit_button("Salva Chitarra")
        
        if submit_btn:
            if marca and modello:
                nome_foto = ""
                if foto_file is not None:
                    nome_foto = f"{marca}_{modello}_{date.today()}.jpg".replace(" ", "_")
                    percorso_foto = os.path.join(CARTELLA_IMG, nome_foto)
                    with open(percorso_foto, "wb") as f:
                        f.write(foto_file.getbuffer())
                
                nuova_riga = pd.DataFrame([{
                    "Marca": marca,
                    "Modello": modello,
                    "Anno": int(anno),
                    "Valore": float(valore),
                    "Foto": nome_foto,
                    "Note": note
                }])
                
                df = pd.concat([df, nuova_riga], ignore_index=True)
                df.to_csv(FILE_CSV, index=False)
                st.sidebar.success("Chitarra aggiunta con successo!")
                st.rerun()
            else:
                st.sidebar.error("Inserisci almeno Marca e Modello.")

# Ricarica i dati aggiornati
df = carica_dati()

# --- NAVIGAZIONE RAPIDA ---
if not df.empty:
    st.subheader("Vai a:")
    cols = st.columns(len(df))
    for idx, (i, row) in enumerate(df.iterrows()):
        if cols[idx].button(f"{row['Marca']} {row['Modello']}", key=f"nav_{i}"):
            st.query_params["target"] = i
            st.rerun()

# --- SCRIPT SCROLL AUTOMATICO ---
target_id = st.query_params.get("target")
if target_id is not None:
    try:
        target_idx = int(target_id)
        scroll_script = f"""
        <script>
            var targetElement = document.getElementById("guitar-{target_idx}");
            if (targetElement) {{
                targetElement.scrollIntoView({{behavior: "smooth", block: "start"}});
            }}
        </script>
        """
        components.html(scroll_script, height=0)
    except ValueError:
        pass

# --- VISUALIZZAZIONE DELLA COLLEZIONE ---
if df.empty:
    st.info("La tua collezione è vuota. Usa il menu a sinistra (**Aggiungi Nuova Chitarra**) per iniziare a inserire i tuoi strumenti!")
else:
    st.metric("Valore Totale", f"{df['Valore'].sum():,.2f} €")
    st.divider()
    
    for i, row in df.iterrows():
        # DIV con ID univoco per il JavaScript dello scroll
        st.markdown(f'<div id="guitar-{i}"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if pd.notna(row['Foto']) and row['Foto'] != "":
                percorso = os.path.join(CARTELLA_IMG, str(row['Foto']))
                if os.path.exists(percorso):
                    st.image(percorso, use_container_width=True)
                else:
                    st.warning("Foto non trovata.")
            else:
                st.info("Nessuna foto disponibile.")
        
        with col2:
            st.write(f"### {row['Marca']} {row['Modello']}")
            st.write(f"**Anno:** {int(row['Anno'])}")
            st.write(f"**Valore:** {row['Valore']:,.2f} €")
            if pd.notna(row['Note']) and row['Note'] != "":
                st.write(f"**Note:** {row['Note']}")
            
            # Tasto per eliminare la singola chitarra
            if st.button("Elimina Chitarra", key=f"del_{i}"):
                # Rimuovi l'immagine se esiste
                if pd.notna(row['Foto']) and row['Foto'] != "":
                    percorso = os.path.join(CARTELLA_IMG, str(row['Foto']))
                    if os.path.exists(percorso):
                        os.remove(percorso)
                
                df = df.drop(i).reset_index(drop=True)
                df.to_csv(FILE_CSV, index=False)
                st.success("Chitarra eliminata!")
                st.rerun()
                
        st.divider()