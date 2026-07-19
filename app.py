import streamlit as st
import sqlite3
import os
import base64
from PIL import Image
import io

def init_db():
    conn = sqlite3.connect("guitars.db")
    c = conn.cursor()
    # Crea la tabella principale se non esiste
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modello TEXT,
            tipo TEXT,
            anno TEXT,
            prezzo REAL,
            note TEXT,
            foto BLOB,
            marca_corde TEXT DEFAULT '',
            spessore_corde TEXT DEFAULT ''
        )
    ''')
    
    # Controllo migrazione colonne per aggiornamenti progressivi del DB
    c.execute("PRAGMA table_info(chitarre)")
    colonne = [colonna[1] for colonna in c.fetchall()]
    
    # Se mancano le colonne introdotte nei vari aggiornamenti, le aggiungiamo dinamicamente
    if "tipo" not in colonne:
        try:
            c.execute("ALTER TABLE chitarre ADD COLUMN tipo TEXT DEFAULT 'Elettrica'")
            conn.commit()
        except Exception:
            pass
            
    if "anno" not in colonne:
        try:
            c.execute("ALTER TABLE chitarre ADD COLUMN anno TEXT DEFAULT ''")
            conn.commit()
        except Exception:
            pass

    if "marca_corde" not in colonne:
        try:
            c.execute("ALTER TABLE chitarre ADD COLUMN marca_corde TEXT DEFAULT ''")
            conn.commit()
        except Exception:
            pass

    if "spessore_corde" not in colonne:
        try:
            c.execute("ALTER TABLE chitarre ADD COLUMN spessore_corde TEXT DEFAULT ''")
            conn.commit()
        except Exception:
            pass
            
    conn.close()

# Esegui l'inizializzazione o la migrazione del DB
init_db()

# Gestione dell'icona dell'applicazione (logo.png se presente, altrimenti l'emoji)
ICON_PATH = "logo.png"
app_icon = ICON_PATH if os.path.exists(ICON_PATH) else "🎸"

st.set_page_config(
    page_title="Guitar Vault Pro", 
    layout="wide", 
    page_icon=app_icon,
    initial_sidebar_state="expanded"
)

# Inizializza lo stato per la gestione della modifica se non presente
if "edit_guitar_id" not in st.session_state:
    st.session_state.edit_guitar_id = None

st.markdown("""
<style>
    /* Sfondo principale scuro con immagine atmosferica di chitarre */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)), 
                          url('https://images.unsplash.com/photo-1510915361894-db8b60106cb1?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f5f5f7;
    }
    
    /* Design Glassmorphism per la Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(25, 20, 20, 0.45) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Titoli dorati premium */
    h1, h2, h3 {
        color: #f1c40f !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Card Chitarre in stile iOS Glassmorphism */
    .guitar-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .guitar-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(241, 196, 15, 0.15);
        border: 1px solid rgba(241, 196, 15, 0.3);
    }
    
    /* Ottimizzazione immagini delle chitarre */
    .guitar-img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Badge del tipo di strumento */
    .badge {
        background: rgba(241, 196, 15, 0.2);
        color: #f1c40f;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
        border: 1px solid rgba(241, 196, 15, 0.4);
    }
    
    /* Stile dettagli tecnici */
    .details-label {
        color: #8e8e93;
        font-size: 0.85rem;
        margin-bottom: 2px;
    }
    .details-val {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    /* Pulsanti ottimizzati per dita su iPhone */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    /* Bottone primario d'inserimento o salvataggio */
    div[data-testid="stSidebar"] .stButton>button {
        width: 100%;
        background-color: #f1c40f !important;
        color: #000000 !important;
        border: none !important;
    }
    
    div[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #f39c12 !important;
        box-shadow: 0 0 10px rgba(241, 196, 15, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

def aggiungi_chitarra(marca, modello, tipo, anno, prezzo, note, foto_bytes, marca_corde, spessore_corde):
    conn = sqlite3.connect("guitars.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO chitarre (marca, modello, tipo, anno, prezzo, note, foto, marca_corde, spessore_corde) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (marca, modello, tipo, anno, prezzo, note, foto_bytes, marca_corde, spessore_corde)
    )
    conn.commit()
    conn.close()

def modifica_chitarra(id_chitarra, marca, modello, tipo, anno, prezzo, note, marca_corde, spessore_corde, foto_bytes=None):
    conn = sqlite3.connect("guitars.db")
    c = conn.cursor()
    if foto_bytes is not None:
        c.execute(
            "UPDATE chitarre SET marca=?, modello=?, tipo=?, anno=?, prezzo=?, note=?, marca_corde=?, spessore_corde=?, foto=? WHERE id=?",
            (marca, modello, tipo, anno, prezzo, note, marca_corde, spessore_corde, foto_bytes, id_chitarra)
        )
    else:
        c.execute(
            "UPDATE chitarre SET marca=?, modello=?, tipo=?, anno=?, prezzo=?, note=?, marca_corde=?, spessore_corde=? WHERE id=?",
            (marca, modello, tipo, anno, prezzo, note, marca_corde, spessore_corde, id_chitarra)
        )
    conn.commit()
    conn.close()

def elimina_chitarra(id_chitarra):
    conn = sqlite3.connect("guitars.db")
    c = conn.cursor()
    c.execute("DELETE FROM chitarre WHERE id = ?", (id_chitarra,))
    conn.commit()
    conn.close()

def ottieni_chitarre():
    conn = sqlite3.connect("guitars.db")
    c = conn.cursor()
    c.execute("SELECT id, marca, modello, tipo, anno, prezzo, note, foto, marca_corde, spessore_corde FROM chitarre ORDER BY id DESC")
    guitars = c.fetchall()
    conn.close()
    return guitars

def ottieni_singola_chitarra(id_chitarra):
    conn = sqlite3.connect("guitars.db")
    c = conn.cursor()
    c.execute("SELECT id, marca, modello, tipo, anno, prezzo, note, foto, marca_corde, spessore_corde FROM chitarre WHERE id = ?", (id_chitarra,))
    guitar = c.fetchone()
    conn.close()
    return guitar

with st.sidebar:
    if os.path.exists(ICON_PATH):
        st.image(ICON_PATH, use_container_width=True)
    else:
        st.title("🎸 Guitar Vault")
        
    st.subheader("La tua Collezione Privata")
    st.write("Catalogazione e valutazione in tempo reale.")
    st.markdown("---")
    
    is_editing = st.session_state.edit_guitar_id is not None
    
    # Modifica di una chitarra esistente
    if is_editing:
        st.markdown("### ✏️ Modifica Strumento")
        guitar_data = ottieni_singola_chitarra(st.session_state.edit_guitar_id)
        
        if guitar_data:
            g_id, g_marca, g_modello, g_tipo, g_anno, g_prezzo, g_note, g_foto, g_marca_corde, g_spessore_corde = guitar_data
            
            marca = st.text_input("Marca *", value=g_marca)
            modello = st.text_input("Modello *", value=g_modello)
            
            lista_tipi = ["Elettrica", "Acustica", "Classica", "Semiacustica", "Basso", "Altro"]
            indice_tipo = lista_tipi.index(g_tipo) if g_tipo in lista_tipi else 0
            tipo = st.selectbox("Tipo di Strumento", options=lista_tipi, index=indice_tipo)
            
            anno = st.text_input("Anno di Costruzione", value=g_anno, placeholder="es: 1959 o Anni '60")
            prezzo = st.number_input("Prezzo d'acquisto (€)", min_value=0.0, step=50.0, value=float(g_prezzo or 0.0))
            
            marca_corde = st.text_input("Marca Corde", value=g_marca_corde or "", placeholder="Es. D'Addario, Ernie Ball...")
            spessore_corde = st.text_input("Spessore Corde / Scalatura", value=g_spessore_corde or "", placeholder="Es. 09-42, 10-46...")
            
            note = st.text_area("Note e Specifiche", value=g_note, placeholder="Es. Pickup sostituiti, liutaio...")
            
            st.markdown("<p style='font-size:0.85rem; color:#8e8e93;'>Carica una nuova foto solo se desideri sostituire quella attuale.</p>", unsafe_allow_html=True)
            foto_upload = st.file_uploader("Sostituisci Foto (opzionale)", type=["png", "jpg", "jpeg"])
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("Salva Modifiche"):
                    if not marca or not modello:
                        st.error("Inserisci Marca e Modello!")
                    else:
                        foto_bytes = None
                        if foto_upload is not None:
                            foto_bytes = foto_upload.read()
                            
                        modifica_chitarra(g_id, marca, modello, tipo, anno, prezzo, note, marca_corde, spessore_corde, foto_bytes)
                        st.success("Strumento aggiornato!")
                        st.session_state.edit_guitar_id = None
                        st.rerun()
            with col_cancel:
                if st.button("Annulla"):
                    st.session_state.edit_guitar_id = None
                    st.rerun()
        else:
            st.error("Strumento non trovato.")
            st.session_state.edit_guitar_id = None
            st.rerun()
            
    # Aggiunta di una nuova chitarra
    else:
        st.markdown("### ➕ Aggiungi Strumento")
        marca = st.text_input("Marca *", placeholder="Es. Fender, Gibson, Ibanez...")
        modello = st.text_input("Modello *", placeholder="Es. Stratocaster, Les Paul...")
        tipo = st.selectbox("Tipo di Strumento", ["Elettrica", "Acustica", "Classica", "Semiacustica", "Basso", "Altro"])
        anno = st.text_input("Anno di Costruzione", placeholder="Es. 1996 o Anni '70")
        prezzo = st.number_input("Prezzo d'acquisto (€)", min_value=0.0, step=50.0, format="%.2f")
        
        marca_corde = st.text_input("Marca Corde", placeholder="Es. Ernie Ball, Elixir, D'Addario...")
        spessore_corde = st.text_input("Spessore Corde / Scalatura", placeholder="Es. 09-42, 10-46...")
        
        note = st.text_area("Note / Specifiche", placeholder="Es. Setup appena fatto, tasti 90%...")
        foto_upload = st.file_uploader("Foto dello Strumento", type=["png", "jpg", "jpeg"])
        
        if st.button("Aggiungi alla Collezione"):
            if not marca or not modello:
                st.error("La marca e il modello sono obbligatori!")
            else:
                foto_bytes = None
                if foto_upload is not None:
                    foto_bytes = foto_upload.read()
                
                aggiungi_chitarra(marca, modello, tipo, anno, prezzo, note, foto_bytes, marca_corde, spessore_corde)
                st.success(f"{marca} aggiunta con successo!")
                st.rerun()

st.title("🎸 Guitar Vault Pro")
st.write("Il tuo caveau digitale personale per catalogare, tracciare e valutare i tuoi strumenti musicali.")

guitars = ottieni_chitarre()

if not guitars:
    st.info("Il tuo caveau è vuoto. Usa il modulo a sinistra nella barra laterale per aggiungere la tua prima chitarra!")
else:
    valore_totale = sum(g[5] for g in guitars if g[5] is not None)
    totale_strumenti = len(guitars)
    
    st.markdown(f"""
    <div style='display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap;'>
        <div style='background: rgba(255,255,255,0.05); padding: 15px 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); flex: 1; min-width: 200px;'>
            <div style='color:#8e8e93; font-size: 0.9rem;'>Valore Totale Stimato</div>
            <div style='color:#f1c40f; font-size: 1.8rem; font-weight: 700;'>€ {valore_totale:,.2f}</div>
        </div>
        <div style='background: rgba(255,255,255,0.05); padding: 15px 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); flex: 1; min-width: 200px;'>
            <div style='color:#8e8e93; font-size: 0.9rem;'>Strumenti in Custodia</div>
            <div style='color:#ffffff; font-size: 1.8rem; font-weight: 700;'>{totale_strumenti}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    for idx, guitar in enumerate(guitars):
        col = cols[idx % 3]
        
        g_id, g_marca, g_modello, g_tipo, g_anno, g_prezzo, g_note, g_foto, g_marca_corde, g_spessore_corde = guitar
        
        with col:
            if g_foto:
                base64_image = base64.b64encode(g_foto).decode("utf-8")
                img_html = f'<img class="guitar-img" src="data:image/png;base64,{base64_image}" />'
            else:
                img_html = '<div style="width:100%; height:250px; border-radius:12px; background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center; margin-bottom:15px; border: 1px dashed rgba(255,255,255,0.2);"><span style="font-size:3rem;">🎸</span></div>'
                
            # Rendering della scheda iOS curata nei minimi dettagli con icone
            st.markdown(f"""
            <div class="guitar-card">
                {img_html}
                <span class="badge">{g_tipo}</span>
                <h3 style="margin: 5px 0 15px 0; font-size: 1.4rem;">{g_marca} {g_modello}</h3>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <div style="flex: 1;">
                        <div class="details-label">📅 Anno</div>
                        <div class="details-val">{g_anno if g_anno else "N/D"}</div>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div class="details-label">💰 Acquisto</div>
                        <div class="details-val">€ {g_prezzo:,.2f}</div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px; margin-bottom: 12px;">
                    <div style="flex: 1;">
                        <div class="details-label">🧵 Marca Corde</div>
                        <div class="details-val" style="font-size: 0.95rem;">{g_marca_corde if g_marca_corde else "Non spec."}</div>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div class="details-label">📐 Scalatura</div>
                        <div class="details-val" style="font-size: 0.95rem;">{g_spessore_corde if g_spessore_corde else "Non spec."}</div>
                    </div>
                </div>
                
                <div class="details-label">📝 Note / Specifiche</div>
                <p style="font-size: 0.95rem; color:#e5e5ea; min-height: 50px; line-height: 1.4; margin-bottom: 15px;">
                    {g_note if g_note else "Nessuna nota aggiuntiva."}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col_actions_1, col_actions_2 = st.columns(2)
            
            with col_actions_1:
                valore_query = f"{g_marca} {g_modello} {g_anno}".strip()
                reverb_url = f"https://reverb.com/marketplace?query={valore_query.replace(' ', '+')}"
                google_url = f"https://www.google.com/search?q={valore_query.replace(' ', '+')}+valore+usato"
                
                st.markdown(f"""
                <div style="display: flex; gap: 5px; margin-bottom: 10px;">
                    <a href="{reverb_url}" target="_blank" style="flex: 1; text-decoration: none;">
                        <button style="width: 100%; height: 35px; background: #e15400; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.8rem;">Valuta Reverb</button>
                    </a>
                    <a href="{google_url}" target="_blank" style="flex: 1; text-decoration: none;">
                        <button style="width: 100%; height: 35px; background: #34a853; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 0.8rem;">Valuta Google</button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
            with col_actions_2:
                col_btn_edit, col_btn_del = st.columns(2)
                
                with col_btn_edit:
                    if st.button("✏️ Modifica", key=f"edit_btn_{g_id}", use_container_width=True):
                        st.session_state.edit_guitar_id = g_id
                        st.rerun()
                        
                with col_btn_del:
                    if st.button("🗑️ Elimina", key=f"del_btn_{g_id}", use_container_width=True):
                        elimina_chitarra(g_id)
                        st.success("Strumento eliminato.")
                        st.rerun()
                        
            st.markdown("<br>", unsafe_allow_html=True)