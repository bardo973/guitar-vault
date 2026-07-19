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
        
    conn.commit()
    conn.close()

# Avvia l'inizializzazione o l'aggiornamento strutturale
init_db()

st.set_page_config(page_title="Guitar Vault Pro", layout="wide", page_icon="🎸")

# Stile CSS integrato per migliorare l'aspetto visivo delle card e dei badge di stato
st.markdown("""
    <style>
    .guitar-card {
        background-color: #f8fafc;
        border-radius: 15px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .warning-box {
        background-color: #fff5f5;
        border-left: 5px solid #e53e3e;
        padding: 12px;
        border-radius: 8px;
        color: #c53030;
    }
    .ok-box {
        background-color: #f0fff4;
        border-left: 5px solid #38a169;
        padding: 12px;
        border-radius: 8px;
        color: #22543d;
    }
    .stat-val {
        font-size: 2rem;
        font-weight: bold;
        color: #1a202c;
    }
    </style>
""", unsafe_allowed_html=True)

st.title("🎸 Guitar Vault Pro")
st.subheader("La tua collezione sotto controllo: manutenzione, setup e storico")

conn = sqlite3.connect(DB_NAME)
df_stats = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if not df_stats.empty:
    oggi = datetime.now().date()
    da_cambiare_count = sum(
        datetime.strptime(x, "%Y-%m-%d").date() <= oggi 
        for x in df_stats['prossimo_cambio']
    )
    
    st.markdown("### 📊 Stato della Collezione")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Chitarre totali nel Vault", len(df_stats))
    with col_stat2:
        st.metric("Corde da sostituire immediatamente ⚠️", da_cambiare_count, delta=-da_cambiare_count if da_cambiare_count > 0 else 0, delta_color="inverse")
    with col_stat3:
        # Trova la data di scadenza più vicina in assoluto
        date_scadenze = [datetime.strptime(x, "%Y-%m-%d").date() for x in df_stats['prossimo_cambio']]
        prossima_scadenza = min(date_scadenze) if date_scadenze else "N/D"
        st.metric("Prossimo intervento programmato", prossima_scadenza.strftime("%d/%m/%Y") if isinstance(prossima_scadenza, datetime) or hasattr(prossima_scadenza, 'strftime') else prossima_scadenza)
    st.markdown("---")

with st.sidebar.expander("➕ Inserisci una nuova chitarra", expanded=False):
    with st.form("nuova_chitarra"):
        modello = st.text_input("Modello della Chitarra", placeholder="Es. Fender Stratocaster Custom Shop")
        serie = st.text_input("Numero di Serie (S/N)", placeholder="Es. CZ543210")
        
        col_side1, col_side2 = st.columns(2)
        with col_side1:
            corde = st.text_input("Corde Montate", placeholder="Es. Elixir Optiweb 09-42")
        with col_side2:
            accordatura = st.selectbox(
                "Accordatura", 
                ["E Standard", "Eb Standard", "D Standard", "Drop D", "Drop C", "Open G", "DADGAD", "Altro"]
            )
            
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            data_cambio = st.date_input("Ultimo Cambio Corde", datetime.now())
        with col_form2:
            frequenza_mesi = st.number_input("Frequenza cambio (mesi)", min_value=1, max_value=12, value=3)
        
        note_setup = st.text_area("Note di Setup & Liuteria", placeholder="Es. Action: 1.5mm cantino / 1.8mm bassone. Truss rod regolato a Gennaio.", height=100)
        foto = st.file_uploader("Carica una foto dello strumento", type=["jpg", "jpeg", "png"])
        
        submit = st.form_submit_button("Metti al sicuro nel Vault")
        
        if submit and modello:
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
                INSERT INTO chitarre (modello, serie, corde, data_cambio, prossimo_cambio, foto_path, frequenza_mesi, accordatura, note_setup)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (modello, serie, corde, str(data_cambio), str(prossimo_cambio), foto_path, int(frequenza_mesi), accordatura, note_setup))
            
            # Registra la creazione anche nello storico delle manutenzioni
            nuovo_id = c.lastrowid
            c.execute('''
                INSERT INTO storico_manutenzioni (chitarra_id, data_evento, tipo_evento, note_evento)
                VALUES (?, ?, ?, ?)
            ''', (nuovo_id, str(data_cambio), "Primo Setup & Cambio Corde", f"Chitarra aggiunta al database con corde {corde} in accordatura {accordatura}."))
            
            conn.commit()
            conn.close()
            st.success(f"La tua {modello} è stata blindata nel Vault!")
            st.rerun()

