import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from PIL import Image

if not os.path.exists("immagini_chitarre"):
    os.makedirs("immagini_chitarre")

st.title("🎸 La mia Collezione di Chitarre")

# --- FUNZIONI DI GESTIONE ---
def carica_dati():
    return pd.read_csv("collezione.csv") if os.path.exists("collezione.csv") else pd.DataFrame()

# Sidebar per Aggiunta
with st.sidebar:
    st.header("Aggiungi nuova chitarra")
    with st.form("nuova_chitarra", clear_on_submit=True):
        marca = st.text_input("Marca")
        modello = st.text_input("Modello")
        anno = st.number_input("Anno", min_value=1900, max_value=2026, step=1)
        tipo = st.selectbox("Tipo", ["Elettrica", "Acustica", "Classica", "Basso"])
        setting = st.text_area("Setting")
        valore = st.number_input("Valore (€)", min_value=0, step=50)
        marca_corde = st.text_input("Marca Corde")
        scalatura = st.text_input("Scalatura")
        data_cambio = st.date_input("Ultimo cambio corde", value=date.today())
        note = st.text_area("Note")
        foto = st.file_uploader("Carica foto", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("Salva")

if submit and marca and modello:
    nome_file = f"{marca}_{modello}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    if foto:
        Image.open(foto).save(os.path.join("immagini_chitarre", nome_file))
    
    nuova_riga = pd.DataFrame([{
        "Marca": marca, "Modello": modello, "Anno": anno, "Tipo": tipo,
        "Setting": setting, "Valore": valore,
        "Marca Corde": marca_corde, "Scalatura": scalatura,
        "Data Cambio": str(data_cambio), "Note": note, "Foto": nome_file
    }])
    
    df = pd.concat([carica_dati(), nuova_riga], ignore_index=True)
    df.to_csv("collezione.csv", index=False)
    st.rerun()

# --- VISUALIZZAZIONE ---
df = carica_dati()
if not df.empty:
    st.metric("Valore Totale", f"{df['Valore'].sum():,.2f} €")
    
    for i, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        
        # Calcolo scadenza corde (90 giorni = circa 3 mesi)
        data_ultima = datetime.strptime(row['Data Cambio'], '%Y-%m-%d').date()
        giorni_trascorsi = (date.today() - data_ultima).days
        
        with col1:
            percorso = os.path.join("immagini_chitarre", str(row['Foto']))
            if os.path.exists(percorso): st.image(percorso)
        
        with col2:
            st.write(f"### {row['Marca']} {row['Modello']}")
            
            # Avviso corde
            if giorni_trascorsi > 90:
                st.error(f"⚠️ Corde da cambiare! (Cambiate {giorni_trascorsi} gg fa)")
            else:
                st.info(f"✅ Corde ok: cambiate {giorni_trascorsi} giorni fa")
            
            # Pulsanti Azione
            c_mod, c_del = st.columns(2)
            with c_mod:
                if st.button("✏️ Modifica", key=f"mod_{i}"):
                    st.session_state.editing = i
            with c_del:
                if st.button("🗑️ Elimina", key=f"del_{i}"):
                    df.drop(i).to_csv("collezione.csv", index=False)
                    st.rerun()

            # Logica Modifica
            if 'editing' in st.session_state and st.session_state.editing == i:
                with st.expander("Modifica dati", expanded=True):
                    with st.form(f"form_mod_{i}"):
                        row['Marca'] = st.text_input("Marca", row['Marca'])
                        row['Valore'] = st.number_input("Valore", row['Valore'])
                        if st.form_submit_button("Salva Modifiche"):
                            df.loc[i] = row
                            df.to_csv("collezione.csv", index=False)
                            del st.session_state.editing
                            st.rerun()
            else:
                st.write(f"💰 **Valore:** {row['Valore']} €")
                with st.expander("Dettagli"):
                    st.write(f"**Tipo:** {row['Tipo']} | **Setting:** {row['Setting']}")
                    st.write(f"**Corde:** {row['Marca Corde']} ({row['Scalatura']})")
                    st.write(f"**Note:** {row['Note']}")
        st.divider()