import streamlit as st
import pandas as pd
import numpy as np

# Configurazione pagina
st.set_page_config(page_title="Fantacalcio 3D Cards & Mercato", layout="wide")

# CSS Avanzato per Flip Card 3D, Shimmer, Glassmorphism e Olografico
st.markdown("""
<style>
/* Stili Generali e Palette */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Container principale della Flip Card 3D */
.card-container {
    perspective: 1000px;
    width: 100%;
    max-width: 340px;
    height: 480px;
    margin: 15px auto;
}

.card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    transform-style: preserve-3d;
    box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    border-radius: 20px;
}

.card-container:hover .card-inner {
    transform: rotateY(180deg);
}

.card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.2);
}

/* Glassmorphism e sfondi */
.card-front {
    background: linear-gradient(135deg, #1a1c29 0%, #3a3f58 100%);
    color: white;
}

.card-back {
    background: linear-gradient(135deg, #2c3e50 0%, #000000 100%);
    color: white;
    transform: rotateY(180deg);
    padding: 20px;
    text-align: left;
}

/* Effetto Shimmer / Luce dinamica */
.card-front::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to right,
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,0.15) 50%,
        rgba(255,255,255,0) 100%
    );
    transform: rotate(30deg);
    pointer-events: none;
    animation: shimmer 6s infinite linear;
}

@keyframes shimmer {
    0% { transform: translateY(-100%) translateX(-100%) rotate(30deg); }
    20% { transform: translateY(100%) translateX(100%) rotate(30deg); }
    100% { transform: translateY(100%) translateX(100%) rotate(30deg); }
}

/* Badge Olografico */
.holographic-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: linear-gradient(135deg, #ff007f, #7f00ff, #00f0ff, #ff007f);
    background-size: 300% 300%;
    animation: holo-shift 4s ease infinite;
    color: white;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: 800;
    border-radius: 20px;
    box-shadow: 0 0 10px rgba(255,255,255,0.5);
    z-index: 10;
    text-transform: uppercase;
    letter-spacing: 1px;
}

@keyframes holo-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.player-header {
    padding: 25px 15px 10px 15px;
}

.player-name {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 2px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.player-meta {
    font-size: 13px;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.player-quotation {
    font-size: 28px;
    font-weight: 800;
    color: #00ffcc;
    margin: 15px 0;
    text-shadow: 0 0 10px rgba(0,255,204,0.4);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    padding: 0 20px;
}

.stat-box {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 8px;
    border-radius: 10px;
    text-align: center;
}

.stat-label {
    font-size: 10px;
    color: #cbd5e0;
    text-transform: uppercase;
}

.stat-value {
    font-size: 16px;
    font-weight: 700;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Funzione di rendering della Flip Card 3D
def render_flip_card(row, stats_per_stagione=None):
    nome = row.get("Nome", "Sconosciuto")
    ruolo = row.get("Ruolo", "P")
    squadra = row.get("Squadra_SerieA", "N/A")
    quotazione = row.get("Quotazione", 0)
    prezzo_consigliato = row.get("Prezzo_Consigliato", 0)
    
    # Statistiche dimostrative (o estratte da stats_per_stagione se presenti)
    f_media = row.get("Fanta_Media", 6.5)
    giornate = row.get("Presenze", 30)
    gol = row.get("Gol", 0)
    assist = row.get("Assist", 0)

    html_code = f"""
    <div class="card-container">
        <div class="card-inner">
            <!-- FRONTE DELLA CARTA -->
            <div class="card-front">
                <div class="holographic-badge">⭐ TOP ELITE</div>
                <div class="player-header">
                    <div class="player-name">{nome}</div>
                    <div class="player-meta">{ruolo} &bull; {squadra}</div>
                </div>
                <div class="player-quotation">
                    {quotazione} cr <span style="font-size:12px; color:#a0aec0;">(Cons: {prezzo_consigliato}cr)</span>
                </div>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Fanta Media</div>
                        <div class="stat-value">{f_media:.2f}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Presenze</div>
                        <div class="stat-value">{giornate}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Gol</div>
                        <div class="stat-value">{gol}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Assist</div>
                        <div class="stat-value">{assist}</div>
                    </div>
                </div>
                <div style="margin-top: 25px; font-size:11px; color: #a0aec0;">Passa il mouse per girare la carta 🔄</div>
            </div>
            <!-- RETRO DELLA CARTA -->
            <div class="card-back">
                <h3 style="margin-top:0; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 8px; font-size: 16px;">Analisi Avanzata</h3>
                <p style="font-size: 12px; color: #cbd5e0; line-height: 1.4;">
                    <b>Indice di appetibilità:</b> Elevato. Giocatore chiave per la vittoria della lega grazie alla titolarità costante e ai bonus pesanti.
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; margin-top: 15px;">
                    <div style="font-size: 11px; color: #00ffcc; font-weight: bold;">Consiglio d'asta:</div>
                    <div style="font-size: 12px;">Non superare il 18% del budget totale per assicurarti questo top player.</div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_code

# Generazione di un Dataset di Esempio (o caricamento dati utente)
st.title("⚽ Gestione Listone Fantacalcio - 3D Showcase")

# Simulazione dati se non presenti
if "df_giocatori" not in st.session_state:
    data = {
        "Nome": ["Lautaro Martínez", "Khvicha Kvaratskhelia", "Matteo Politano", "Nikola Krstović", "Niccolò Barella"],
        "Ruolo": ["A", "A", "C", "A", "C"],
        "Squadra_SerieA": ["Inter", "Napoli", "Napoli", "Lecce", "Inter"],
        "Quotazione": [45, 38, 18, 12, 25],
        "Prezzo_Consigliato": [62, 44, 22, 14, 32],
        "Fanta_Media": [8.45, 7.80, 6.70, 6.40, 6.75],
        "Presenze": [32, 30, 28, 31, 33],
        "Gol": [22, 11, 7, 8, 3],
        "Assist": [6, 9, 6, 2, 5]
    }
    st.session_state["df_giocatori"] = pd.DataFrame(data)

df = st.session_state["df_giocatori"]

st.sidebar.header("Filtri Mercato")
filtro_solo_top = st.sidebar.checkbox("Mostra solo carte interattive (Prezzo > 40cr)", value=False)

st.subheader("Elenco Giocatori & Anteprima Carte 3D")

# Layout a griglia per le carte
cols_per_row = 3
cols = st.columns(cols_per_row)

card_count = 0
for idx, row in df.iterrows():
    prezzo_consigliato = row.get("Prezzo_Consigliato", 0)
    
    if filtro_solo_top and prezzo_consigliato <= 40:
        continue
        
    with cols[card_count % cols_per_row]:
        if prezzo_consigliato > 40:
            # Esecuzione del rendering Flip Card 3D con effetti completi per giocatori > 40cr
            card_html = render_flip_card(row)
            st.markdown(card_html, unsafe_allow_html=True)
        else:
            # Visualizzazione standard per giocatori con prezzo <= 40cr
            st.markdown(f"""
            <div style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 15px; text-align: center; margin: 15px 0; height: 480px; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="color: #333; margin-bottom: 5px;">{row['Nome']}</h4>
                <p style="color: #666; font-size: 13px;">{row['Ruolo']} &bull; {row['Squadra_SerieA']}</p>
                <div style="font-size: 22px; font-weight: bold; color: #3b82f6; margin: 15px 0;">{row['Quotazione']} cr</div>
                <p style="font-size: 12px; color: #888;">Prezzo Consigliato: {prezzo_consigliato} cr</p>
                <span style="background: #e2e8f0; color: #475569; padding: 4px 10px; border-radius: 10px; font-size: 11px; display: inline-block; margin-top: 10px;">Standard Card</span>
            </div>
            """, unsafe_allow_html=True)
            
    card_count += 1
