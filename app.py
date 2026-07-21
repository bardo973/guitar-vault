from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class AzioneA12Tasto(BaseModel):
    mi_alto: float = Field(..., description="Altezza corda Mi alto al 12° tasto in mm")
    mi_basso: float = Field(..., description="Altezza corda Mi basso al 12° tasto in mm")


class SetupMeccanico(BaseModel):
    scalatura_corde: str = Field(..., example=".010-.046")
    marca_corde: str
    accordatura: str = Field("E Standard", example="E Standard")
    azione_mm: AzioneA12Tasto
    relief_manico_mm: Optional[float] = None
    materiale_capotasto: Optional[str] = None
    note_setup: Optional[str] = None


class AltezzaPickups(BaseModel):
    manico: Optional[float] = None
    centrale: Optional[float] = None
    ponte: Optional[float] = None


class Elettronica(BaseModel):
    configurazione: str = Field(..., example="HSS")
    pickups: dict[str, str]  # es. {"manico": "V-Mod II", "ponte": "Shawbucker"}
    altezza_pickups_mm: Optional[AltezzaPickups] = None
    modifiche_elettronica: Optional[str] = None


class InterventoManutenzione(BaseModel):
    id_intervento: str
    data: date
    tipo: str = Field(..., example="Cambio Corde")
    descrizione: Optional[str] = None
    costo: Optional[float] = 0.0


class Generale(BaseModel):
    marca: str
    modello: str
    anno_produzione: Optional[int] = None
    numero_serie: Optional[str] = None
    colore_finitura: Optional[str] = None
    foto: List[str] = []


class ValoreDocumenti(BaseModel):
    data_acquisto: Optional[date] = None
    prezzo_acquisto: Optional[float] = None
    valore_stimato_attuale: Optional[float] = None
    documenti_allegati: List[str] = []


class Chitarra(BaseModel):
    id: str
    generale: Generale
    setup_meccanico: SetupMeccanico
    elettronica: Elettronica
    registro_manutenzione: List[InterventoManutenzione] = []
    valore_documenti: Optional[ValoreDocumenti] = None