from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Guitar Vault", page_icon="🎸", layout="centered")


# ---------------------------------------------------------
# 2. DEFINIZIONE DEI MODELLI PYDANTIC (Tipi di Dati)
# ---------------------------------------------------------
class SetupMeccanico(BaseModel):
  scalatura_corde: str = ".010-.046"
  marca_corde: str = "D'Addario EXL110"
  data_ultimo_cambio: date = Field(default_factory=date.today)


class Chitarra(BaseModel):
  id: str
  marca: str
  modello: str
  anno: Optional[int] = None
  setup: SetupMeccanico


# ---------------------------------------------------------
# 3. INIZIALIZZAZIONE DELLO STATO (Database Locale)
# ---------------------------------------------------------
if "chitarre" not in st.session_state:
  # Creiamo una prima chitarra di prova usando la classe definita sopra
  chitarra_demo = Chitarra(
      id="gtr_01",
      marca="Fender",
      modello="Stratocaster",
      anno=2021,
      setup=SetupMeccanico(
          scalatura_corde=".010-.046",
          marca_corde="D'Addario EXL110",
          data_ultimo_cambio=date(2026, 6, 1),
      ),
  )
  st.session_state.chitarre = [chitarra_demo]


# ---------------------------------------------------------
# 4. INTERFACCIA UTENTE (Streamlit App)
# ---------------------------------------------------------
st.title("🎸 Guitar Vault")
st.caption("Gestione collezione, setup & manutenzione strumenti")

st.divider()

# Ciclo di visualizzazione delle chitarre nel database
for idx, chitarra in enumerate(st.session_state.chitarre):
  with st.container(border=True):
    col1, col2 = st.columns([3, 1])

    # Colonna Sinistra: Dettagli della Chitarra
    with col1:
      st.subheader(f"{chitarra.marca} {chitarra.modello}")
      if chitarra.anno:
        st.caption(f"Anno di produzione: {chitarra.anno}")

      st.write(
          f"**Corde montate:** {chitarra.setup.marca_corde} ("
          f" {chitarra.setup.scalatura_corde})"
      )
      st.info(
          f"📅 Ultimo cambio corde:"
          f" **{chitarra.setup.data_ultimo_cambio.strftime('%d/%m/%Y')}**"
      )

    # Colonna Destra: Tasto Reset Rapido
    with col2:
      st.write("")  # Spaziatore visivo
      if st.button("🔄 Reset Corde", key=f"reset_{chitarra.id}"):
        chitarra.setup.data_ultimo_cambio = date.today()
        st.toast("Corde resettate alla data di oggi!", icon="✅")
        st.rerun()

    # Sezione Espandibile: Modifica Dati
    with st.expander("✏️ Modifica Dettagli & Setup"):
      nuova_marca = st.text_input(
          "Marca Corde",
          value=chitarra.setup.marca_corde,
          key=f"marca_{chitarra.id}",
      )
      nuova_scalatura = st.text_input(
          "Scalatura Corde",
          value=chitarra.setup.scalatura_corde,
          key=f"scal_{chitarra.id}",
      )

      if st.button("💾 Salva Modifiche", key=f"save_{chitarra.id}"):
        chitarra.setup.marca_corde = nuova_marca
        chitarra.setup.scalatura_corde = nuova_scalatura
        st.success("Informazioni aggiornate con successo!")
        st.rerun()

st.divider()

# Form rapido per aggiungere una nuova chitarra
with st.sidebar:
  st.header("➕ Aggiungi Chitarra")
  nuova_marca_gtr = st.text_input("Marca (es. Gibson)")
  nuovo_modello_gtr = st.text_input("Modello (es. Les Paul)")
  nuovo_anno_gtr = st.number_input(
      "Anno", min_value=1950, max_value=2026, value=2024
  )

  if st.button("Aggiungi alla Collezione"):
    if nuova_marca_gtr and nuovo_modello_gtr:
      nuova_g = Chitarra(
          id=f"gtr_{len(st.session_state.chitarre) + 1}",
          marca=nuova_marca_gtr,
          modello=nuovo_modello_gtr,
          anno=nuovo_anno_gtr,
          setup=SetupMeccanico(),
      )
      st.session_state.chitarre.append(nuova_g)
      st.toast("Nuova chitarra aggiunta!", icon="🎸")
      st.rerun()
    else:
      st.error("Inserisci sia la marca che il modello!")