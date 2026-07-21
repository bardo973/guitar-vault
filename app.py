from datetime import date
from pydantic import BaseModel
import streamlit as st

# Impostazione pagina
st.set_page_config(page_title="Guitar Vault", page_icon="🎸")


# Modello Pydantic
class Chitarra(BaseModel):
  marca: str
  modello: str
  data_cambio_corde: date


# Titolo nell'app
st.title("🎸 Guitar Vault")
st.write("La tua collezione di chitarre è online!")

# Creazione di un oggetto di prova
chitarra_demo = Chitarra(
    marca="Fender",
    modello="Stratocaster",
    data_cambio_corde=date(2026, 7, 21),
)

# Mostra i dati a schermo
st.subheader(f"{chitarra_demo.marca} {chitarra_demo.modello}")
st.info(f"Ultimo cambio corde: {chitarra_demo.data_cambio_corde}")

if st.button("🔄 Reset Cambio Corde"):
  chitarra_demo.data_cambio_corde = date.today()
  st.success("Corde resettate ad oggi!")