from datetime import date, timedelta
from typing import Optional
from PIL import Image
from pydantic import BaseModel, Field
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
# 2. MODELLI DI DATI (PYDANTIC)
# ---------------------------------------------------------
class SetupMeccanico(BaseModel):
  scalatura_corde: str = ".010-.046"
  marca_corde: str = "D'Addario EXL110"
  accordatura: str = "E Standard"
  action_mm: str = "1.5mm / 1.8mm"
  relief_manico: str = "0.20mm"
  capotasto: str = "Osso"


class Elettronica(BaseModel):
  configurazione_pickup: str = "HSS"
  modello_pickup: str = "Custom Shop '69 / Shawbucker"
  altezza_pickup: str = "2.4mm / 2.0mm"
  controlli_modifiche: str = "Wiring Standard"
  has_push_pull: bool = False


class Manutenzione(BaseModel):
  data_ultimo_cambio_corde: date = Field(default_factory=date.today)
  data_pulizia_tastiera: Optional[date] = None
  interventi_liuteria: str = "Nessun intervento"
  note_problemi: str = "Nessun problema"


class ValoreEconomico(BaseModel):
  prezzo_acquisto: float = 0.0
  valore_stimato_attuale: float = 0.0


class Chitarra(BaseModel):
  id: str
  marca: str
  modello: str
  numero_serie: str = ""
  colore_finitura: str = ""
  setup: SetupMeccanico = Field(default_factory=SetupMeccanico)
  elettronica: Elettronica = Field(default_factory=Elettronica)
  manutenzione: Manutenzione = Field(default_factory=Manutenzione)
  economia: ValoreEconomico = Field(default_factory=ValoreEconomico)


# ---------------------------------------------------------
# 3. INIZIALIZZAZIONE STATO
# ---------------------------------------------------------
if "chitarre" not in st.session_state:
  demo_gtr1 = Chitarra(
      id="gtr_1",
      marca="Fender",
      modello="American Professional II Stratocaster",
      numero_serie="US21004589",
      colore_finitura="3-Color Sunburst",
      setup=SetupMeccanico(
          scalatura_corde=".010-.046",
          marca_corde="D'Addario EXL110",
          accordatura="E Standard",
      ),
      manutenzione=Manutenzione(
          data_ultimo_cambio_corde=date(2026, 4, 1),
          data_pulizia_tastiera=date(2026, 4, 1),
      ),
  )

  demo_gtr2 = Chitarra(
      id="gtr_2",
      marca="PRS",
      modello="Custom 24",
      numero_serie="1928374",
      colore_finitura="Charcoal Burst",
      setup=SetupMeccanico(
          scalatura_corde=".010-.046",
          marca_corde="PRS Signature",
          accordatura="Drop D",
      ),
      manutenzione=Manutenzione(
          data_ultimo_cambio_corde=date(2026, 7, 10),
      ),
  )
  st.session_state.chitarre = [demo_gtr1, demo_gtr2]

if "foto_chitarre" not in st.session_state:
  st.session_state.foto_chitarre = {}


# ---------------------------------------------------------
# 4. INTERFACCIA UTENTE
# ---------------------------------------------------------
st.title("🎸 Guitar Vault Pro")
st.caption("Gestione avanzata collezione, specifiche e manutenzione")

st.divider()

# --- MENU A TENDINA E FILTRI IN ALTO ---
col_menu1, col_menu2 = st.columns([2, 2])

with col_menu1:
  opzioni_selezione = ["Tutte le chitarre"] + [
      f"{g.marca} {g.modello} ({g.id})" for g in st.session_state.chitarre
  ]
  chitarra_selezionata_str = st.selectbox(
      "🔍 Seleziona o Cerca uno strumento:", opzioni_selezione
  )

with col_menu2:
  filtro_corde_scadute = st.checkbox(
      "⚠️ Mostra solo chitarre che necessitano CAMBIO CORDE (> 60 giorni)",
      value=False,
  )