st.markdown("### 🔍 Trova e Gestisci i tuoi Strumenti")
col_search1, col_search2 = st.columns([2, 1])

with col_search1:
    ricerca = st.text_input("Cerca per modello, numero di serie o corde...", placeholder="Scrivi una chiave di ricerca...")
with col_search2:
    solo_da_cambiare = st.checkbox("📅 Mostra solo chitarre da sostituire corde")

# Caricamento aggiornato dei dati dal database
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM chitarre", conn)
conn.close()

if df.empty:
    st.info("Il tuo Vault è vuoto. Apri il pannello a comparsa di sinistra per inserire il tuo primo strumento!")
else:
    df_filtrato = df.copy()
    
    if ricerca:
        df_filtrato = df_filtrato[
            df_filtrato['modello'].str.contains(ricerca, case=False, na=False) | 
            df_filtrato['serie'].str.contains(ricerca, case=False, na=False) |
            df_filtrato['corde'].str.contains(ricerca, case=False, na=False)
        ]
        
    if solo_da_cambiare:
        oggi = datetime.now().date()
        df_filtrato = df_filtrato[df_filtrato['prossimo_cambio'].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d").date() <= oggi
        )]

    if df_filtrato.empty:
        st.warning("Nessuna chitarra corrisponde ai filtri impostati.")
    else:
        st.write(f"Strumenti filtrati: **{len(df_filtrato)}**")
        st.markdown("---")
        
        for index, row in df_filtrato.iterrows():
            # Layout diviso in 4 sezioni: Foto, Specifiche, Stato Manutenzione, Azioni Veloci
            col_img, col_info, col_status, col_actions = st.columns([1.5, 2.5, 2, 1.5])
            
            # 1. Foto dello strumento
            with col_img:
                if row['foto_path'] and os.path.exists(row['foto_path']):
                    st.image(row['foto_path'], use_column_width=True)
                else:
                    # Immagine segnaposto stilosa in caso di assenza foto
                    st.image("https://images.unsplash.com/photo-1550985616-10810253b84d?w=400&auto=format&fit=crop&q=60", use_column_width=True)
            
            # 2. Informazioni tecniche ed estetiche
            with col_info:
                st.markdown(f"### {row['modello']}")
                st.markdown(f"🆔 **S/N:** `{row['serie'] if row['serie'] else 'N/D'}`")
                st.markdown(f"🎸 **Corde:** `{row['corde'] if row['corde'] else 'N/D'}`")
                st.markdown(f"🎵 **Accordatura:** `{row.get('accordatura', 'E Standard')}`")
                st.caption(f"Frequenza manutenzione programmata: ogni {row['frequenza_mesi']} mesi")

            # 3. Stato usura corde e notifiche
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
                        unsafe_allowed_html=True
                    )
                else:
                    st.markdown(
                        f"""<div class='ok-box'>
                        <strong>Stato: Ottimale</strong><br>
                        Prossimo cambio: {row['prossimo_cambio']}<br>
                        <small>Ultimo cambio: {row['data_cambio']}</small>
                        </div>""", 
                        unsafe_allowed_html=True
                    )
            
            # 4. Pulsantiera azioni rapide
            with col_actions:
                st.markdown("##### ⚙️ Azioni")
                
                # Azione 1: Registrazione rapida cambio corde
                key_cambio = f"cambio_{row['id']}"
                if st.button("🧼 Corde Cambiate!", key=key_cambio, help="Resetta la scadenza impostando la data odierna"):
                    nuova_data = datetime.now().date()
                    nuovo_prossimo = nuova_data + timedelta(days=int(row['frequenza_mesi']) * 30)
                    
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    # Aggiorna date nella tabella principale
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
                    st.success("Storico aggiornato e scadenze reimpostate!")
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
                    st.success("Strumento eliminato permanentemente.")
                    st.rerun()

            # Expander in fondo ad ogni card per mostrare i dettagli della chitarra, storici e note setup
            with st.expander("🛠️ Note di Setup & Registro Storico Manutenzioni", expanded=False):
                tab_setup, tab_storico = st.tabs(["📋 Scheda di Setup", "📜 Storico Interventi"])
                
                # TAB SETUP: Permette anche di modificare le note di setup al volo
                with tab_setup:
                    st.markdown("##### Informazioni e misure di Setup")
                    nuove_note = st.text_area(
                        "Dettagli Setup (Action, Truss rod, ponti, pickup, modifiche)", 
                        value=row.get('note_setup', ''), 
                        key=f"setup_notes_{row['id']}",
                        height=120
                    )
                    
                    # Salva le note modificate
                    if st.button("Aggiorna Scheda Setup", key=f"save_setup_{row['id']}"):
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("UPDATE chitarre SET note_setup = ? WHERE id = ?", (nuove_note, row['id']))
                        conn.commit()
                        conn.close()
                        st.success("Scheda di setup aggiornata!")
                        st.rerun()
                
                # TAB STORICO: Mostra tutti gli eventi passati legati alla chitarra
                with tab_storico:
                    st.markdown("##### Registro cronologico delle manutenzioni")
                    
                    # Form veloce per registrare interventi extra (es. regolazione truss rod, lucidatura tasti)
                    with st.form(f"nuovo_evento_storico_{row['id']}"):
                        col_ev1, col_ev2 = st.columns(2)
                        with col_ev1:
                            tipo_evento = st.text_input("Tipo Intervento", placeholder="Es. Regolazione Truss Rod, Pulizia")
                        with col_ev2:
                            data_evento = st.date_input("Data Intervento", datetime.now())
                        
                        desc_evento = st.text_area("Dettagli dell'intervento fatto", placeholder="Es. Allentato truss rod di 1/4 di giro. Pulito tastiera con olio di limone.")
                        aggiungi_evento = st.form_submit_button("Registra nel diario")
                        
                        if aggiungi_evento and tipo_evento:
                            conn = sqlite3.connect(DB_NAME)
                            c = conn.cursor()
                            c.execute('''
                                INSERT INTO storico_manutenzioni (chitarra_id, data_evento, tipo_evento, note_evento)
                                VALUES (?, ?, ?, ?)
                            ''', (row['id'], str(data_evento), tipo_evento, desc_evento))
                            conn.commit()
                            conn.close()
                            st.success("Evento registrato con successo!")
                            st.rerun()
                    
                    st.markdown("---")
                    
                    # Caricamento e rendering degli eventi dello storico registrati
                    conn = sqlite3.connect(DB_NAME)
                    df_history = pd.read_sql_query(
                        "SELECT data_evento, tipo_evento, note_evento FROM storico_manutenzioni WHERE chitarra_id = ? ORDER BY data_evento DESC", 
                        conn, 
                        params=(row['id'],)
                    )
                    conn.close()
                    
                    if df_history.empty:
                        st.info("Nessuna manutenzione registrata in archivio.")
                    else:
                        for _, h_row in df_history.iterrows():
                            # Conversione formattazione data per visualizzazione italiana
                            try:
                                data_f = datetime.strptime(h_row['data_evento'], "%Y-%m-%d").strftime("%d/%m/%Y")
                            except Exception:
                                data_f = h_row['data_evento']
                                
                            st.markdown(f"📅 **{data_f}** - **{h_row['tipo_evento']}**")
                            if h_row['note_evento']:
                                st.caption(h_row['note_evento'])
                            st.markdown(" ")
            
            st.markdown("---")