from datetime import date
from typing import List, Optional
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
# 2. DEFINIZIONE DEI MODELLI PYDANTIC (Tipi di Dati)
# ---------------------------------------------------------
class SetupMeccanico(BaseModel):
  scalatura_corde: str = ".010-.046"
  marca_corde: str = "D'Addario EXL110"
  accordatura: str = "E Standard"
  action_mm: str = "1.5mm - 2.0mm"
  relief_manico: str = "0.25mm"
  capotasto: str = "Osso"


class Elettronica(BaseModel):
  configurazione_pickup: str = "HSS"
  modello_pickup: str = "Custom Shop '69 / Shawbucker"
  altezza_pickup: str = "2.4mm / 2.0mm"
  controlli_modifiche: str = "Wiring standard"
  has_push_pull: bool = False


class Manutenzione(BaseModel):
  data_ultimo_cambio_corde: date = Field(default_factory=date.today)
  data_pulizia_tastiera: Optional[date] = None
  interventi_liuteria: str = "Nessun intervento recente"
  note_problemi: str = "Nessun problema rilevato"


class ValoreEconomico(BaseModel):
  prezzo_acquisto: Optional[float] = 0.0
  valore_stimato_attuale: Optional[float] = 0.0


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
# 3. INIZIALIZZAZIONE DELLO STATO (Database Locale)
# ---------------------------------------------------------
if "chitarre" not in st.session_state:
  chitarra_demo = Chitarra(
      id="gtr_01",
      marca="Fender",
      modello="Stratocaster",
      numero_serie="US21004589",
      colore_finitura="3-Color Sunburst",
      setup=SetupMeccanico(
          scalatura_corde=".010-.046",
          marca_corde="D'Addario EXL110",
          accordatura="E Standard",
          action_mm="1.5mm / 1.8mm",
          relief_manico="0.20mm",
          capotasto="Osso sintetico",
      ),
      elettronica=Elettronica(
          configurazione_pickup="SSS",
          modello_pickup="V-Mod II Single-Coil",
          altezza_pickup="2.4mm",
          controlli_modifiche="Push-push su secondo tono per attivare pickup manico",
          has_push_pull=True,
      ),
      manutenzione=Manutenzione(
          data_ultimo_cambio_corde=date(2026, 6, 15),
          data_pulizia_tastiera=date(2026, 5, 10),
          interventi_liuteria="Schermatura vano elettronica",
          note_problemi="Piccolo fruscio sul potenziometro del volume",
      ),
      economia=ValoreEconomico(
          prezzo_acquisto=1450.0, valore_stimato_attuale=1600.0
      ),
  )
  st.session_state.chitarre = [chitarra_demo]

if "foto_chitarre" not in st.session_state:
  st.session_state.foto_chitarre = {}


# ---------------------------------------------------------
# 4. INTERFACCIA UTENTE (Streamlit App)
# ---------------------------------------------------------
st.title("🎸 Guitar Vault Pro")
st.caption("Gestore completo collezione, specifiche e manutenzione")

st.divider()

