import streamlit as st
import pandas as pd
import os
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
        colore = st.text_input("Colore")
        note = st.text_area("Note/Modifiche")
        foto = st.file_uploader("Carica foto", type=['jpg', 'png', 'jpeg'])
        
        submit = st.form_submit_button("Salva Chitarra")

# Salvataggio dati
if submit and marca and modello:
    nome_file = f"{marca}_{modello}.jpg"
    if foto:
        img = Image.open(foto)
        img.save(os.path.join("immagini_chitarre", nome_file))
    
    nuova_chitarra = {
        "Marca": [marca], "Modello": [modello], "Anno": [anno], 
        "Tipo": [tipo], "Colore": [colore], "Note": [note], "Foto": [nome_file]
    }
    
    df_nuovo = pd.DataFrame(nuova_chitarra)
    if os.path.exists("collezione.csv"):
        df_esistente = pd.read_csv("collezione.csv")
        df_finale = pd.concat([df_esistente, df_nuovo], ignore_index=True)
    else:
        df_finale = df_nuovo
    
    df_finale.to_csv("collezione.csv", index=False)
    st.success("Chitarra aggiunta!")

# Visualizzazione collezione
if os.path.exists("collezione.csv"):
    df = pd.read_csv("collezione.csv")
    st.subheader("La tua collezione")
    
    for i, row in df.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            if os.path.exists(os.path.join("immagini_chitarre", row['Foto'])):
                st.image(os.path.join("immagini_chitarre", row['Foto']), use_column_width=True)
        with col2:
            st.write(f"### {row['Marca']} {row['Modello']}")
            st.write(f"**Anno:** {row['Anno']} | **Tipo:** {row['Tipo']}")
            st.write(f"**Colore:** {row['Colore']}")
            st.write(f"**Note:** {row['Note']}")
        st.divider()