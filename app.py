import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from PIL import Image

# Configurazione cartella immagini
if not os.path.exists("immagini_chitarre"):
    os.makedirs("immagini_chitarre")

st.title("🎸 La mia Collezione di Chitarre")

# Form per aggiungere una chitarra
with st.sidebar:
    st.header("Aggiungi nuova chitarra")
    with st.form("nuova_chitarra"):
        marca = st.text_input("Marca")
        modello = st.text_input("Modello")
        anno = st.number_input("Anno", min_value=1900, max_value=2026, step=1)
        tipo = st.selectbox("Tipo", ["Elettrica", "Acustica", "Classica", "Basso"])
        
        # Nuovi campi
        pickup = st.text_input("Pickup (es. Humbucker, Single Coil)")
        custodia = st.selectbox("Custodia", ["Rigida", "Morbida", "Nessuna"])
        setting = st.text_area("Setting (es. Action, Ponte)")
        valore = st.number_input("Valore Attuale (€)", min_value=0, step=50)
        
        marca_corde = st.text_input("Marca Corde")
        scalatura = st.text_input("Scalatura (es. 09-42)")
        data_cambio = st.date_input("Ultimo cambio corde", value=date.today())
        
        note = st.text_area("Note aggiuntive")
        foto = st.file_uploader("Carica foto", type=['jpg', 'png', 'jpeg'])
        
        submit = st.form_submit_button("Salva Chitarra")

# Salvataggio dati
if submit and marca and modello:
    nome_file = f"{marca}_{modello}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    if foto:
        img = Image.open(foto)
        img.save(os.path.join("immagini_chitarre", nome_file))
    
    nuova_chitarra = {
        "Marca": [marca], "Modello": [modello], "Anno": [anno], 
        "Tipo": [tipo], "Pickup": [pickup], "Custodia": [custodia],
        "Setting": [setting], "Valore": [valore],
        "Marca Corde": [marca_corde], "Scalatura": [scalatura], 
        "Data Cambio": [str(data_cambio)], "Note": [note], "Foto": [nome_file]
    }
    
    df_nuovo = pd.DataFrame(nuova_chitarra)
    if os.path.exists("collezione.csv"):
        df_esistente = pd.read_csv("collezione.csv")
        df_finale = pd.concat([df_esistente, df_nuovo], ignore_index=True)
    else:
        df_finale = df_nuovo
    
    df_finale.to_csv("collezione.csv", index=False)
    st.success("Chitarra salvata!")

# Visualizzazione collezione
if os.path.exists("collezione.csv"):
    df = pd.read_csv("collezione.csv")
    st.subheader("La tua collezione")
    
    st.metric("Valore Totale Collezione", f"{df['Valore'].sum():,.2f} €")
    
    for i, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        
        data_ultima = datetime.strptime(row['Data Cambio'], '%Y-%m-%d').date()
        giorni_trascorsi = (date.today() - data_ultima).days
        
        with col1:
            percorso_img = os.path.join("immagini_chitarre", str(row['Foto']))
            if os.path.exists(percorso_img):
                st.image(percorso_img, use_column_width=True)
            else:
                st.write("Nessuna foto")
        
        with col2:
            st.write(f"### {row['Marca']} {row['Modello']} ({row['Anno']})")
            st.write(f"💰 **Valore:** {row['Valore']} € | 🛡️ **Custodia:** {row['Custodia']}")
            
            if giorni_trascorsi > 90:
                st.error(f"⚠️ Corde da cambiare! ({giorni_trascorsi} gg)")
            else:
                st.info(f"✅ Corde ok: {giorni_trascorsi} giorni dall'ultimo cambio")
                
            with st.expander("Dettagli Tecnici"):
                st.write(f"**Tipo:** {row['Tipo']}")
                st.write(f"**Pickup:** {row['Pickup']}")
                st.write(f"**Setting:** {row['Setting']}")
                st.write(f"**Corde:** {row['Marca Corde']} ({row['Scalatura']})")
                st.write(f"**Note:** {row['Note']}")
        st.divider()