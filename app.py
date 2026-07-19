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
    st.header("Aggiungi/Modifica chitarra")
    with st.form("nuova_chitarra"):
        marca = st.text_input("Marca")
        modello = st.text_input("Modello")
        anno = st.number_input("Anno", min_value=1900, max_value=2026, step=1)
        tipo = st.selectbox("Tipo", ["Elettrica", "Acustica", "Classica", "Basso"])
        colore = st.text_input("Colore")
        marca_corde = st.text_input("Marca Corde")
        scalatura = st.text_input("Scalatura (es. 09-42)")
        
        # Nuovo campo data
        data_cambio = st.date_input("Ultimo cambio corde", value=date.today())
        
        note = st.text_area("Note/Modifiche")
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
        "Tipo": [tipo], "Colore": [colore], "Marca Corde": [marca_corde],
        "Scalatura": [scalatura], "Data Cambio": [str(data_cambio)],
        "Note": [note], "Foto": [nome_file]
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
    
    for i, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        
        # Calcolo giorni trascorsi
        data_ultima = datetime.strptime(row['Data Cambio'], '%Y-%m-%d').date()
        giorni_trascorsi = (date.today() - data_ultima).days
        
        with col1:
            percorso_img = os.path.join("immagini_chitarre", str(row['Foto']))
            if os.path.exists(percorso_img):
                st.image(percorso_img, use_column_width=True)
        
        with col2:
            st.write(f"### {row['Marca']} {row['Modello']}")
            st.write(f"**Corde:** {row['Marca Corde']} ({row['Scalatura']})")
            
            # Logica avviso cambio corde
            if giorni_trascorsi > 90:
                st.error(f"⚠️ Corde vecchie: cambiate {giorni_trascorsi} giorni fa!")
            else:
                st.info(f"✅ Corde ok: cambiate {giorni_trascorsi} giorni fa.")
                
            with st.expander("Vedi dettagli"):
                st.write(f"**Anno:** {row['Anno']} | **Tipo:** {row['Tipo']} | **Colore:** {row['Colore']}")
                st.write(f"**Note:** {row['Note']}")
        st.divider()