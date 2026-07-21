# Creazione di un'istanza e serializzazione in JSON
chitarra_data = {
    "id": "gtr_01",
    "generale": {
        "marca": "Fender",
        "modello": "Stratocaster",
        "anno_produzione": 2021,
        "numero_serie": "US210001",
    },
    "setup_meccanico": {
        "scalatura_corde": ".010-.046",
        "marca_corde": "D'Addario",
        "accordatura": "E Standard",
        "azione_mm": {"mi_alto": 1.5, "mi_basso": 2.0},
    },
    "elettronica": {
        "configurazione": "SSS",
        "pickups": {"manico": "Custom 69", "ponte": "Custom 69"},
    },
}

chitarra = Chitarra(**chitarra_data)

# Esporta in JSON pronto per essere salvato o inviato
print(chitarra.model_dump_json(indent=2))