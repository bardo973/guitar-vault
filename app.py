from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Guitar Vault",
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
# 3. STATO INIZIALE (DATABASE IN MEMORIA)
# ---------------------------------------------------------
if "chitarre" not in st.session_state:
  demo_gtr = Chitarra(
      id="gtr_1",
      marca="Fender",
      modello="American Professional II Stratocaster",
      numero_serie="US21004589",
      colore_finitura="3-Color Sunburst",
      setup=SetupMeccanico(
          scalatura_corde=".010-.046",
          marca_corde="D'Addario EXL110",
          accordatura="E Standard",
          action_mm="1.5mm / 1.8mm",
          relief_manico="0.20mm",
          capotasto="Osso",
      ),
      elettronica=Elettronica(
          configurazione_pickup="SSS",
          modello_pickup="V-Mod II Single-Coil",
          altezza_pickup="2.4mm",
          controlli_modifiche="Push-push su secondo tono",
          has_push_pull=True,
      ),
      manutenzione=Manutenzione(
          data_ultimo_cambio_corde=date(2026, 6, 15),
          data_pulizia_tastiera=date(2026, 5, 10),
          interventi_liuteria="Schermatura vano elettronica",
          note_problemi="Nessuno",
      ),
      economia=ValoreEconomico(
          prezzo_acquisto=1450.0, valore_stimato_attuale=1600.0
      ),
  )
  st.session_state.chitarre = [demo_gtr]


# ---------------------------------------------------------
# 4. INTERFACCIA STREAMLIT
# ---------------------------------------------------------
st.title("🎸 Guitar Vault")
st.caption("Gestione completa collezione, specifiche e manutenzione")

st.divider()

if not st.session_state.chitarre:
  st.info("La tua collezione è vuota. Aggiungi uno strumento dalla barra laterale!")

# Ciclo per mostrare e gestire ciascuna chitarra
for idx, chitarra in enumerate(st.session_state.chitarre):
  with st.container(border=True):
    col_info, col_azioni = st.columns([3, 1])

    with col_info:
      st.subheader(f"{chitarra.marca} {chitarra.modello}")
      dettagli = []
      if chitarra.numero_serie:
        dettagli.append(f"S/N: {chitarra.numero_serie}")
      if chitarra.colore_finitura:
        dettagli.append(f"Colore: {chitarra.colore_finitura}")
      if dettagli:
        st.caption(" | ".join(dettagli))

    with col_azioni:
      st.write("")
      # PULSANTE PER ELIMINARE LO STRUMENTO
      if st.button("🗑️ Elimina", key=f"del_{chitarra.id}_{idx}"):
        st.session_state.chitarre.pop(idx)
        st.toast(
            f"Strumento {chitarra.marca} {chitarra.modello} rimosso!", icon="🗑️"
        )
        st.rerun()

    # SCHEDE RIEPILOGATIVE
    t1, t2, t3, t4 = st.tabs([
        "🔧 Setup & Meccanica",
        "⚡ Elettronica",
        "🛠️ Manutenzione",
        "💰 Valore",
    ])

    with t1:
      c1, c2, c3 = st.columns(3)
      c1.write(f"**Corde:** {chitarra.setup.marca_corde}")
      c1.write(f"**Scalatura:** {chitarra.setup.scalatura_corde}")
      c2.write(f"**Accordatura:** {chitarra.setup.accordatura}")
      c2.write(f"**Action:** {chitarra.setup.action_mm}")
      c3.write(f"**Relief:** {chitarra.setup.relief_manico}")
      c3.write(f"**Capotasto:** {chitarra.setup.capotasto}")

    with t2:
      c1, c2 = st.columns(2)
      c1.write(f"**Configurazione:** {chitarra.elettronica.configurazione_pickup}")
      c1.write(f"**Pickup:** {chitarra.elettronica.modello_pickup}")
      c1.write(f"**Altezza Pickup:** {chitarra.elettronica.altezza_pickup}")
      c2.write(
          f"**Push-Pull:**"
          f" {'Sì 🔘' if chitarra.elettronica.has_push_pull else 'No ❌'}"
      )
      c2.write(f"**Modifiche:** {chitarra.elettronica.controlli_modifiche}")

    with t3:
      c1, c2 = st.columns(2)
      d_corde = chitarra.manutenzione.data_ultimo_cambio_corde.strftime(
          "%d/%m/%Y"
      )
      d_pulizia = (
          chitarra.manutenzione.data_pulizia_tastiera.strftime("%d/%m/%Y")
          if chitarra.manutenzione.data_pulizia_tastiera
          else "Non indicata"
      )
      c1.info(f"📅 **Ultimo cambio corde:** {d_corde}")
      c1.write(f"🧹 **Pulizia tastiera:** {d_pulizia}")
      c2.write(f"🛠️ **Liuteria:** {chitarra.manutenzione.interventi_liuteria}")
      c2.write(f"⚠️ **Note:** {chitarra.manutenzione.note_problemi}")

    with t4:
      c1, c2 = st.columns(2)
      c1.metric(
          "Prezzo Acquisto", f"€ {chitarra.economia.prezzo_acquisto:.2f}"
      )
      c2.metric(
          "Valore Attuale", f"€ {chitarra.economia.valore_stimato_attuale:.2f}"
      )

    # SEZIONE DI MODIFICA
    with st.expander("✏️ Modifica Valori e Scheda"):
      with st.form(f"form_edit_{chitarra.id}_{idx}"):
        st.subheader("Generalità")
        e_marca = st.text_input("Marca", value=chitarra.marca)
        e_modello = st.text_input("Modello", value=chitarra.modello)
        e_sn = st.text_input("Numero di Serie", value=chitarra.numero_serie)
        e_colore = st.text_input(
            "Colore/Finitura", value=chitarra.colore_finitura
        )

        st.subheader("Setup")
        es_marca = st.text_input(
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

        st.subheader("Manutenzione & Valore")
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

        if st.form_submit_button("💾 Salva Modifiche"):
          chitarra.marca = e_marca
          chitarra.modello = e_modello
          chitarra.numero_serie = e_sn
          chitarra.colore_finitura = e_colore

          chitarra.setup.marca_corde = es_marca
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

          st.toast("Modifiche salvate con successo!", icon="✅")
          st.rerun()

# BARRA LATERALE PER NUOVI INSERIMENTI
with st.sidebar:
  st.header("➕ Nuovo Strumento")
  with st.form("form_add"):
    add_m = st.text_input("Marca *")
    add_mod = st.text_input("Modello *")
    add_sn = st.text_input("Numero di Serie")
    add_col = st.text_input("Colore / Finitura")

    if st.form_submit_button("Aggiungi"):
      if add_m and add_mod:
        n_id = f"gtr_{len(st.session_state.chitarre) + 1}"
        nuova = Chitarra(
            id=n_id,
            marca=add_m,
            modello=add_mod,
            numero_serie=add_sn,
            colore_finitura=add_col,
        )
        st.session_state.chitarre.append(nuova)
        st.toast("Nuova chitarra aggiunta!", icon="🎸")
        st.rerun()
      else:
        st.error("Marca e Modello sono obbligatori!")