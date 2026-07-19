import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Configurazione database e directory per l'archiviazione delle immagini
DB_NAME = "collezione_chitarre.db"
IMG_DIR = "foto_chitarre"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def init_db():
    """Inizializza il database e applica le migrazioni necessarie per supportare le nuove funzionalità."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Abilita le chiavi esterne per la cancellazione a cascata dello storico
    c.execute("PRAGMA foreign_keys = ON")
    
    # Tabella principale chitarre
    c.execute('''
        CREATE TABLE IF NOT EXISTS chitarre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modello TEXT,
            serie TEXT,
            corde TEXT,
            data_cambio TEXT,
            prossimo_cambio TEXT,
            foto_path TEXT
        )
    ''')
    
    # Nuova tabella per lo storico delle manutenzioni
    c.execute('''
        CREATE TABLE IF NOT EXISTS storico_manutenzioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chitarra_id INTEGER,
            data_evento TEXT,
            tipo_evento TEXT,
            note_evento TEXT,
            FOREIGN KEY (chitarra_id) REFERENCES chitarre (id) ON DELETE CASCADE
        )
    ''')
    
    # Migrazione dinamica: verifica ed inserisce le colonne aggiunte nei vari aggiornamenti
    c.execute("PRAGMA table_info(chitarre)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'frequenza_mesi' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN frequenza_mesi INTEGER DEFAULT 3")
    if 'accordatura' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN accordatura TEXT DEFAULT 'E Standard'")
    if 'note_setup' not in columns:
        c.execute("ALTER TABLE chitarre ADD COLUMN note_setup TEXT DEFAULT ''")
        
    conn.commit()
    conn.close()