for chitarra in st.session_state.chitarre:
  with st.container(border=True):
    col_titolo, col_reset = st.columns([3, 1])

    with col_titolo:
      st.subheader(f"{chitarra.marca} {chitarra.modello}")
      sub_info = []
      if chitarra.numero_serie:
        sub_info.append(f"S/N: {chitarra.numero_serie}")
      if chitarra.colore_finitura:
        sub_info.append(f"Colore: {chitarra.colore_finitura}")
      if sub_info:
        st.caption(" | ".join(sub_info))

    with col_reset:
      st.write("")
      if st.button("🔄 Reset Corde", key=f"reset_{chitarra.id}"):
        chitarra.manutenzione.data_ultimo_cambio_corde = date.today()
        st.toast("Data cambio corde aggiornata ad oggi!", icon="✅")
        st.rerun()

    # Mostra la foto se presente
    if chitarra.id in st.session_state.foto_chitarre:
      st.image(
          st.session_state.foto_chitarre[chitarra.id],
          caption=f"{chitarra.marca} {chitarra.modello}",
          use_container_width=True,
      )

    # SCHEDE INFORMATIVE
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔧 Setup & Meccanica",
        "⚡ Elettronica",
        "🛠️ Manutenzione",
        "💰 Valore",
        "📷 Foto",
    ])

    with tab1:
      c1, c2, c3 = st.columns(3)
      c1.write(f"**Marca corde:** {chitarra.setup.marca_corde}")
      c1.write(f"**Scalatura:** {chitarra.setup.scalatura_corde}")
      c2.write(f"**Accordatura:** {chitarra.setup.accordatura}")
      c2.write(f"**Action:** {chitarra.setup.action_mm}")
      c3.write(f"**Relief Manico:** {chitarra.setup.relief_manico}")
      c3.write(f"**Capotasto:** {chitarra.setup.capotasto}")

    with tab2:
      c1, c2 = st.columns(2)
      c1.write(f"**Configurazione:** {chitarra.elettronica.configurazione_pickup}")
      c1.write(f"**Modello Pickup:** {chitarra.elettronica.modello_pickup}")
      c1.write(f"**Altezza Pickup:** {chitarra.elettronica.altezza_pickup}")
      c2.write(
          f"**Push-Pull / Push-Push:**"
          f" {'Sì 🔘' if chitarra.elettronica.has_push_pull else 'No ❌'}"
      )
      c2.write(
          f"**Controlli / Modifiche:** {chitarra.elettronica.controlli_modifiche}"
      )

    with tab3:
      c1, c2 = st.columns(2)
      data_corde = chitarra.manutenzione.data_ultimo_cambio_corde.strftime(
          "%d/%m/%Y"
      )
      data_pulizia = (
          chitarra.manutenzione.data_pulizia_tastiera.strftime("%d/%m/%Y")
          if chitarra.manutenzione.data_pulizia_tastiera
          else "Non registrata"
      )
      c1.info(f"📅 **Ultimo cambio corde:** {data_corde}")
      c1.write(f"🧹 **Pulizia/Nutrizione tastiera:** {data_pulizia}")
      c2.write(
          f"🛠️ **Interventi liuteria:** {chitarra.manutenzione.interventi_liuteria}"
      )
      c2.write(f"⚠️ **Note / Problemi:** {chitarra.manutenzione.note_problemi}")

    with tab4:
      c1, c2 = st.columns(2)
      c1.metric(
          label="Prezzo di Acquisto",
          value=f"€ {chitarra.economia.prezzo_acquisto:.2f}",
      )
      c2.metric(
          label="Valore Stimato Attuale",
          value=f"€ {chitarra.economia.valore_stimato_attuale:.2f}",
      )

    with tab5:
      uploaded_file = st.file_uploader(
          "Carica o aggiorna la foto dello strumento",
          type=["jpg", "jpeg", "png"],
          key=f"uploader_{chitarra.id}",
      )
      if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.foto_chitarre[chitarra.id] = image
        st.success("Foto caricata con successo!")
        st.rerun()

    # FORM PER LA MODIFICA
    with st.expander("✏️ Modifica Scheda Completa"):
      with st.form(f"form_edit_{chitarra.id}"):
        st.subheader("Dati Generali")
        m_marca = st.text_input("Marca", value=chitarra.marca)
        m_modello = st.text_input("Modello", value=chitarra.modello)
        m_sn = st.text_input("Numero di Serie", value=chitarra.numero_serie)
        m_colore = st.text_input(
            "Colore / Finitura", value=chitarra.colore_finitura
        )

        st.subheader("Setup & Meccanica")
        ms_marca_corde = st.text_input(
            "Marca Corde", value=chitarra.setup.marca_corde
        )
        ms_scalatura = st.text_input(
            "Scalatura Corde", value=chitarra.setup.scalatura_corde
        )
        ms_accordatura = st.selectbox(
            "Accordatura",
            ["E Standard", "Drop D", "Eb Standard", "Drop C", "Altro"],
            index=[
                "E Standard",
                "Drop D",
                "Eb Standard",
                "Drop C",
                "Altro",
            ].index(chitarra.setup.accordatura)
            if chitarra.setup.accordatura
            in ["E Standard", "Drop D", "Eb Standard", "Drop C", "Altro"]
            else 0,
        )
        ms_action = st.text_input("Action", value=chitarra.setup.action_mm)
        ms_relief = st.text_input(
            "Relief Manico", value=chitarra.setup.relief_manico
        )
        ms_capotasto = st.text_input(
            "Capotasto", value=chitarra.setup.capotasto
        )

        st.subheader("Elettronica")
        me_config = st.text_input(
            "Configurazione Pickup (es. HSS, SSS, HH)",
            value=chitarra.elettronica.configurazione_pickup,
        )
        me_modello = st.text_input(
            "Modello Pickup", value=chitarra.elettronica.modello_pickup
        )
        me_altezza = st.text_input(
            "Altezza Pickup", value=chitarra.elettronica.altezza_pickup
        )
        me_pushpull = st.checkbox(
            "Presente Push-Pull / Push-Push",
            value=chitarra.elettronica.has_push_pull,
        )
        me_controlli = st.text_area(
            "Controlli e Modifiche",
            value=chitarra.elettronica.controlli_modifiche,
        )

        st.subheader("Manutenzione & Registro")
        mm_pulizia = st.date_input(
            "Data Ultima Pulizia/Nutrizione Tastiera",
            value=chitarra.manutenzione.data_pulizia_tastiera
            or date.today(),
        )
        mm_liuteria = st.text_area(
            "Interventi di Liuteria",
            value=chitarra.manutenzione.interventi_liuteria,
        )
        mm_note = st.text_area(
            "Note & Problemi", value=chitarra.manutenzione.note_problemi
        )

        st.subheader("Economia")
        m_prezzo = st.number_input(
            "Prezzo di Acquisto (€)",
            value=float(chitarra.economia.prezzo_acquisto or 0.0),
        )
        m_valore = st.number_input(
            "Valore Stimato Attuale (€)",
            value=float(chitarra.economia.valore_stimato_attuale or 0.0),
        )

        if st.form_submit_button("💾 Salva Tutte le Modifiche"):
          chitarra.marca = m_marca
          chitarra.modello = m_modello
          chitarra.numero_serie = m_sn
          chitarra.colore_finitura = m_colore

          chitarra.setup.marca_corde = ms_marca_corde
          chitarra.setup.scalatura_corde = ms_scalatura
          chitarra.setup.accordatura = ms_accordatura
          chitarra.setup.action_mm = ms_action
          chitarra.setup.relief_manico = ms_relief
          chitarra.setup.capotasto = ms_capotasto

          chitarra.elettronica.configurazione_pickup = me_config
          chitarra.elettronica.modello_pickup = me_modello
          chitarra.elettronica.altezza_pickup = me_altezza
          chitarra.elettronica.has_push_pull = me_pushpull
          chitarra.elettronica.controlli_modifiche = me_controlli

          chitarra.manutenzione.data_pulizia_tastiera = mm_pulizia
          chitarra.manutenzione.interventi_liuteria = mm_liuteria
          chitarra.manutenzione.note_problemi = mm_note

          chitarra.economia.prezzo_acquisto = m_prezzo
          chitarra.economia.valore_stimato_attuale = m_valore

          st.toast("Scheda aggiornata con successo!", icon="✅")
          st.rerun()

# SIDEBAR PER AGGIUNGERE NUOVE CHITARRE
with st.sidebar:
  st.header("➕ Aggiungi Strumento")
  with st.form("form_add_guitar"):
    add_marca = st.text_input("Marca *")
    add_modello = st.text_input("Modello *")
    add_sn = st.text_input("Numero di Serie")
    add_colore = st.text_input("Colore / Finitura")

    if st.form_submit_button("Aggiungi alla Collezione"):
      if add_marca and add_modello:
        nuova = Chitarra(
            id=f"gtr_{len(st.session_state.chitarre) + 1}",
            marca=add_marca,
            modello=add_modello,
            numero_serie=add_sn,
            colore_finitura=add_colore,
        )
        st.session_state.chitarre.append(nuova)
        st.toast("Nuova chitarra aggiunta alla collezione!", icon="🎸")
        st.rerun()
      else:
        st.error("Inserisci almeno Marca e Modello!")