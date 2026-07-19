import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from PIL import Image
import streamlit.components.v1 as components

CARTELLA_IMG = "guitar_valute"
if not os.path.exists(CARTELLA_IMG):
    os.makedirs(CARTELLA_IMG)

st.title("🎸 La mia Collezione di Chitarre")

def carica_dati():
    return pd.read_csv("collezione.csv") if os.path.exists("collezione.csv") else pd.DataFrame()

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
if target_id:
    # JavaScript per trovare l'elemento e scrollare
    scroll_script = f"""
    <script>
        var targetElement = document.getElementById("guitar-{target_id}");
        if (targetElement) {{
            targetElement.scrollIntoView({{behavior: "smooth", block: "start"}});
        }}
    </script>
    """
    components.html(scroll_script, height=0)

# Sidebar e salvataggio (omessi per brevità, resta uguale al precedente)
# ... [Inserire qui il codice della Sidebar e il salvataggio CSV del messaggio precedente] ...

# --- VISUALIZZAZIONE ---
if not df.empty:
    st.metric("Valore Totale", f"{df['Valore'].sum():,.2f} €")
    
    for i, row in df.iterrows():
        # DIV con ID univoco per il JavaScript
        st.markdown(f'<div id="guitar-{i}"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        # ... [Resto del codice di visualizzazione uguale al precedente] ...
        
        with col1:
            percorso = os.path.join(CARTELLA_IMG, str(row['Foto']))
            if os.path.exists(percorso): st.image(percorso)
        
        with col2:
            st.write(f"### {row['Marca']} {row['Modello']}")
            # ... (logica corde, modifica, elimina) ...
            
        st.divider()