st.divider()

# --- FILTRAGGIO DELLA LISTA ---
chitarre_da_mostrare = st.session_state.chitarre.copy()

if filtro_corde_scadute:
  soglia_giorni = date.today() - timedelta(days=60)
  chitarre_da_mostrare = [
      g
      for g in chitarre_da_mostrare
      if g.manutenzione.data_ultimo_cambio_corde <= soglia_giorni
  ]

if chitarra_selezionata_str != "Tutte le chitarre":
  chitarre_da_mostrare = [
      g
      for g in chitarre_da_mostrare
      if f"{g.marca} {g.modello} ({g.id})" == chitarra_selezionata_str
  ]

# --- VISUALIZZAZIONE RISULTATI ---
if not chitarre_da_mostrare:
  if filtro_corde_scadute:
    st.success(
        "🎉 Tutte le chitarre hanno corde recenti! Nessun cambio necessario."
    )
  else:
    st.info("Nessuna chitarra trovata nella collezione.")

for idx, chitarra in enumerate(chitarre_da_mostrare):
  giorni_da_cambio = (
      date.today() - chitarra.manutenzione.data_ultimo_cambio_corde
  ).days
  necessita_cambio = giorni_da_cambio >= 60

  with st.container(border=True):
    col_titolo, col_azioni = st.columns([3, 1])

    with col_titolo:
      st.subheader(f"{chitarra.marca} {chitarra.modello}")
      dettagli = []
      if chitarra.numero_serie:
        dettagli.append(f"S/N: {chitarra.numero_serie}")
      if chitarra.colore_finitura:
        dettagli.append(f"Colore: {chitarra.colore_finitura}")
      if dettagli:
        st.caption(" | ".join(dettagli))

      if necessita_cambio:
        st.error(
            f"⚠️ **ATTENZIONE: Corde da cambiare!** Ultimo cambio"
            f" {giorni_da_cambio} giorni fa ("
            f" {chitarra.manutenzione.data_ultimo_cambio_corde.strftime('%d/%m/%Y')})"
        )
      else:
        st.success(
            f"✅ Corde OK (Cambiate {giorni_da_cambio} giorni fa -"
            f" {chitarra.manutenzione.data_ultimo_cambio_corde.strftime('%d/%m/%Y')})"
        )

    with col_azioni:
      st.write("")
      if st.button("🔄 Reset Corde Oggi", key=f"reset_btn_{chitarra.id}"):
        chitarra.manutenzione.data_ultimo_cambio_corde = date.today()
        st.toast("Data cambio corde aggiornata ad oggi!", icon="✅")
        st.rerun()

      if st.button("🗑️ Elimina Strumento", key=f"del_btn_{chitarra.id}"):
        st.session_state.chitarre = [
            g for g in st.session_state.chitarre if g.id != chitarra.id
        ]
        if chitarra.id in st.session_state.foto_chitarre:
          del st.session_state.foto_chitarre[chitarra.id]
        st.toast(f"{chitarra.marca} {chitarra.modello} eliminata!", icon="🗑️")
        st.rerun()

    # SCHEDE Dettagli + Foto
    t1, t2, t3, t4, t5 = st.tabs([
        "📷 Foto Strumento",
        "🔧 Setup & Meccanica",
        "⚡ Elettronica",
        "🛠️ Manutenzione",
        "💰 Valore",
    ])

    with t1:
      col_img_show, col_img_up = st.columns([2, 2])
      with col_img_show:
        if chitarra.id in st.session_state.foto_chitarre:
          st.image(
              st.session_state.foto_chitarre[chitarra.id],
              caption=f"{chitarra.marca} {chitarra.modello}",
              use_container_width=True,
          )
        else:
          st.info("📸 Nessuna foto caricata per questo strumento.")

      with col_img_up:
        uploaded_file = st.file_uploader(
            "Carica / Aggiorna foto",
            type=["jpg", "png", "jpeg"],
            key=f"foto_up_{chitarra.id}",
        )
        if uploaded_file is not None:
          img = Image.open(uploaded_file)
          st.session_state.foto_chitarre[chitarra.id] = img
          st.success("Foto salvata!")
          st.rerun()

    with t2:
      c1, c2, c3 = st.columns(3)
      c1.write(f"**Marca corde:** {chitarra.setup.marca_corde}")
      c1.write(f"**Scalatura:** {chitarra.setup.scalatura_corde}")
      c2.write(f"**Accordatura:** {chitarra.setup.accordatura}")
      c2.write(f"**Action:** {chitarra.setup.action_mm}")
      c3.write(f"**Relief:** {chitarra.setup.relief_manico}")
      c3.write(f"**Capotasto:** {chitarra.setup.capotasto}")

    with t3:
      c1, c2 = st.columns(2)
      c1.write(f"**Configurazione:** {chitarra.elettronica.configurazione_pickup}")
      c1.write(f"**Pickup:** {chitarra.elettronica.modello_pickup}")
      c1.write(f"**Altezza:** {chitarra.elettronica.altezza_pickup}")
      c2.write(
          f"**Push-Pull:**"
          f" {'Sì 🔘' if chitarra.elettronica.has_push_pull else 'No ❌'}"
      )
      c2.write(f"**Modifiche:** {chitarra.elettronica.controlli_modifiche}")

    with t4:
      c1, c2 = st.columns(2)
      d_pulizia = (
          chitarra.manutenzione.data_pulizia_tastiera.strftime("%d/%m/%Y")
          if chitarra.manutenzione.data_pulizia_tastiera
          else "Non effettuata"
      )
      c1.write(f"🧹 **Pulizia tastiera:** {d_pulizia}")
      c1.write(f"🛠️ **Liuteria:** {chitarra.manutenzione.interventi_liuteria}")
      c2.write(f"⚠️ **Note / Problemi:** {chitarra.manutenzione.note_problemi}")

    with t5:
      c1, c2 = st.columns(2)
      c1.metric(
          "Prezzo Acquisto", f"€ {chitarra.economia.prezzo_acquisto:.2f}"
      )
      c2.metric(
          "Valore Attuale", f"€ {chitarra.economia.valore_stimato_attuale:.2f}"
      )

    # FORM MODIFICA
    with st.expander("✏️ Modifica Dettagli e Specifiche"):
      with st.form(f"form_edit_{chitarra.id}"):
        st.subheader("Dati Generali")
        e_marca = st.text_input("Marca", value=chitarra.marca)
        e_modello = st.text_input("Modello", value=chitarra.modello)
        e_sn = st.text_input("Numero di Serie", value=chitarra.numero_serie)
        e_colore = st.text_input(
            "Colore / Finitura", value=chitarra.colore_finitura
        )

        st.subheader("Setup")
        es_m_corde = st.text_input(
            "Marca Corde", value=chitarra.setup.marca_corde
        )
        es_scal = st.text_input(
            "Scalatura Corde", value=chitarra.setup.scalatura_corde
        )
        es_acc = st.text_input(
            "Accordatura", value=chitarra.setup.accordatura
        )
        es_act = st.text_input("Action", value=chitarra.setup.action_mm)
        es_rel = st.text_input(
            "Relief Manico", value=chitarra.setup.relief_manico
        )
        es_cap = st.text_input("Capotasto", value=chitarra.setup.capotasto)

        st.subheader("Elettronica")
        ee_cfg = st.text_input(
            "Configurazione Pickup",
            value=chitarra.elettronica.configurazione_pickup,
        )
        ee_mod = st.text_input(
            "Modello Pickup", value=chitarra.elettronica.modello_pickup
        )
        ee_alt = st.text_input(
            "Altezza Pickup", value=chitarra.elettronica.altezza_pickup
        )
        ee_pp = st.checkbox(
            "Push-Pull / Push-Push Presente",
            value=chitarra.elettronica.has_push_pull,
        )
        ee_ctrl = st.text_area(
            "Controlli & Modifiche",
            value=chitarra.elettronica.controlli_modifiche,
        )

        st.subheader("Manutenzione & Economia")
        em_corde = st.date_input(
            "Data Ultimo Cambio Corde",
            value=chitarra.manutenzione.data_ultimo_cambio_corde,
        )
        em_pul = st.date_input(
            "Data Pulizia Tastiera",
            value=chitarra.manutenzione.data_pulizia_tastiera or date.today(),
        )
        em_liut = st.text_area(
            "Interventi Liuteria",
            value=chitarra.manutenzione.interventi_liuteria,
        )
        em_note = st.text_area(
            "Note & Problemi", value=chitarra.manutenzione.note_problemi
        )

        eco_acq = st.number_input(
            "Prezzo Acquisto (€)",
            value=float(chitarra.economia.prezzo_acquisto),
        )
        eco_val = st.number_input(
            "Valore Attuale (€)",
            value=float(chitarra.economia.valore_stimato_attuale),
        )

        if st.form_submit_button("💾 Salva Tutte le Modifiche"):
          chitarra.marca = e_marca
          chitarra.modello = e_modello
          chitarra.numero_serie = e_sn
          chitarra.colore_finitura = e_colore

          chitarra.setup.marca_corde = es_m_corde
          chitarra.setup.scalatura_corde = es_scal
          chitarra.setup.accordatura = es_acc
          chitarra.setup.action_mm = es_act
          chitarra.setup.relief_manico = es_rel
          chitarra.setup.capotasto = es_cap

          chitarra.elettronica.configurazione_pickup = ee_cfg
          chitarra.elettronica.modello_pickup = ee_mod
          chitarra.elettronica.altezza_pickup = ee_alt
          chitarra.elettronica.has_push_pull = ee_pp
          chitarra.elettronica.controlli_modifiche = ee_ctrl

          chitarra.manutenzione.data_ultimo_cambio_corde = em_corde
          chitarra.manutenzione.data_pulizia_tastiera = em_pul
          chitarra.manutenzione.interventi_liuteria = em_liut
          chitarra.manutenzione.note_problemi = em_note

          chitarra.economia.prezzo_acquisto = eco_acq
          chitarra.economia.valore_stimato_attuale = eco_val

          st.toast("Scheda aggiornata!", icon="✅")
          st.rerun()

