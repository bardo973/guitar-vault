from datetime import date, timedelta
from PIL import Image
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Guitar Vault Pro",
    page_icon="🎸",
    layout="wide",
)

# ---------------------------------------------------------
# 2. INIZIALIZZAZIONE DATABASE IN MEMORIA
# ---------------------------------------------------------
if "chitarre" not in st.session_state:
  st.session_state.chitarre = [
      {
          "id": "gtr_1",
          "marca": "Fender",
          "modello": "Stratocaster",
          "numero_serie": "US21004589",
          "colore": "3-Color Sunburst",
          "marca_corde": "D'Addario EXL110",
          "scalatura": ".010-.046",
          "accordatura": "E Standard",
          "action": "1.5mm / 1.8mm",
          "relief": "0.20mm",
          "capotasto": "Osso",
          "cfg_pickup": "SSS",
          "modello_pickup": "V-Mod II",
          "altezza_pickup": "2.4mm",
          "push_pull": True,
          "controlli": "Wiring Standard",
          "data_corde": date(2026, 4, 1),  # Corde vecchie per test
          "data_pulizia": date(2026, 4, 1),
          "liuteria": "Schermatura vano",
          "note": "Nessuna",
          "prezzo": 1450.0,
          "valore": 1600.0,
      }
  ]

if "foto_chitarre" not in st.session_state:
  st.session_state.foto_chitarre = {}

# ---------------------------------------------------------
# 3. INTERFACCIA PRINCIPALE
# ---------------------------------------------------------
st.title("🎸 Guitar Vault Pro")
st.caption("Gestione collezione, specifiche e manutenzione")

st.divider()

# --- FILTRI IN ALTO ---
col1, col2 = st.columns([2, 2])

with col1:
  opzioni = ["Tutte le chitarre"] + [
      f"{g['marca']} {g['modello']} ({g['id']})"
      for g in st.session_state.chitarre
  ]
  scelta = st.selectbox("🔍 Seleziona o Cerca uno strumento:", opzioni)

with col2:
  filtro_scadute = st.checkbox(
      "⚠️ Mostra solo chitarre con CAMBIO CORDE necessario (> 60 gg)",
      value=False,
  )

st.divider()

# --- FILTRAGGIO LISTA ---
lista_filtrata = st.session_state.chitarre.copy()

if filtro_scadute:
  soglia = date.today() - timedelta(days=60)
  lista_filtrata = [g for g in lista_filtrata if g["data_corde"] <= soglia]

if scelta != "Tutte le chitarre":
  lista_filtrata = [
      g
      for g in lista_filtrata
      if f"{g['marca']} {g['modello']} ({g['id']})" == scelta
  ]

if not lista_filtrata:
  st.info("Nessuno strumento trovato.")

