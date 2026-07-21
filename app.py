import json

# DATABASE INIZIALE DELLA COLLEZIONE
guitars = [
    {
        "id": "gtr-001",
        "brand": "Fender",
        "model": "American Professional II Stratocaster",
        "year": 2021,
        "serial_number": "US210984",
        "string_gauge": "0.010 - 0.046",
        "last_setup": "2026-05-10",
        "notes": "Action bassa, accordatura Standard E"
    },
    {
        "id": "gtr-002",
        "brand": "PRS",
        "model": "Custom 24",
        "year": 2019,
        "serial_number": "19 28374",
        "string_gauge": "0.010 - 0.046",
        "last_setup": "2026-06-02",
        "notes": "Top Flame 10-Top"
    },
    {
        "id": "gtr-003",
        "brand": "Gibson",
        "model": "Les Paul Standard '60s",
        "year": 2022,
        "serial_number": "22091004",
        "string_gauge": "0.010 - 0.052",
        "last_setup": "2026-04-15",
        "notes": "Finitura Bourbon Burst"
    }
]

def show_collection(guitar_list):
    """Mostra la lista aggiornata di tutte le chitarre."""
    print("\n==========================================")
    print("         COLLEZIONE CHITARRE")
    print("==========================================")
    if not guitar_list:
        print("La collezione è vuota.")
        return
    for g in guitar_list:
        print(f"[{g['id']}] {g['brand']} {g['model']} ({g['year']})")
        print(f"       Corde: {g['string_gauge']} | Setup: {g['last_setup']}")
        print(f"       Note: {g['notes']}")
        print("-" * 42)

def update_guitar(guitar_list, guitar_id, **kwargs):
    """Modifica i valori di una chitarra esistente."""
    found = False
    for guitar in guitar_list:
        if guitar["id"] == guitar_id:
            found = True
            for key, value in kwargs.items():
                if key in guitar:
                    guitar[key] = value
                    print(f"✓ Aggiornato '{key}' -> '{value}' per [{guitar_id}]")
            break
    if not found:
        print(f"✗ Nessuno strumento trovato con ID: {guitar_id}")

def delete_guitar(guitar_list, guitar_id):
    """Cancella uno strumento tramite ID."""
    initial_count = len(guitar_list)
    updated_list = [g for g in guitar_list if g["id"] != guitar_id]
    
    if len(updated_list) < initial_count:
        print(f"✓ Strumento [{guitar_id}] eliminato con successo.")
    else:
        print(f"✗ Nessuno strumento trovato con ID: {guitar_id}")
        
    return updated_list


# --- ESECUZIONE ---

# 1. Mostra situazione iniziale
show_collection(guitars)

print("\n--- APPLICO MODIFICHE E CANCELLAZIONE ---")

# 2. Modifica la Fender
update_guitar(
    guitars, 
    "gtr-001", 
    last_setup="2026-07-21", 
    string_gauge="0.009 - 0.042",
    notes="Cambio scalatura a 09-42"
)

# 3. Cancella la Gibson
guitars = delete_guitar(guitars, "gtr-003")

# 4. Mostra situazione finale
show_collection(guitars)

# MANTIENE IL TERMINALE APERTO
input("\nPremi INVIO sulla tastiera per chiudere...")