# --- SIDEBAR PER NUOVO STRUMENTO (RISOLTO PROBLEMA INVIO) ---
with st.sidebar:
  st.header("➕ Nuovo Strumento")
  with st.form("form_add_guitar", clear_on_submit=True):
    add_m = st.text_input("Marca (obbligatoria)*")
    add_mod = st.text_input("Modello (obbligatorio)*")
    add_sn = st.text_input("Numero di Serie")
    add_col = st.text_input("Colore / Finitura")

    submitted = st.form_submit_button("Aggiungi Strumento")

    if submitted:
      if add_m.strip() != "" and add_mod.strip() != "":
        # Generiamo un ID univoco basato sul numero attuale di chitarre
        nuovo_id = f"gtr_{len(st.session_state.chitarre) + 100}"
        nuova_chitarra = Chitarra(
            id=nuovo_id,
            marca=add_m.strip(),
            modello=add_mod.strip(),
            numero_serie=add_sn.strip(),
            colore_finitura=add_col.strip(),
            setup=SetupMeccanico(),
            elettronica=Elettronica(),
            manutenzione=Manutenzione(),
            economia=ValoreEconomico(),
        )
        st.session_state.chitarre.append(nuova_chitarra)
        st.toast(
            f"Aggiunta {nuova_chitarra.marca} {nuova_chitarra.modello}!",
            icon="🎸",
        )
        st.rerun()
      else:
        st.error("Inserisci sia la **Marca** che il **Modello**!")