# --- LISTA CHITARRE ---
for g in lista_filtrata:
  giorni = (date.today() - g["data_corde"]).days
  needs_change = giorni >= 60

  with st.container(border=True):
    col_t, col_b = st.columns([3, 1])

    with col_t:
      st.subheader(f"{g['marca']} {g['modello']}")
      st.caption(f"S/N: {g['numero_serie']} | Colore: {g['colore']}")

      if needs_change:
        st.error(
            f"⚠️ **Corde da cambiare!** Ultimo cambio {giorni} giorni fa ("
            f" {g['data_corde'].strftime('%d/%m/%Y')})"
        )
      else:
        st.success(
            f"✅ Corde OK (Cambiate {giorni} giorni fa -"
            f" {g['data_corde'].strftime('%d/%m/%Y')})"
        )

    with col_b:
      if st.button("🔄 Reset Corde", key=f"reset_{g['id']}"):
        g["data_corde"] = date.today()
        st.toast("Data cambio corde resettata!")
        st.rerun()

      if st.button("🗑️ Elimina", key=f"del_{g['id']}"):
        st.session_state.chitarre = [
            x for x in st.session_state.chitarre if x["id"] != g["id"]
        ]
        st.toast("Strumento eliminato!")
        st.rerun()

    # SCHEDE
    t1, t2, t3, t4, t5 = st.tabs([
        "📷 Foto",
        "🔧 Setup",
        "⚡ Elettronica",
        "🛠️ Manutenzione",
        "💰 Valore",
    ])

    with t1:
      col_img, col_up = st.columns(2)
      with col_img:
        if g["id"] in st.session_state.foto_chitarre:
          st.image(
              st.session_state.foto_chitarre[g["id"]], use_container_width=True
          )
        else:
          st.write("Nessuna foto presente.")
      with col_up:
        up_file = st.file_uploader(
            "Carica foto", type=["jpg", "png"], key=f"up_{g['id']}"
        )
        if up_file:
          st.session_state.foto_chitarre[g["id"]] = Image.open(up_file)
          st.toast("Foto salvata!")
          st.rerun()

    with t2:
      st.write(
          f"**Corde:** {g['marca_corde']} ({g['scalatura']}) | **Accordatura:**"
          f" {g['accordatura']}"
      )
      st.write(
          f"**Action:** {g['action']} | **Relief:** {g['relief']} |"
          f" **Capotasto:** {g['capotasto']}"
      )

    with t3:
      st.write(
          f"**Pickup:** {g['cfg_pickup']} - {g['modello_pickup']} (Altezza:"
          f" {g['altezza_pickup']})"
      )
      st.write(
          f"**Push-Pull:** {'Sì' if g['push_pull'] else 'No'} | **Controlli:**"
          f" {g['controlli']}"
      )

    with t4:
      p_date = (
          g["data_pulizia"].strftime("%d/%m/%Y")
          if g["data_pulizia"]
          else "Non indicata"
      )
      st.write(f"🧹 **Pulizia tastiera:** {p_date}")
      st.write(f"🛠️ **Liuteria:** {g['liuteria']}")
      st.write(f"⚠️ **Note:** {g['note']}")

    with t5:
      c1, c2 = st.columns(2)
      c1.metric("Acquisto", f"€ {g['prezzo']:.2f}")
      c2.metric("Valore Attuale", f"€ {g['valore']:.2f}")

# --- BARRA LATERALE (AGGIUNTA SEMPLIFICATA SENZA LOOP) ---
with st.sidebar:
  st.header("➕ Nuovo Strumento")

  nuova_marca = st.text_input("Marca *", key="add_m")
  nuovo_modello = st.text_input("Modello *", key="add_mod")
  nuovo_sn = st.text_input("Numero di Serie", key="add_sn")
  nuovo_colore = st.text_input("Colore / Finitura", key="add_col")

  if st.button("➕ Aggiungi alla collezione", use_container_width=True):
    if nuova_marca.strip() != "" and nuovo_modello.strip() != "":
      n_id = f"gtr_{len(st.session_state.chitarre) + 100}"
      nuova_g = {
          "id": n_id,
          "marca": nuova_marca.strip(),
          "modello": nuovo_modello.strip(),
          "numero_serie": nuovo_sn.strip(),
          "colore": nuovo_colore.strip(),
          "marca_corde": "D'Addario",
          "scalatura": ".010-.046",
          "accordatura": "E Standard",
          "action": "1.5mm",
          "relief": "0.20mm",
          "capotasto": "Osso",
          "cfg_pickup": "HH",
          "modello_pickup": "Standard",
          "altezza_pickup": "2.0mm",
          "push_pull": False,
          "controlli": "Standard",
          "data_corde": date.today(),
          "data_pulizia": date.today(),
          "liuteria": "Nessuna",
          "note": "",
          "prezzo": 0.0,
          "valore": 0.0,
      }
      st.session_state.chitarre.append(nuova_g)
      st.toast("Chitarra aggiunta con successo!", icon="🎸")
      st.rerun()
    else:
      st.error("Inserisci sia Marca che Modello!")