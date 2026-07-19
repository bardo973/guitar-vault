import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configurazione database e immagini
DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Creazione tabella base
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT,
            serie TEXT,
            corde TEXT,
            data_cambio TEXT,
            prossimo_cambio TEXT,
            foto_path TEXT
        )
    ''')
    
    # Migrazione dinamica: aggiunge la colonna 'frequenza_mesi' se non esiste nel database
    c.execute("PRAGMA table_info(chitarre)")
    columns = [col[1] for col in c.fetchall()]
    if 'frequenza_mesi' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN frequenza_mesi INTEGER DEFAULT 3")
        
    conn.commit()
    conn.close()

# Inizializza o aggiorna il database
init_db()

# Configurazione pagina Streamlit
st.set_page_config(page_title="Guitar Vault Pro", layout="wide", page_icon="🎸")

# Stile CSS personalizzato per rendere l'interfaccia ancora più elegante
st.markdown("""
    <style>
    .guitar-card {
        background-color: #f8fafc;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #fff5f5;
        border-left: 5px solid #e53e3e;
        padding: 10px;
        border-radius: 5px;
    }
    .ok-box {
        background-color: #f0fff4;
        border-left: 5px solid #38a169;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allowed_html=True)

st.title("🎸 Guitar Vault Pro")
st.subheader("Gestione avanzata della tua collezione e manutenzione corde")

# --- PANNELLO LATERALE: INSERIMENTO NUOVA CHITARRA ---
with st.sidebar.expander("➕ Inserisci una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        modello = st.text_input("Modello della Chitarra", placeholder="Es. Gibson Les Paul Standard")
        serie = st.text_input("Numero di Serie", placeholder="Es. 215430XXX")
        corde = st.text_input("Corde Montate", placeholder="Es. Ernie Ball Paradigm 10-46")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            data_cambio = st.date_input("Ultimo Cambio Corde", datetime.now())
        with col_form2:
            frequenza_mesi = st.number_input("Frequenza cambio (mesi)", min_value=1, max_value=12, value=3)
        
        foto = st.file_uploader("Fotografia dello strumento", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Aggiungi al Vault")
        
        if submit and modello:
            # Calcolo della data del prossimo cambio basata sulla frequenza scelta
            prossimo_cambio = data_cambio + timedelta(days=int(frequenza_mesi) * 30)
            
            foto_path = ""
            if foto is not None:
                # Evitiamo sovrascritture usando il numero di serie o il timestamp nel nome del file
                safe_serie = serie if serie else "noserial"
                foto_path = os.path.join(IMG_DIR, f"{safe_serie}_{foto.name}")
                with open(foto_path, "wb") as f:
                    f.write(foto.getbuffer())
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO chitarre (modello, serie, corde, data_cambio, prossimo_cambio, foto_path, frequenza_mesi)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (modello, serie, corde, str(data_cambio), str(prossimo_cambio), foto_path, int(frequenza_mesi)))
            conn.commit()
            conn.close()
            st.success(f"La tua {modello} è stata blindata nel Vault!")
            st.rerun()

# --- FILTRI DI RICERCA NELLA SCHERMATA PRINCIPALE ---
st.markdown("### 🔍 Trova e Filtra la tua Collezione")
col_search1, col_search2 = st.columns([2, 1])

with col_search1:
    ricerca = st.text_input("Cerca per modello o numero di serie...", placeholder="Digita per filtrare...")
with col_search2:
    solo_da_cambiare = st.checkbox("📅 Mostra solo chitarre da cambiare")

# --- CARICAMENTO E FILTRAGGIO DATI ---
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il tuo Vault è vuoto. Apri il pannello a sinistra per registrare la tua prima chitarra!")
else:
    # Applichiamo i filtri se l'utente digita o seleziona opzioni
    df_filtrato = df.copy()
    
    if ricerca:
        df_filtrato = df_filtrato[
            df_filtrato['modello'].str.contains(ricerca, case=False, na=False) | 
            df_filtrato['serie'].str.contains(ricerca, case=False, na=False)
        ]
        
    if solo_da_cambiare:
        oggi = datetime.now().date()
        # Filtriamo le righe dove la data del prossimo cambio è passata o è oggi
        df_filtrato = df_filtrato[df_filtrato['prossimo_cambio'].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d").date() <= oggi
        )]

    # --- MOSTRA LE CHITARRE FILTRATE ---
    if df_filtrato.empty:
        st.warning("Nessuna chitarra corrisponde ai filtri impostati.")
    else:
        st.write(f"Strumenti visualizzati: **{len(df_filtrato)}**")
        st.markdown("---")
        
        for index, row in df_filtrato.iterrows():
            # Generiamo una card visiva usando colonne Streamlit
            col_img, col_info, col_status, col_actions = st.columns([1.5, 2.5, 2, 1.5])
            
            # 1. Colonna Immagine
            with col_img:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], use_column_width=True)
                else:
                    # Immagine di fallback se non è stata caricata nessuna foto
                    st.image("https://images.unsplash.com/photo-1550985616-10810253b84d?w=400&auto=format&fit=crop&q=60", use_column_width=True)
            
            # 2. Colonna Informazioni Generali
            with col_info:
                st.markdown(f"### {row['modello']}")
                st.markdown(f"🆔 **S/N:** `{row['serie'] if row['serie'] else 'N/D'}`")
                st.markdown(f"🎸 **Corde:** `{row['corde'] if row['corde'] else 'N/D'}`")
                st.caption(f"Frequenza programmata: ogni {row['frequenza_mesi']} mesi")

            # 3. Colonna Stato Manutenzione
            with col_status:
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                oggi = datetime.now().date()
                
                st.markdown("##### 📅 Stato Corde")
                if data_scadenza <= oggi:
                    st.markdown(
                        f"""<div class='warning-box'>
                        <strong>DA CAMBIARE!</strong><br>
                        Scadenza il: {row['prossimo_cambio']}<br>
                        <small>Ultimo cambio: {row['data_cambio']}</small>
                        </div>""", 
                        unsafe_allowed_html=True
                    )
                else:
                    st.markdown(
                        f"""<div class='ok-box'>
                        <strong>Stato: OK</strong><br>
                        Prossimo cambio: {row['prossimo_cambio']}<br>
                        <small>Ultimo cambio: {row['data_cambio']}</small>
                        </div>""", 
                        unsafe_allowed_html=True
                    )
            
            # 4. Colonna Azioni Rapide
            with col_actions:
                st.markdown("##### ⚙️ Azioni")
                
                # Bottone per resettare il cambio corde a oggi
                key_cambio = f"cambio_{row['id']}"
                if st.button("🧼 Corde Cambiate!", key=key_cambio, help="Clicca qui se hai appena cambiato le corde a questa chitarra"):
                    nuova_data = datetime.now().date()
                    nuovo_prossimo = nuova_data + timedelta(days=int(row['frequenza_mesi']) * 30)
                    
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute('''
                        UPDATE chitarre 
                        SET data_cambio = ?, prossimo_cambio = ? 
                        WHERE id = ?
                    ''', (str(nuova_data), str(nuovo_prossimo), row['id']))
                    conn.commit()
                    conn.close()
                    st.success("Stato corde aggiornato!")
                    st.rerun()
                
                # Bottone per eliminare lo strumento con pop-up di conferma nativo di Streamlit
                key_del = f"del_{row['id']}"
                if st.button("🗑️ Elimina", key=key_del, type="secondary"):
                    # Eliminiamo la foto dal computer per non sprecare spazio
                    if row['foto_path'] and os.path.exists(row['foto_path']):
                        try:
                            os.remove(row['foto_path'])
                        except Exception:
                            pass # Ignora se il file è bloccato o già rimosso
                    
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("DELETE FROM chitarre WHERE id = ?", (row['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Strumento rimosso dal database.")
                    st.rerun()
            