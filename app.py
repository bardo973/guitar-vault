import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Guitar Rack & Vault",
    page_icon="🎸",
    layout="wide"
)

html_code = r"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Guitar Rack & Vault</title>
  <style>
    :root {
      --ff-sans: 'Google Sans Flex', 'Google Sans Text', 'Google Sans', system-ui, -apple-system, sans-serif;
      --ff-mono: 'Google Sans Code', 'Google Sans Mono', monospace;
      --fw-normal: 400;
      --fw-medium: 500;
      --fw-semibold: 600;

      --body-bg: #0f172a;
      --primary: #3b82f6;
      --on-primary: #ffffff;
      --primary-container: #1e3a8a;
      --surface: rgba(15, 23, 42, 0.88);
      --surface-container: rgba(30, 41, 59, 0.75);
      --surface-container-high: rgba(51, 65, 85, 0.85);
      --surface-container-highest: rgba(71, 85, 105, 0.9);
      --on-surface-default: #f8fafc;
      --on-surface-de-emphasis: #cbd5e1;
      --outline: #94a3b8;
      --outline-variant: #475569;
      --stroke-default: rgba(255, 255, 255, 0.18);
      --negative: #ef4444;
      --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }

    body {
      background: linear-gradient(rgba(15, 23, 42, 0.82), rgba(15, 23, 42, 0.90)),
                  url('https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
      background-size: cover;
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: var(--ff-sans);
      color: var(--on-surface-default);
      min-height: 100vh;
    }

    .widget-container {
      max-width: 1050px;
      width: 100%;
      margin: 0 auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      box-sizing: border-box;
    }

    .header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }

    .title {
      font-size: 28px;
      font-weight: var(--fw-semibold);
      line-height: 32px;
      margin: 0;
      color: #ffffff;
      text-shadow: 0 2px 8px rgba(0,0,0,0.8);
    }

    .subtitle {
      font-size: 14px;
      font-weight: var(--fw-normal);
      color: var(--on-surface-de-emphasis);
      margin: 4px 0 0 0;
      text-shadow: 0 1px 4px rgba(0,0,0,0.8);
    }

    .right-section {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .dashboard-hud {
      display: flex;
      background: var(--surface);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      padding: 12px 16px;
      border: 1px solid var(--stroke-default);
      border-radius: 14px;
      justify-content: space-between;
      box-shadow: var(--card-shadow);
    }

    .hud-pill {
      flex: 1;
      text-align: center;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .hud-pill:not(:last-child) {
      border-right: 1px solid var(--stroke-default);
    }

    .hud-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--on-surface-de-emphasis);
      font-weight: var(--fw-medium);
    }

    .hud-value {
      font-size: 20px;
      font-weight: var(--fw-semibold);
      font-family: var(--ff-mono);
      font-variant-numeric: tabular-nums;
      color: var(--on-surface-default);
    }

    .filter-bar {
      background: var(--surface);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--stroke-default);
      border-radius: 14px;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: var(--card-shadow);
      flex-wrap: wrap;
    }

    .filter-label {
      font-size: 13px;
      font-weight: var(--fw-semibold);
      color: var(--on-surface-de-emphasis);
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }

    .filter-select {
      flex: 1;
      background: var(--surface-container);
      color: var(--on-surface-default);
      border: 1px solid var(--outline-variant);
      padding: 8px 12px;
      border-radius: 8px;
      font-family: var(--ff-sans);
      font-size: 13px;
      outline: none;
      cursor: pointer;
      min-width: 220px;
    }

    .filter-select:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px var(--primary-container);
    }

    .btn-tonal {
      background: var(--surface-container-high);
      color: var(--on-surface-default);
      border: 1px solid var(--stroke-default);
      font-family: var(--ff-sans);
      font-weight: var(--fw-semibold);
      font-size: 13px;
      padding: 8px 16px;
      border-radius: 999px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: background 0.2s ease, transform 0.1s ease;
      user-select: none;
    }

    .btn-tonal:hover { background: var(--surface-container-highest); }
    .btn-tonal:active { transform: scale(0.98); }

    .btn-primary {
      background: var(--primary);
      color: var(--on-primary);
      border: none;
      font-family: var(--ff-sans);
      font-weight: var(--fw-semibold);
      font-size: 14px;
      padding: 10px 20px;
      border-radius: 999px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: opacity 0.2s ease, transform 0.1s ease;
      user-select: none;
    }

    .btn-primary:hover { opacity: 0.9; }
    .btn-primary:active { transform: scale(0.98); }

    .btn-danger {
      background: var(--negative);
      color: #fff;
      border: none;
      font-family: var(--ff-sans);
      font-weight: var(--fw-semibold);
      font-size: 13px;
      padding: 8px 16px;
      border-radius: 999px;
      cursor: pointer;
      transition: opacity 0.2s ease;
    }

    .btn-danger:hover { opacity: 0.9; }

    .btn-text {
      background: transparent;
      color: var(--on-surface-de-emphasis);
      border: none;
      font-family: var(--ff-sans);
      font-weight: var(--fw-medium);
      font-size: 13px;
      padding: 6px 12px;
      border-radius: 999px;
      cursor: pointer;
      transition: background 0.2s ease, color 0.2s ease;
    }

    .btn-text:hover {
      background: var(--surface-container);
      color: var(--on-surface-default);
    }

    .guitar-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .guitar-card {
      background: var(--surface);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--stroke-default);
      border-radius: 16px;
      padding: 20px;
      transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
      position: relative;
      box-shadow: var(--card-shadow);
    }

    .guitar-card:hover { border-color: var(--outline); }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .guitar-brand-model {
      font-size: 20px;
      font-weight: var(--fw-semibold);
      color: var(--on-surface-default);
      margin: 0;
    }

    .guitar-year {
      font-size: 12px;
      font-family: var(--ff-mono);
      color: var(--on-surface-de-emphasis);
      background: var(--surface-container);
      padding: 3px 10px;
      border-radius: 6px;
    }

    .section-title-card {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--primary);
      font-weight: var(--fw-semibold);
      margin: 14px 0 8px 0;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding-bottom: 4px;
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px 14px;
    }

    @media (min-width: 650px) {
      .card-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
    }

    .info-group {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .info-label {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--on-surface-de-emphasis);
      font-weight: var(--fw-medium);
    }

    .info-value {
      font-size: 13px;
      color: var(--on-surface-default);
    }

    .info-value.mono { font-family: var(--ff-mono); }

    .card-actions {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
      border-top: 1px solid var(--stroke-default);
      padding-top: 12px;
      margin-top: 16px;
    }

    .form-section-title {
      font-size: 13px;
      font-weight: var(--fw-semibold);
      color: #60a5fa;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin: 16px 0 8px 0;
      padding-bottom: 4px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      grid-column: span 2;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .form-group.full-width { grid-column: span 2; }

    .form-label {
      font-size: 11px;
      font-weight: var(--fw-medium);
      color: var(--on-surface-de-emphasis);
    }

    .input-field {
      background: var(--surface-container);
      color: var(--on-surface-default);
      border: 1px solid var(--outline-variant);
      padding: 8px 10px;
      border-radius: 8px;
      font-family: var(--ff-sans);
      font-size: 13px;
      outline: none;
      box-sizing: border-box;
      width: 100%;
    }

    .input-field:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px var(--primary-container);
    }

    .input-field.mono { font-family: var(--ff-mono); }

    .guitar-photo-wrapper {
      position: relative;
      width: 100%;
      height: 180px;
      border-radius: 10px;
      overflow: hidden;
      background: var(--surface-container-high);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .guitar-photo {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .photo-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: var(--on-surface-de-emphasis);
      gap: 4px;
      font-size: 12px;
    }

    .photo-upload-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      background: var(--surface-container-high);
      border: 1px dashed var(--outline);
      border-radius: 8px;
      color: var(--on-surface-default);
      font-size: 12px;
      cursor: pointer;
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
      transition: background 0.2s;
    }

    .photo-upload-btn:hover { background: var(--surface-container-highest); }

    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.78);
      backdrop-filter: blur(8px);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      box-sizing: border-box;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }

    .modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-box {
      background: var(--surface);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--stroke-default);
      border-radius: 20px;
      padding: 24px;
      max-width: 680px;
      width: 100%;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
      transform: translateY(20px);
      transition: transform 0.25s ease;
      display: flex;
      flex-direction: column;
      gap: 16px;
      max-height: 90vh;
      overflow-y: auto;
    }

    .modal-overlay.active .modal-box {
      transform: translateY(0);
    }

    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .modal-title {
      font-size: 18px;
      font-weight: var(--fw-semibold);
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 0;
      color: var(--on-surface-default);
    }

    .due-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 260px;
      overflow-y: auto;
    }

    .due-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--surface-container);
      padding: 10px 14px;
      border-radius: 12px;
      border: 1px solid var(--stroke-default);
    }

    .due-item-info {
      display: flex;
      flex-direction: column;
    }

    .due-item-title {
      font-size: 14px;
      font-weight: var(--fw-semibold);
    }

    .badge-overdue {
      background: rgba(239, 68, 68, 0.2);
      color: var(--negative);
      font-size: 11px;
      font-weight: var(--fw-semibold);
      padding: 4px 8px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-top: 4px;
    }

    .photo-modal-box {
      max-width: 90vw;
      max-height: 90vh;
      background: transparent;
      box-shadow: none;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
    }

    .full-image-container {
      position: relative;
      max-width: 100%;
      max-height: 80vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .full-image {
      max-width: 100%;
      max-height: 80vh;
      object-fit: contain;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }

    .empty-state {
      background: var(--surface);
      backdrop-filter: blur(14px);
      border: 1px dashed var(--outline);
      border-radius: 16px;
      padding: 30px;
      text-align: center;
      color: var(--on-surface-de-emphasis);
      font-size: 14px;
    }
  </style>
</head>
<body>

  <div class="widget-container">
    <div class="header-row">
      <div>
        <h1 class="title">Guitar Rack & Vault</h1>
        <p class="subtitle">Gestione inventario, specifiche tecniche, manutenzione e registro documenti</p>
      </div>
      <button class="btn-primary" onclick="openAddGuitarModal()">+ Nuovo Strumento</button>
    </div>

    <div class="right-section">
      <!-- HUD STATISTICHE -->
      <div class="dashboard-hud" id="hud-stats">
        <div class="hud-pill">
          <span class="hud-label">Strumenti</span>
          <span class="hud-value" id="stat-total">0</span>
        </div>
        <div class="hud-pill">
          <span class="hud-label">Scalatura Max</span>
          <span class="hud-value" id="stat-common">-</span>
        </div>
        <div class="hud-pill">
          <span class="hud-label">Setup Mese</span>
          <span class="hud-value" id="stat-setups">0</span>
        </div>
        <div class="hud-pill" id="hud-overdue-pill" style="cursor:pointer;" onclick="filterByOverdue()">
          <span class="hud-label">Cambio Corde</span>
          <span class="hud-value" id="stat-overdue" style="color:var(--negative);">0</span>
        </div>
      </div>

      <!-- TENDINA / BARRA DI SELEZIONE E FILTRAGGIO -->
      <div class="filter-bar">
        <span class="filter-label">🔍 Mostra Strumento:</span>
        <select class="filter-select" id="guitar-select-filter" onchange="handleFilterChange(this.value)">
          <option value="ALL">-- Mostra Tutti gli Strumenti --</option>
          <option value="OVERDUE" style="color:var(--negative); font-weight:bold;">⚠️ SOLO CAMBIO CORDE NECESSARIO (> 4 Mesi)</option>
        </select>
      </div>

      <!-- LISTA DELLE CHITARRE -->
      <div class="guitar-list" id="guitar-list-container">
        <!-- Carte iniettate dinamicamente -->
      </div>
    </div>
  </div>

  <!-- POPUP INSERIMENTO / MODIFICA STRUMENTO COMPLETO DI TUTTE LE SPECIFICHE -->
  <div class="modal-overlay" id="popup-form">
    <div class="modal-box">
      <div class="modal-header">
        <h3 class="modal-title" id="form-panel-title">Nuovo Strumento</h3>
        <button class="btn-text" onclick="closeModal('popup-form')">✕</button>
      </div>

      <!-- SEZIONE 4: MULTIMEDIA E DOCUMENTI -->
      <div class="form-section-title" style="margin-top:0;">4. Multimedia e Documenti</div>
      <div class="form-group full-width">
        <label class="form-label">Foto Strumento (Vista principale)</label>
        <div class="guitar-photo-wrapper" id="form-photo-preview">
          <div class="photo-placeholder">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            Nessuna foto
          </div>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 6px;">
          <label class="photo-upload-btn" style="flex:1;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Carica Foto Intera
            <input type="file" accept="image/*" id="form-input-photo" style="display:none" onchange="handleFormPhotoUpload(event)">
          </label>
          <button class="btn-text" id="btn-remove-photo" style="color:var(--negative); display:none;" onclick="removeFormPhoto()">Rimuovi</button>
        </div>
      </div>

      <div class="form-grid">
        <!-- SEZIONE 1: DATI ANAGRAFICI -->
        <div class="form-section-title">1. Dati Anagrafici dello Strumento</div>
        
        <div class="form-group">
          <label class="form-label">Marca *</label>
          <input type="text" class="input-field" id="form-brand" placeholder="es. Fender">
        </div>
        <div class="form-group">
          <label class="form-label">Modello *</label>
          <input type="text" class="input-field" id="form-model" placeholder="es. American Professional II Stratocaster">
        </div>
        <div class="form-group">
          <label class="form-label">Anno di Produzione</label>
          <input type="number" class="input-field mono" id="form-year" placeholder="2021">
        </div>
        <div class="form-group">
          <label class="form-label">Numero di Serie *</label>
          <input type="text" class="input-field mono" id="form-serial" placeholder="US210984">
        </div>
        <div class="form-group">
          <label class="form-label">Paese e Fabbrica</label>
          <input type="text" class="input-field" id="form-factory" placeholder="es. Corona, USA">
        </div>
        <div class="form-group">
          <label class="form-label">Stato dello Strumento</label>
          <select class="input-field" id="form-condition">
            <option value="Mint">Mint (Pari al nuovo)</option>
            <option value="Ottimo" selected>Ottimo</option>
            <option value="Buono">Buono</option>
            <option value="Relic / Usurato">Relic / Usurato</option>
            <option value="Da restaurare">Da restaurare</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Data Acquisto</label>
          <input type="date" class="input-field mono" id="form-purchase-date">
        </div>
        <div class="form-group">
          <label class="form-label">Prezzo Pagato (€)</label>
          <input type="number" class="input-field mono" id="form-price" placeholder="1850">
        </div>
        <div class="form-group full-width">
          <label class="form-label">Valore Attuale Stimato (€)</label>
          <input type="number" class="input-field mono" id="form-market-value" placeholder="1900">
        </div>

        <!-- SEZIONE 2: SPECIFICHE TECNICHE -->
        <div class="form-section-title">2. Specifiche Tecniche (Specs)</div>

        <div class="form-group">
          <label class="form-label">Tipo di Corpo (Body)</label>
          <input type="text" class="input-field" id="form-body" placeholder="es. Alder con Flamed Maple top, Poly">
        </div>
        <div class="form-group">
          <label class="form-label">Manico (Legno e Giunzione)</label>
          <input type="text" class="input-field" id="form-neck-wood" placeholder="es. Acero, Bolt-On">
        </div>
        <div class="form-group">
          <label class="form-label">Profilo Manico</label>
          <select class="input-field" id="form-neck-profile">
            <option value="">Seleziona profilo...</option>
            <option value="Modern C">Modern C</option>
            <option value="Vintage C / C-Shape">Vintage C / C-Shape</option>
            <option value="Slim Taper ('60s)">Slim Taper ('60s)</option>
            <option value="Deep C">Deep C</option>
            <option value="Soft V">Soft V</option>
            <option value="Hard V">Hard V</option>
            <option value="Thin U">Thin U</option>
            <option value="D-Shape ('50s)">D-Shape ('50s)</option>
            <option value="Compound">Compound</option>
            <option value="Custom">Altro / Custom</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Tastiera (Legno, Raggio, Tasti)</label>
          <input type="text" class="input-field" id="form-fretboard" placeholder="es. Palissandro, 9.5&quot;, 22 Medium Jumbo">
        </div>
        <div class="form-group">
          <label class="form-label">Scala (Scale Length)</label>
          <input type="text" class="input-field mono" id="form-scale" placeholder="es. 25.5&quot;">
        </div>
        <div class="form-group">
          <label class="form-label">Hardware (Ponte e Meccaniche)</label>
          <input type="text" class="input-field" id="form-hardware" placeholder="es. Tremolo 2 punti, Meccaniche autobloccanti">
        </div>
        <div class="form-group full-width">
          <label class="form-label">Elettronica / Pickup</label>
          <input type="text" class="input-field" id="form-pickups" placeholder="es. SSS - 3x V-Mod II Single-Coil, Treble Bleed">
        </div>

        <!-- SEZIONE 3: MANUTENZIONE E CURA -->
        <div class="form-section-title">3. Manutenzione e Cura</div>

        <div class="form-group">
          <label class="form-label">Scalatura Corde Preferita</label>
          <input type="text" class="input-field mono" id="form-gauge" placeholder="0.010-0.046">
        </div>
        <div class="form-group">
          <label class="form-label">Marca e Modello Corde</label>
          <input type="text" class="input-field" id="form-string-brand" placeholder="es. Ernie Ball Regular Slinky">
        </div>
        <div class="form-group">
          <label class="form-label">Ultimo Setup / Cambio Corde</label>
          <input type="date" class="input-field mono" id="form-setup">
        </div>
        <div class="form-group">
          <label class="form-label">Ultima Pulizia / Nutrizione Tastiera</label>
          <input type="date" class="input-field mono" id="form-clean-date">
        </div>
        <div class="form-group full-width">
          <label class="form-label">Registro Modifiche (Mod)</label>
          <input type="text" class="input-field" id="form-mods" placeholder="es. Sostituzione pickup al ponte, schermatura rame">
        </div>
        <div class="form-group full-width">
          <label class="form-label">🛠️ Storico Interventi Liuteria</label>
          <input type="text" class="input-field" id="form-lutherie" placeholder="es. Rettifica tasti, capotasto in osso sagomato">
        </div>
        <div class="form-group full-width">
          <label class="form-label">Note e Segni Particolari / Dents</label>
          <input type="text" class="input-field" id="form-notes" placeholder="Piccolo segno sul fondo del body, setup Drop D...">
        </div>
      </div>

      <div style="display: flex; gap: 8px; margin-top: 12px;">
        <button class="btn-text" onclick="closeModal('popup-form')" style="flex:1;">Annulla</button>
        <button class="btn-primary" id="btn-save" onclick="saveFormGuitar()" style="flex:2;">Salva in Vault</button>
      </div>
    </div>
  </div>

  <!-- POPUP PROMEMORIA CAMBIO CORDE INIZIALE -->
  <div class="modal-overlay" id="popup-reminder">
    <div class="modal-box">
      <div class="modal-header">
        <h3 class="modal-title">
          <span>🎸</span> Promemoria Cambio Corde (> 4 Mesi)
        </h3>
        <button class="btn-text" onclick="closeModal('popup-reminder')">✕</button>
      </div>
      <p style="font-size:13px; color:var(--on-surface-de-emphasis); margin:0;">
        Sono trascorsi più di 4 mesi dall'ultimo setup o cambio corde per questi strumenti.
      </p>
      <div class="due-list" id="due-list-container"></div>
      <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:8px;">
        <button class="btn-tonal" onclick="closeModal('popup-reminder')">Chiudi</button>
      </div>
    </div>
  </div>

  <!-- POPUP INGRANDIMENTO FOTO -->
  <div class="modal-overlay" id="popup-photo">
    <div class="photo-modal-box">
      <button class="btn-tonal" style="position:absolute; top:-40px; right:0; background:rgba(255,255,255,0.2); color:#fff; border:none;" onclick="closeModal('popup-photo')">Chiudi ✕</button>
      <div class="full-image-container">
        <img src="" id="full-photo-img" class="full-image" alt="Foto Intera Strumento">
      </div>
      <span id="full-photo-caption" style="color:#fff; margin-top:12px; font-weight:var(--fw-medium); text-shadow:0 2px 4px rgba(0,0,0,0.8);"></span>
    </div>
  </div>

  <script>
    let defaultGuitars = [
      {
        id: "g-1",
        brand: "Fender",
        model: "American Professional II Stratocaster",
        year: 2021,
        serialNumber: "US210984",
        factory: "Corona, USA",
        purchaseDate: "2021-11-15",
        pricePaid: "1850",
        marketValue: "1950",
        condition: "Mint",
        body: "Alder con finitura Gloss Urethane",
        neckWood: "Acero, Bolt-On con Micro-Tilt",
        neckProfile: "Deep C",
        fretboard: "Palissandro, Raggio 9.5\", 22 Narrow Tall",
        scaleLength: "25.5\"",
        hardware: "Tremolo Sincronizzato 2-Punti, Meccaniche Autobloccanti",
        pickups: "SSS - 3x V-Mod II Single-Coil",
        stringGauge: "0.010-0.046",
        stringBrand: "Ernie Ball Regular Slinky",
        lastSetup: "2025-10-10",
        lastFretboardClean: "2025-10-10",
        mods: "Schermatura cavità controlli con foglia di rame",
        lutherieWork: "Capotasto in osso sagomato a mano",
        notes: "Azione molto bassa, setup Mi Standard",
        photo: "https://images.unsplash.com/photo-1550985616-10810253b84d?q=80&w=800&auto=format&fit=crop"
      },
      {
        id: "g-2",
        brand: "Gibson",
        model: "Les Paul Standard '60s",
        year: 2022,
        serialNumber: "22091004",
        factory: "Nashville, USA",
        purchaseDate: "2022-05-20",
        pricePaid: "2400",
        marketValue: "2500",
        condition: "Ottimo",
        body: "Mogano pieno con Top Acero Fiammato AA",
        neckWood: "Mogano, Set-Neck",
        neckProfile: "Slim Taper ('60s)",
        fretboard: "Palissandro, Raggio 12\", 22 Medium Jumbo",
        scaleLength: "24.75\"",
        hardware: "Ponte ABR-1 Tune-O-Matic, Meccaniche Grover Rotomatics",
        pickups: "HH - Burstbucker 61R / 61T",
        stringGauge: "0.010-0.052",
        stringBrand: "Elixir Optiweb",
        lastSetup: "2025-02-15",
        lastFretboardClean: "2025-02-15",
        mods: "Condensatori Orange Drop e potenziometri 500k Custom Audio",
        lutherieWork: "Rettifica e lucidatura tasti PLEK",
        notes: "Piccolo dent invisibile sul binding inferiore",
        photo: "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?q=80&w=800&auto=format&fit=crop"
      }
    ];

    // Caricamento da LocalStorage
    let stored = localStorage.getItem("guitar_vault_data");
    let guitars = stored ? JSON.parse(stored) : defaultGuitars;

    function saveToStorage() {
      localStorage.setItem("guitar_vault_data", JSON.stringify(guitars));
    }

    let currentFilter = "ALL";
    let activeEditingId = null;
    let currentFormPhoto = "";
    let hasShownPopupOnLoad = false;

    const container = document.getElementById("guitar-list-container");
    const selectFilter = document.getElementById("guitar-select-filter");
    const statTotal = document.getElementById("stat-total");
    const statCommon = document.getElementById("stat-common");
    const statSetups = document.getElementById("stat-setups");
    const statOverdue = document.getElementById("stat-overdue");

    function getMonthsSinceSetup(dateString) {
      if (!dateString) return 999;
      const setupDate = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - setupDate);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return Math.floor(diffDays / 30);
    }

    function isSetupOlderThan4Months(dateString) {
      if (!dateString) return true;
      const setupDate = new Date(dateString);
      const fourMonthsAgo = new Date();
      fourMonthsAgo.setMonth(fourMonthsAgo.getMonth() - 4);
      return setupDate < fourMonthsAgo;
    }

    function updateSelectOptions() {
      const selectedValue = selectFilter.value;
      selectFilter.innerHTML = `
        <option value="ALL">-- Mostra Tutti gli Strumenti (${guitars.length}) --</option>
        <option value="OVERDUE" style="color:var(--negative); font-weight:bold;">⚠️ SOLO CAMBIO CORDE NECESSARIO (> 4 Mesi)</option>
      `;

      guitars.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g.id;
        const isOverdue = isSetupOlderThan4Months(g.lastSetup);
        opt.textContent = `${g.brand} ${g.model} ${g.year ? '(' + g.year + ')' : ''} ${isOverdue ? '⚠️' : ''}`;
        selectFilter.appendChild(opt);
      });

      selectFilter.value = selectedValue || "ALL";
    }

    function handleFilterChange(val) {
      currentFilter = val;
      render();
    }

    function filterByOverdue() {
      selectFilter.value = "OVERDUE";
      currentFilter = "OVERDUE";
      render();
    }

    function updateStats() {
      statTotal.textContent = guitars.length;

      if (guitars.length === 0) {
        statCommon.textContent = "-";
        statSetups.textContent = "0";
        statOverdue.textContent = "0";
        return;
      }

      // Scalatura più usata
      const gauges = guitars.map(g => g.stringGauge || "-");
      const counts = {};
      let maxGauge = "-";
      let maxCount = 0;
      gauges.forEach(gauge => {
        if(gauge !== "-") {
          counts[gauge] = (counts[gauge] || 0) + 1;
          if (counts[gauge] > maxCount) {
            maxCount = counts[gauge];
            maxGauge = gauge;
          }
        }
      });
      statCommon.textContent = maxGauge;

      // Setup questo mese
      const now = new Date();
      const currentMonth = now.getMonth();
      const currentYear = now.getFullYear();
      const thisMonthSetups = guitars.filter(g => {
        if (!g.lastSetup) return false;
        const d = new Date(g.lastSetup);
        return d.getMonth() === currentMonth && d.getFullYear() === currentYear;
      }).length;
      statSetups.textContent = thisMonthSetups;

      // Overdue
      const overdueGuitars = guitars.filter(g => isSetupOlderThan4Months(g.lastSetup));
      statOverdue.textContent = overdueGuitars.length;

      if (!hasShownPopupOnLoad && overdueGuitars.length > 0) {
        hasShownPopupOnLoad = true;
        showReminderModal(overdueGuitars);
      }
    }

    function showReminderModal(overdueGuitars) {
      const list = document.getElementById("due-list-container");
      list.innerHTML = "";
      overdueGuitars.forEach(g => {
        const months = getMonthsSinceSetup(g.lastSetup);
        const item = document.createElement("div");
        item.className = "due-item";
        item.innerHTML = `
          <div class="due-item-info">
            <span class="due-item-title">${g.brand} ${g.model}</span>
            <span class="badge-overdue">⚠️ Setup: ${g.lastSetup || 'Mai'} (${months} mesi fa)</span>
          </div>
          <button class="btn-tonal" onclick="quickSetupUpdate('${g.id}')">Segna Come Fatto</button>
        `;
        list.appendChild(item);
      });
      openModal("popup-reminder");
    }

    function quickSetupUpdate(id) {
      const g = guitars.find(x => x.id === id);
      if (g) {
        const today = new Date().toISOString().split('T')[0];
        g.lastSetup = today;
        g.lastFretboardClean = today;
        saveToStorage();
        render();
        closeModal("popup-reminder");
      }
    }

    function render() {
      updateSelectOptions();
      updateStats();
      container.innerHTML = "";

      let filtered = guitars;
      if (currentFilter === "OVERDUE") {
        filtered = guitars.filter(g => isSetupOlderThan4Months(g.lastSetup));
      } else if (currentFilter !== "ALL") {
        filtered = guitars.filter(g => g.id === currentFilter);
      }

      if (filtered.length === 0) {
        container.innerHTML = `<div class="empty-state">Nessuno strumento trovato per i criteri selezionati.</div>`;
        return;
      }

      filtered.forEach(g => {
        const isOverdue = isSetupOlderThan4Months(g.lastSetup);
        const card = document.createElement("div");
        card.className = "guitar-card";
        
        card.innerHTML = `
          <div class="card-header">
            <div>
              <h2 class="guitar-brand-model">${g.brand} ${g.model}</h2>
              <div style="font-size:12px; color:var(--on-surface-de-emphasis); margin-top:2px;">
                S/N: <span class="mono">${g.serialNumber || 'N/D'}</span> | ${g.factory || 'Origine N/D'}
              </div>
            </div>
            <span class="guitar-year">${g.year || 'N/D'}</span>
          </div>

          ${g.photo ? `
            <div class="guitar-photo-wrapper" style="margin-bottom:14px;" onclick="viewPhoto('${g.photo}', '${g.brand} ${g.model}')">
              <img src="${g.photo}" class="guitar-photo" alt="Foto ${g.brand}">
            </div>
          ` : ''}

          <div class="section-title-card">1. Anagrafica & Valore</div>
          <div class="card-grid">
            <div class="info-group">
              <span class="info-label">Stato</span>
              <span class="info-value">${g.condition || 'N/D'}</span>
            </div>
            <div class="info-group">
              <span class="info-label">Acquistata il</span>
              <span class="info-value mono">${g.purchaseDate || 'N/D'}</span>
            </div>
            <div class="info-group">
              <span class="info-label">Prezzo Pagato / Valore</span>
              <span class="info-value mono">€${g.pricePaid || '0'} / €${g.marketValue || '0'}</span>
            </div>
          </div>

          <div class="section-title-card">2. Specifiche Tecniche</div>
          <div class="card-grid">
            <div class="info-group"><span class="info-label">Body</span><span class="info-value">${g.body || 'N/D'}</span></div>
            <div class="info-group"><span class="info-label">Manico / Profilo</span><span class="info-value">${g.neckWood || ''} (${g.neckProfile || 'N/D'})</span></div>
            <div class="info-group"><span class="info-label">Tastiera / Scala</span><span class="info-value">${g.fretboard || 'N/D'} - ${g.scaleLength || ''}</span></div>
            <div class="info-group"><span class="info-label">Hardware</span><span class="info-value">${g.hardware || 'N/D'}</span></div>
            <div class="info-group" style="grid-column: span 2;"><span class="info-label">Elettronica</span><span class="info-value">${g.pickups || 'N/D'}</span></div>
          </div>

          <div class="section-title-card">3. Manutenzione & Registro</div>
          <div class="card-grid">
            <div class="info-group">
              <span class="info-label">Scalatura / Marca Corde</span>
              <span class="info-value mono">${g.stringGauge || 'N/D'} (${g.stringBrand || 'N/D'})</span>
            </div>
            <div class="info-group">
              <span class="info-label">Ultimo Setup</span>
              <span class="info-value mono" style="${isOverdue ? 'color:var(--negative); font-weight:bold;' : ''}">
                ${g.lastSetup || 'Mai'} ${isOverdue ? '⚠️ (>4 mesi)' : '✓'}
              </span>
            </div>
            <div class="info-group">
              <span class="info-label">Pulizia Tastiera</span>
              <span class="info-value mono">${g.lastFretboardClean || 'N/D'}</span>
            </div>
            <div class="info-group" style="grid-column: span 3;"><span class="info-label">Modifiche</span><span class="info-value">${g.mods || 'Nessuna'}</span></div>
            <div class="info-group" style="grid-column: span 3;"><span class="info-label">Interventi Liuteria</span><span class="info-value">${g.lutherieWork || 'Nessuno'}</span></div>
            <div class="info-group" style="grid-column: span 3;"><span class="info-label">Note</span><span class="info-value">${g.notes || 'Nessuna nota'}</span></div>
          </div>

          <div class="card-actions">
            <button class="btn-danger" onclick="deleteGuitar('${g.id}')">Elimina</button>
            <button class="btn-tonal" onclick="openEditGuitarModal('${g.id}')">Modifica Scheda</button>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function openModal(id) { document.getElementById(id).classList.add("active"); }
    function closeModal(id) { document.getElementById(id).classList.remove("active"); }

    function openAddGuitarModal() {
      activeEditingId = null;
      currentFormPhoto = "";
      document.getElementById("form-panel-title").textContent = "Nuovo Strumento";
      resetFormFields();
      updatePhotoPreview();
      openModal("popup-form");
    }

    function openEditGuitarModal(id) {
      activeEditingId = id;
      const g = guitars.find(x => x.id === id);
      if (!g) return;

      document.getElementById("form-panel-title").textContent = "Modifica: " + g.brand + " " + g.model;
      document.getElementById("form-brand").value = g.brand || "";
      document.getElementById("form-model").value = g.model || "";
      document.getElementById("form-year").value = g.year || "";
      document.getElementById("form-serial").value = g.serialNumber || "";
      document.getElementById("form-factory").value = g.factory || "";
      document.getElementById("form-condition").value = g.condition || "Ottimo";
      document.getElementById("form-purchase-date").value = g.purchaseDate || "";
      document.getElementById("form-price").value = g.pricePaid || "";
      document.getElementById("form-market-value").value = g.marketValue || "";

      document.getElementById("form-body").value = g.body || "";
      document.getElementById("form-neck-wood").value = g.neckWood || "";
      document.getElementById("form-neck-profile").value = g.neckProfile || "";
      document.getElementById("form-fretboard").value = g.fretboard || "";
      document.getElementById("form-scale").value = g.scaleLength || "";
      document.getElementById("form-hardware").value = g.hardware || "";
      document.getElementById("form-pickups").value = g.pickups || "";

      document.getElementById("form-gauge").value = g.stringGauge || "";
      document.getElementById("form-string-brand").value = g.stringBrand || "";
      document.getElementById("form-setup").value = g.lastSetup || "";
      document.getElementById("form-clean-date").value = g.lastFretboardClean || "";
      document.getElementById("form-mods").value = g.mods || "";
      document.getElementById("form-lutherie").value = g.lutherieWork || "";
      document.getElementById("form-notes").value = g.notes || "";

      currentFormPhoto = g.photo || "";
      updatePhotoPreview();
      openModal("popup-form");
    }

    function resetFormFields() {
      const inputs = document.querySelectorAll("#popup-form input, #popup-form select");
      inputs.forEach(i => {
        if(i.type !== "file") i.value = "";
      });
      document.getElementById("form-condition").value = "Ottimo";
    }

    function handleFormPhotoUpload(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          currentFormPhoto = evt.target.result;
          updatePhotoPreview();
        };
        reader.readAsDataURL(file);
      }
    }

    function removeFormPhoto() {
      currentFormPhoto = "";
      updatePhotoPreview();
    }

    function updatePhotoPreview() {
      const wrapper = document.getElementById("form-photo-preview");
      const btnRemove = document.getElementById("btn-remove-photo");
      if (currentFormPhoto) {
        wrapper.innerHTML = `<img src="${currentFormPhoto}" class="guitar-photo">`;
        btnRemove.style.display = "inline-flex";
      } else {
        wrapper.innerHTML = `
          <div class="photo-placeholder">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            Nessuna foto
          </div>`;
        btnRemove.style.display = "none";
      }
    }

    function saveFormGuitar() {
      const brand = document.getElementById("form-brand").value.trim();
      const model = document.getElementById("form-model").value.trim();

      if (!brand || !model) {
        alert("Inserisci almeno Marca e Modello per salvare lo strumento.");
        return;
      }

      const guitarObj = {
        id: activeEditingId ? activeEditingId : "g-" + Date.now(),
        brand: brand,
        model: model,
        year: document.getElementById("form-year").value,
        serialNumber: document.getElementById("form-serial").value,
        factory: document.getElementById("form-factory").value,
        condition: document.getElementById("form-condition").value,
        purchaseDate: document.getElementById("form-purchase-date").value,
        pricePaid: document.getElementById("form-price").value,
        marketValue: document.getElementById("form-market-value").value,

        body: document.getElementById("form-body").value,
        neckWood: document.getElementById("form-neck-wood").value,
        neckProfile: document.getElementById("form-neck-profile").value,
        fretboard: document.getElementById("form-fretboard").value,
        scaleLength: document.getElementById("form-scale").value,
        hardware: document.getElementById("form-hardware").value,
        pickups: document.getElementById("form-pickups").value,

        stringGauge: document.getElementById("form-gauge").value,
        stringBrand: document.getElementById("form-string-brand").value,
        lastSetup: document.getElementById("form-setup").value,
        lastFretboardClean: document.getElementById("form-clean-date").value,
        mods: document.getElementById("form-mods").value,
        lutherieWork: document.getElementById("form-lutherie").value,
        notes: document.getElementById("form-notes").value,

        photo: currentFormPhoto
      };

      if (activeEditingId) {
        const idx = guitars.findIndex(x => x.id === activeEditingId);
        if (idx !== -1) guitars[idx] = guitarObj;
      } else {
        guitars.push(guitarObj);
      }

      saveToStorage();
      render();
      closeModal("popup-form");
    }

    function deleteGuitar(id) {
      if (confirm("Sei sicuro di voler eliminare definitivamente questa scheda strumento dal Vault?")) {
        guitars = guitars.filter(x => x.id !== id);
        saveToStorage();
        render();
      }
    }

    function viewPhoto(url, title) {
      document.getElementById("full-photo-img").src = url;
      document.getElementById("full-photo-caption").textContent = title;
      openModal("popup-photo");
    }

    // Inizializzazione
    render();
  </script>
</body>
</html>
"""

# Render in Streamlit
components.html(html_code, height=950, scrolling=True)