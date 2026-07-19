import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configurazione database e directory per l'archiviazione delle immagini
DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def init_db():
    """Inizializza il database e applica le migrazioni necessarie per supportare le nuove funzionalità."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Abilita le chiavi esterne per la cancellazione a cascata dello storico
    c.execute("PRAGMA foreign_keys = ON")
    
    # Tabella principale chitarre
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
    
    # Nuova tabella per lo storico delle manutenzioni
    c.execute('''
        CREATE TABLE IF NOT EXISTS storico_manutenzioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chitarra_id INTEGER,
            data_evento TEXT,
            tipo_evento TEXT,
            note_evento TEXT,
            FOREIGN KEY (chitarra_id) REFERENCES chitarre (id) ON DELETE CASCADE
        )
    ''')
    
    # Migrazione dinamica: verifica ed inserisce le colonne aggiunte nei vari aggiornamenti
    c.execute("PRAGMA table_info(chitarre)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'frequenza_mesi' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN frequenza_mesi INTEGER DEFAULT 3")
    if 'accordatura' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN accordatura TEXT DEFAULT 'E Standard'")
    if 'note_setup' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN note_setup TEXT DEFAULT ''")
    if 'marca' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN marca TEXT DEFAULT ''")
    if 'tipo' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN tipo TEXT DEFAULT 'Elettrica'")
        
    conn.commit()
    conn.close()

# Avvia l'inizializzazione o l'aggiornamento strutturale
init_db()

st.set_page_config(
    page_title="Guitar Vault Pro", 
    layout="wide", 
    page_icon="🎸",
    initial_sidebar_state="collapsed"
)

# Stile CSS integrato per migliorare l'aspetto visivo delle card, renderle responsive per smartphone
st.markdown("""
    <style>
    /* Ottimizzazioni generali per mobile */
    .reportview-container .main .block-container {
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
    }
    
    /* Card Chitarra con design moderno stile iOS/Material */
    .guitar-card {
        background-color: #f8fafc;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    @media (max-width: 768px) {
        .guitar-card {
            padding: 15px;
            margin-bottom: 15px;
        }
    }
    
    /* Box di stato con angoli arrotondati e colori vivaci */
    .warning-box {
        background-color: #fff5f5;
        border-left: 6px solid #e53e3e;
        padding: 12px;
        border-radius: 10px;
        color: #c53030;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .ok-box {
        background-color: #f0fff4;
        border-left: 6px solid #38a169;
        padding: 12px;
        border-radius: 10px;
        color: #22543d;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    /* Rende le immagini delle chitarre stabili e uniformi */
    .guitar-img {
        border-radius: 12px;
        object-fit: cover;
        max-height: 250px;
        width: 100%;
    }
    
    /* Nasconde elementi superflui su mobile per un look più pulito */
    .stDeployButton {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎸 Guitar Vault Pro")
st.subheader("La tua collezione sotto controllo")

conn = sqlite3.connect(DB_NAME)
df_stats = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if not df_stats.empty:
    oggi = datetime.now().date()
    da_cambiare_count = sum(
        datetime.strptime(x, "%Y-%m-%d").date() <= oggi 
        for x in df_stats['prossimo_cambio']
    )
    
    # Grid statistiche responsive
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Chitarre totali", len(df_stats))
    with col_stat2:
        st.metric("Corde da sostituire ⚠️", da_cambiare_count, delta=-da_cambiare_count if da_cambiare_count > 0 else 0, delta_color="inverse")
    with col_stat3:
        # Trova la data di scadenza più vicina in assoluto
        date_scadenze = [datetime.strptime(x, "%Y-%m-%d").date() for x in df_stats['prossimo_cambio']]
        prossima_scadenza = min(date_scadenze) if date_scadenze else "N/D"
        st.metric("Prossimo cambio", prossima_scadenza.strftime("%d/%m/%Y") if isinstance(prossima_scadenza, datetime) or hasattr(prossima_scadenza, 'strftime') else prossima_scadenza)
    st.markdown("---")

with st.sidebar.expander("➕ Inserisci una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        marca = st.text_input("Marca dello Strumento", placeholder="Es. Fender, Gibson")
        modello = st.text_input("Modello della Chitarra", placeholder="Es. Stratocaster")
            
        tipo = st.selectbox(
            "Tipo di Strumento",
            ["Elettrica", "Acustica", "Classica", "Semiacustica", "Basso", "Altro"]
        )
        serie = st.text_input("Numero di Serie (S/N)", placeholder="Es. CZ543210")
        
        corde = st.text_input("Corde Montate", placeholder="Es. Elixir Optiweb 09-42")
        accordatura = st.selectbox(
            "Accordatura", 
            ["E Standard", "Eb Standard", "D Standard", "Drop D", "Drop C", "Open G", "DADGAD", "Altro"]
        )
            
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            data_cambio = st.date_input("Ultimo Cambio Corde", datetime.now())
        with col_form2:
            frequenza_mesi = st.number_input("Frequenza cambio (mesi)", min_value=1, max_value=12, value=3)
        
        note_setup = st.text_area("Note di Setup & Liuteria", placeholder="Action, truss rod, regolazioni...", height=100)
        foto = st.file_uploader("Carica una foto dello strumento", type=["jpg", "jpeg", "png"])
        
        submit = st.form_submit_button("Metti al sicuro nel Vault")
        
        if submit and (marca or modello):
            prossimo_cambio = data_cambio + timedelta(days=int(frequenza_mesi) * 30)
            
            foto_path = ""
            if foto is not None:
                safe_serie = serie if serie else "noserial"
                foto_path = os.path.join(IMG_DIR, f"{safe_serie}_{foto.name}")
                with open(foto_path, "wb") as f:
                    f.write(foto.getbuffer())
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''
                INSERT INTO chitarre (marca, modello, serie, corde, data_cambio, prossimo_cambio, foto_path, frequenza_mesi, accordatura, note_setup, tipo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (marca, modello, serie, corde, str(data_cambio), str(prossimo_cambio), foto_path, int(frequenza_mesi), accordatura, note_setup, tipo))
            
            # Registra la creazione anche nello storico delle manutenzioni
            nuovo_id = c.lastrowid
            nome_completo = f"{marca} {modello}".strip()
            c.execute('''
                INSERT INTO storico_manutenzioni (chitarra_id, data_evento, tipo_evento, note_evento)
                VALUES (?, ?, ?, ?)
            ''', (nuovo_id, str(data_cambio), "Primo Setup & Cambio Corde", f"Chitarra {nome_completo} ({tipo}) aggiunta al database."))
            
            conn.commit()
            conn.close()
            st.success(f"La tua {nome_completo} è stata registrata!")
            st.rerun()

st.markdown("### 🔍 Trova e Gestisci")
ricerca = st.text_input("Cerca per marca, modello, serie o tipo...", placeholder="Scrivi una chiave di ricerca...")
solo_da_cambiare = st.checkbox("📅 Mostra solo chitarre da sostituire corde")

# Caricamento aggiornato dei dati dal database
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il tuo Vault è vuoto. Apri il pannello laterale per inserire il tuo primo strumento!")
else:
    df_filtrato = df.copy()
    
    if ricerca:
        df_filtrato = df_filtrato[
            df_filtrato['marca'].str.contains(ricerca, case=False, na=False) | 
            df_filtrato['modello'].str.contains(ricerca, case=False, na=False) | 
            df_filtrato['serie'].str.contains(ricerca, case=False, na=False) |
            df_filtrato['corde'].str.contains(ricerca, case=False, na=False) |
            df_filtrato.get('tipo', '').str.contains(ricerca, case=False, na=False)
        ]
        
    if solo_da_cambiare:
        oggi = datetime.now().date()
        df_filtrato = df_filtrato[df_filtrato['prossimo_cambio'].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d").date() <= oggi
        )]

    if df_filtrato.empty:
        st.warning("Nessun risultato corrispondente ai filtri.")
    else:
        st.markdown("---")
        
        for index, row in df_filtrato.iterrows():
            # Su schermi grandi usiamo 4 colonne, su mobile Streamlit le impilerà automaticamente in verticale!
            col_img, col_info, col_status, col_actions = st.columns([2, 3, 2.5, 2])
            
            # 1. Foto dello strumento
            with col_img:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], use_column_width=True)
                else:
                    # Immagine di fallback di una chitarra sfocata
                    st.image("https://images.unsplash.com/photo-1550985616-10810253b84d?w=400&auto=format&fit=crop&q=60", use_column_width=True)
            
            # 2. Informazioni tecniche dettagliate dello strumento
            with col_info:
                nome_marca = row.get('marca', '')
                nome_modello = row['modello']
                st.markdown(f"### {nome_marca} {nome_modello}".strip())
                
                st.markdown(f"🏷️ **Marca:** `{nome_marca if nome_marca else 'N/D'}`")
                st.markdown(f"🎸 **Modello:** `{nome_modello if nome_modello else 'N/D'}`")
                st.markdown(f"📁 **Tipo:** `{row.get('tipo', 'Elettrica')}`")
                st.markdown(f"🆔 **S/N:** `{row['serie'] if row['serie'] else 'N/D'}`")
                st.markdown(f"🧵 **Corde:** `{row['corde'] if row['corde'] else 'N/D'}`")
                st.markdown(f"🎵 **Accordatura:** `{row.get('accordatura', 'E Standard')}`")
                st.caption(f"Frequenza cambio: ogni {row['frequenza_mesi']} mesi")

            # 3. Stato scadenze manutenzione
            with col_status:
                data_scadenza = datetime.strptime(row['prossimo_cambio'], "%Y-%m-%d").date()
                oggi = datetime.now().date()
                
                st.markdown("##### 📅 Stato Corde")
                if data_scadenza <= oggi:
                    st.markdown(
                        f"""<div class='warning-box'>
                        <strong>DA SOSTITUIRE!</strong><br>
                        Termine scaduto il: {row['prossimo_cambio']}<br>
                        <small>Ultimo cambio: {row['data_cambio']}</small>
                        </div>""", 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""<div class='ok-box'>
                        <strong>Stato: Ottimale</strong><br>
                        Prossimo cambio: {row['prossimo_cambio']}<br>
                        <small>Ultimo cambio: {row['data_cambio']}</small>
                        </div>""", 
                        unsafe_allow_html=True
                    )
            
            # 4. Pulsantiera azioni rapide
            with col_actions:
                st.markdown("##### ⚙️ Azioni")
                
                # Azione 1: Registrazione rapida cambio corde
                key_cambio = f"cambio_{row['id']}"
                if st.button("🧼 Corde Cambiate!", key=key_cambio):
                    nuova_data = datetime.now().date()
                    nuovo_prossimo = nuova_data + timedelta(days=int(row['frequenza_mesi']) * 30)
                    
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute('''
                        UPDATE chitarre 
                        SET data_cambio = ?, prossimo_cambio = ? 
                        WHERE id = ?
                    ''', (str(nuova_data), str(nuovo_prossimo), row['id']))
                    
                    # Salva l'evento nello storico
                    c.execute('''
                        INSERT INTO storico_manutenzioni (chitarra_id, data_evento, tipo_evento, note_evento)
                        VALUES (?, ?, ?, ?)
                    ''', (row['id'], str(nuova_data), "Cambio Corde", f"Sostituita muta completa di corde ({row['corde']})."))
                    
                    conn.commit()
                    conn.close()
                    st.success("Scadenze reimpostate!")
                    st.rerun()
                
                # Azione 2: Rimozione della chitarra
                key_del = f"del_{row['id']}"
                if st.button("🗑️ Rimuovi Chitarra", key=key_del, type="secondary"):
                    if row['foto_path'] and os.path.exists(row['foto_path']):
                        try:
                            os.remove(row['foto_path'])
                        except Exception:
                            pass
                    
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("DELETE FROM chitarre WHERE id = ?", (row['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Strumento eliminato.")
                    st.rerun()

            with st.expander("🛠️ Note Setup e Storico", expanded=False):
                tab_setup, tab_storico = st.tabs(["📋 Setup", "📜 Diario"])
                
                with tab_setup:
                    st.markdown("##### Informazioni e misure di Setup")
                    nuove_note = st.text_area(
                        "Dettagli Setup", 
                        value=row.get('note_setup', ''), 
                        key=f"setup_notes_{row['id']}",
                        height=100
                    )
                    
                    if st.button("Salva Setup", key=f"save_setup_{row['id']}"):
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("UPDATE chitarre SET note_setup = ? WHERE id = ?", (nuove_note, row['id']))
                        conn.commit()
                        conn.close()
                        st.success("Setup salvato!")
                        st.rerun()
                
                with tab_storico:
                    st.markdown("##### Registro cronologico")
                    
                    with st.form(f"nuovo_evento_storico_{row['id']}"):
                        tipo_evento = st.text_input("Tipo Intervento", placeholder="Es. Regolazione Manico, Pulizia")
                        data_evento = st.date_input("Data Intervento", datetime.now())
                        desc_evento = st.text_area("Dettagli dell'intervento fatto")
                        aggiungi_evento = st.form_submit_button("Salva nel diario")
                        
                        if aggiungi_evento and tipo_evento:
                            conn = sqlite3.connect(DB_NAME)
                            c = conn.cursor()
                            c.execute('''
                                INSERT INTO storico_manutenzioni (chitarra_id, data_evento, tipo_evento, note_evento)
                                VALUES (?, ?, ?, ?)
                            ''', (row['id'], str(data_evento), tipo_evento, desc_evento))
                            conn.commit()
                            conn.close()
                            st.success("Intervento aggiunto!")
                            st.rerun()
                    
                    st.markdown("---")
                    
                    conn = sqlite3.connect(DB_NAME)
                    df_history = pd.read_sql_query(
                        "SELECT data_evento, tipo_evento, note_evento FROM storico_manutenzioni WHERE chitarra_id = ? ORDER BY data_evento DESC", 
                        conn, 
                        params=(row['id'],)
                    )
                    conn.close()
                    
                    if df_history.empty:
                        st.info("Nessuna manutenzione in archivio.")
                    else:
                        for _, h_row in df_history.iterrows():
                            try:
                                data_f = datetime.strptime(h_row['data_evento'], "%Y-%m-%d").strftime("%d/%m/%Y")
                            except Exception:
                                data_f = h_row['data_evento']
                                
                            st.markdown(f"📅 **{data_f}** - **{h_row['tipo_evento']}**")
                            if h_row['note_evento']:
                                st.caption(h_row['note_evento'])
                            st.markdown(" ")
            
            st.markdown("---")