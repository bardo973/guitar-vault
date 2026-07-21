import streamlit as st

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
      /* Foto di sfondo: Fender Stratocaster */
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
      max-width: 900px;
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
      gap: 14px;
    }

    .guitar-card {
      background: var(--surface);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--stroke-default);
      border-radius: 16px;
      padding: 18px;
      transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
      position: relative;
      box-shadow: var(--card-shadow);
      cursor: pointer;
    }

    .guitar-card:hover {
      border-color: var(--outline);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .guitar-brand-model {
      font-size: 18px;
      font-weight: var(--fw-semibold);
      color: var(--on-surface-default);
      margin: 0;
    }

    .guitar-year {
      font-size: 12px;
      font-family: var(--ff-mono);
      color: var(--on-surface-de-emphasis);
      background: var(--surface-container);
      padding: 2px 8px;
      border-radius: 6px;
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px 14px;
    }

    @media (min-width: 600px) {
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
      padding-top: 10px;
      margin-top: 12px;
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
      font-size: 12px;
      font-weight: var(--fw-medium);
      color: var(--on-surface-default);
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

    .confirm-banner {
      background: var(--surface-container);
      border: 1px solid var(--outline-variant);
      border-radius: 12px;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .confirm-text {
      font-size: 13px;
      color: var(--on-surface-default);
    }

    .guitar-photo-wrapper {
      position: relative;
      width: 100%;
      height: 160px;
      border-radius: 10px;
      overflow: hidden;
      background: var(--surface-container-high);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
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

    /* MODALI POPUP */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.75);
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
      max-width: 520px;
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

    .due-item-sub {
      font-size: 12px;
      color: var(--negative);
      font-weight: var(--fw-medium);
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

    .photo-zoom-hint {
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0,0,0,0.6);
      color: #fff;
      font-size: 10px;
      padding: 4px 8px;
      border-radius: 6px;
      backdrop-filter: blur(4px);
      pointer-events: none;
      display: flex;
      align-items: center;
      gap: 4px;
    }
  </style>
</head>
<body>

  <div class="widget-container">
    <div class="header-row">
      <div>
        <h1 class="title">Guitar Rack & Vault</h1>
        <p class="subtitle">Gestione inventario, scalature, setup e interventi di liuteria</p>
      </div>
      <button class="btn-primary" onclick="openAddGuitarModal()">+ Nuovo Strumento</button>
    </div>

    <div class="right-section">
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
        <div class="hud-pill" id="hud-overdue-pill" style="cursor:pointer;" onclick="checkStringChangeReminders(true)">
          <span class="hud-label">Cambio Corde</span>
          <span class="hud-value" id="stat-overdue" style="color:var(--negative);">0</span>
        </div>
      </div>

      <div class="guitar-list" id="guitar-list-container">
        <!-- Carte iniettate dinamicamente -->
      </div>
    </div>
  </div>

  <!-- POPUP INSERIMENTO / MODIFICA STRUMENTO -->
  <div class="modal-overlay" id="popup-form">
    <div class="modal-box">
      <div class="modal-header">
        <h3 class="modal-title" id="form-panel-title">Nuovo Strumento</h3>
        <button class="btn-text" onclick="closeModal('popup-form')">✕</button>
      </div>

      <div class="form-group full-width">
        <label class="form-label">Foto Strumento</label>
        <div class="guitar-photo-wrapper" id="form-photo-preview">
          <div class="photo-placeholder">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            Nessuna foto
          </div>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 6px;">
          <label class="photo-upload-btn" style="flex:1;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Carica Foto
            <input type="file" accept="image/*" id="form-input-photo" style="display:none" onchange="handleFormPhotoUpload(event)">
          </label>
          <button class="btn-text" id="btn-remove-photo" style="color:var(--negative); display:none;" onclick="removeFormPhoto()">Rimuovi</button>
        </div>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Marca *</label>
          <input type="text" class="input-field" id="form-brand" placeholder="es. Fender">
        </div>
        <div class="form-group">
          <label class="form-label">Modello *</label>
          <input type="text" class="input-field" id="form-model" placeholder="es. Stratocaster">
        </div>
        <div class="form-group">
          <label class="form-label">Anno</label>
          <input type="number" class="input-field mono" id="form-year" placeholder="1968">
        </div>
        <div class="form-group">
          <label class="form-label">Num. Serial</label>
          <input type="text" class="input-field mono" id="form-serial" placeholder="US123456">
        </div>
        <div class="form-group">
          <label class="form-label">Scalatura Corde</label>
          <input type="text" class="input-field mono" id="form-gauge" placeholder="0.010-0.046">
        </div>
        <div class="form-group">
          <label class="form-label">Marca Corde</label>
          <input type="text" class="input-field" id="form-string-brand" placeholder="es. Ernie Ball">
        </div>
        <div class="form-group">
          <label class="form-label">Pick Up</label>
          <input type="text" class="input-field" id="form-pickups" placeholder="es. 3x Single Coil">
        </div>
        <div class="form-group">
          <label class="form-label">Profilo Manico</label>
          <select class="input-field" id="form-neck">
            <option value="">Seleziona profilo...</option>
            <option value="Modern C">Modern C</option>
            <option value="C-Shape">Vintage C / C-Shape</option>
            <option value="Slim Taper">Slim Taper ('60s)</option>
            <option value="Deep C">Deep C</option>
            <option value="Soft V">Soft V</option>
            <option value="Hard V">Hard V</option>
            <option value="Thin U">Thin U</option>
            <option value="D-Shape">D-Shape ('50s)</option>
            <option value="Asimmetrico / Compound">Asimmetrico / Compound</option>
            <option value="Altro / Custom">Altro / Custom</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Ultimo Setup</label>
          <input type="date" class="input-field mono" id="form-setup">
        </div>
        
        <div class="form-group full-width">
          <label class="form-label">🛠️ Interventi di Liuteria</label>
          <input type="text" class="input-field" id="form-lutherie" placeholder="es. Rettifica tasti, capotasto in osso, schermatura...">
        </div>

        <div class="form-group full-width">
          <label class="form-label">Note Aggiuntive</label>
          <input type="text" class="input-field" id="form-notes" placeholder="Drop D, action bassa...">
        </div>
      </div>

      <div style="display: flex; gap: 8px; margin-top: 8px;">
        <button class="btn-text" onclick="closeModal('popup-form')" style="flex:1;">Annulla</button>
        <button class="btn-primary" id="btn-save" onclick="saveFormGuitar()" style="flex:2;">Salva in Rack</button>
      </div>
    </div>
  </div>

  <!-- POPUP CAMBIO CORDE -->
  <div class="modal-overlay" id="popup-reminder">
    <div class="modal-box">
      <div class="modal-header">
        <h3 class="modal-title">
          <span>🎸</span> Promemoria Cambio Corde (> 4 Mesi)
        </h3>
        <button class="btn-text" onclick="closeModal('popup-reminder')">✕</button>
      </div>
      <p style="font-size:13px; color:var(--on-surface-de-emphasis); margin:0;">
        Sono trascorsi più di 4 mesi dall'ultimo setup per questi strumenti.
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
    let guitars = [
      {
        id: "g-1",
        brand: "Fender",
        model: "Stratocaster American Professional II",
        year: 2021,
        serialNumber: "US210984",
        stringGauge: "0.010-0.046",
        stringBrand: "Ernie Ball",
        pickups: "3x V-Mod II Single-Coil",
        neckProfile: "Deep C",
        lastSetup: "2025-10-10",
        lutherieWork: "Capotasto in osso sagomato a mano, schermatura vano controlli",
        notes: "Setup per Mi standard, action bassa",
        photo: ""
      },
      {
        id: "g-2",
        brand: "PRS",
        model: "Custom 24",
        year: 2019,
        serialNumber: "19 28374",
        stringGauge: "0.010-0.046",
        stringBrand: "D'Addario",
        pickups: "85/15 Humbuckers",
        neckProfile: "Thin U",
        lastSetup: "2026-06-02",
        lutherieWork: "Rettifica e lucidatura tasti PLEK",
        notes: "Top in acero fiammato",
        photo: ""
      },
      {
        id: "g-3",
        brand: "Gibson",
        model: "Les Paul Standard '60s",
        year: 2022,
        serialNumber: "22091004",
        stringGauge: "0.010-0.052",
        stringBrand: "Elixir",
        pickups: "60s Burstbucker HH",
        neckProfile: "Slim Taper",
        lastSetup: "2025-08-15",
        lutherieWork: "Sostituzione bridge con ABR-1 in ottone e ricablaggio potenziometri 500k",
        notes: "Bourbon Burst",
        photo: ""
      }
    ];

    let activeEditingId = null;
    let deletingId = null;
    let currentFormPhoto = "";
    let hasShownPopupOnLoad = false;

    const container = document.getElementById("guitar-list-container");
    const statTotal = document.getElementById("stat-total");
    const statCommon = document.getElementById("stat-common");
    const statSetups = document.getElementById("stat-setups");

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

    function updateStats() {
      statTotal.textContent = guitars.length;

      if (guitars.length === 0) {
        statCommon.textContent = "-";
        statSetups.textContent = "0";
        document.getElementById("stat-overdue").textContent = "0";
        return;
      }

      const gauges = guitars.map(g => g.stringGauge || "-");
      const counts = {};
      let maxGauge = "-";
      let maxCount = 0;
      gauges.forEach(gauge => {
        counts[gauge] = (counts[gauge] || 0) + 1;
        if (counts[gauge] > maxCount) {
          maxCount = counts[gauge];
          maxGauge = gauge;
        }
      });
      statCommon.textContent = maxGauge;

      const now = new Date();
      const currentYearMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
      const recentSetups = guitars.filter(g => g.lastSetup && g.lastSetup.startsWith(currentYearMonth)).length;
      statSetups.textContent = recentSetups;

      const overdueCount = guitars.filter(g => isSetupOlderThan4Months(g.lastSetup)).length;
      document.getElementById("stat-overdue").textContent = overdueCount;
    }

    function render() {
      container.innerHTML = "";

      guitars.forEach(guitar => {
        const card = document.createElement("div");
        card.className = "guitar-card";

        const isOverdue = isSetupOlderThan4Months(guitar.lastSetup);
        const monthsCount = getMonthsSinceSetup(guitar.lastSetup);

        if (deletingId === guitar.id) {
          card.innerHTML = `
            <div class="confirm-banner">
              <span class="confirm-text">Eliminare <strong>${guitar.brand} ${guitar.model}</strong>?</span>
              <div style="display:flex; gap:6px;">
                <button class="btn-text" onclick="event.stopPropagation(); cancelDelete()">Annulla</button>
                <button class="btn-danger" onclick="event.stopPropagation(); confirmDelete('${guitar.id}')">Rimuovi</button>
              </div>
            </div>
          `;
        } else {
          card.onclick = () => selectGuitarForEdit(guitar.id);
          card.innerHTML = `
            ${guitar.photo ? `
              <div class="guitar-photo-wrapper" style="margin-bottom:12px;" onclick="event.stopPropagation(); openPhotoModal('${guitar.photo}', '${guitar.brand} ${guitar.model}')">
                <img src="${guitar.photo}" class="guitar-photo" alt="${guitar.brand} ${guitar.model}">
                <div class="photo-zoom-hint">🔍 Foto Intera</div>
              </div>` : ''}
            <div class="card-header">
              <div>
                <h3 class="guitar-brand-model">${guitar.brand || 'Senza Marca'} ${guitar.model || 'Senza Modello'}</h3>
                ${isOverdue ? `<div class="badge-overdue">⚠️ Cambio Corde Consigliato (${monthsCount >= 999 ? 'Mai fatto' : '+' + monthsCount + ' mesi'})</div>` : ''}
              </div>
              ${guitar.year ? `<span class="guitar-year">${guitar.year}</span>` : ''}
            </div>
            <div class="card-grid">
              <div class="info-group">
                <span class="info-label">Serial Number</span>
                <span class="info-value mono">${guitar.serialNumber || 'N/D'}</span>
              </div>
              <div class="info-group">
                <span class="info-label">Scalatura Corde</span>
                <span class="info-value mono">${guitar.stringGauge || 'N/D'}</span>
              </div>
              <div class="info-group">
                <span class="info-label">Marca Corde</span>
                <span class="info-value">${guitar.stringBrand || 'N/D'}</span>
              </div>
              <div class="info-group">
                <span class="info-label">Pick Up</span>
                <span class="info-value">${guitar.pickups || 'N/D'}</span>
              </div>
              <div class="info-group">
                <span class="info-label">Profilo Manico</span>
                <span class="info-value">${guitar.neckProfile || 'N/D'}</span>
              </div>
              <div class="info-group">
                <span class="info-label">Ultimo Setup</span>
                <span class="info-value mono" style="${isOverdue ? 'color:var(--negative); font-weight:bold;' : ''}">${guitar.lastSetup || 'N/D'}</span>
              </div>
              <div class="info-group full-width" style="grid-column: span 2;">
                <span class="info-label">🛠️ Interventi di Liuteria</span>
                <span class="info-value" style="color:#93c5fd;">${guitar.lutherieWork || 'Nessun intervento registrato'}</span>
              </div>
              <div class="info-group full-width" style="grid-column: span 2;">
                <span class="info-label">Note</span>
                <span class="info-value">${guitar.notes || '-'}</span>
              </div>
            </div>
            <div class="card-actions">
              ${isOverdue ? `<button class="btn-text" style="color:var(--primary);" onclick="event.stopPropagation(); markStringsChangedToday('${guitar.id}')">✨ Cambiate Oggi</button>` : ''}
              <button class="btn-text" onclick="event.stopPropagation(); setDeleteState('${guitar.id}')">Elimina</button>
              <button class="btn-tonal" onclick="event.stopPropagation(); selectGuitarForEdit('${guitar.id}')">Modifica</button>
            </div>
          `;
        }

        container.appendChild(card);
      });

      updateStats();
    }

    function checkStringChangeReminders(forceOpen = false) {
      const overdueGuitars = guitars.filter(g => isSetupOlderThan4Months(g.lastSetup));
      
      if (overdueGuitars.length > 0 && (!hasShownPopupOnLoad || forceOpen)) {
        hasShownPopupOnLoad = true;
        const dueContainer = document.getElementById("due-list-container");
        dueContainer.innerHTML = "";

        overdueGuitars.forEach(g => {
          const m = getMonthsSinceSetup(g.lastSetup);
          const item = document.createElement("div");
          item.className = "due-item";
          item.innerHTML = `
            <div class="due-item-info">
              <span class="due-item-title">${g.brand} ${g.model}</span>
              <span class="due-item-sub">Setup: ${g.lastSetup || 'Mai'} (${m >= 999 ? '>4 mesi' : m + ' mesi fa'})</span>
            </div>
            <button class="btn-primary" style="font-size:12px; padding:6px 12px; width:auto;" onclick="markStringsChangedToday('${g.id}')">Segna Cambiate</button>
          `;
          dueContainer.appendChild(item);
        });

        openModal("popup-reminder");
      } else if (forceOpen && overdueGuitars.length === 0) {
        alert("Tutti gli strumenti sono stati settati negli ultimi 4 mesi!");
      }
    }

    function markStringsChangedToday(id) {
      const g = guitars.find(item => item.id === id);
      if (g) {
        g.lastSetup = new Date().toISOString().split('T')[0];
        render();
        checkStringChangeReminders(false);
        const overdueGuitars = guitars.filter(item => isSetupOlderThan4Months(item.lastSetup));
        if (overdueGuitars.length === 0) {
          closeModal("popup-reminder");
        }
      }
    }

    function openAddGuitarModal() {
      resetForm();
      openModal("popup-form");
    }

    function selectGuitarForEdit(id) {
      const g = guitars.find(item => item.id === id);
      if (!g) return;

      activeEditingId = id;
      document.getElementById("form-panel-title").textContent = "Modifica Strumento";
      document.getElementById("btn-save").textContent = "Aggiorna";

      document.getElementById("form-brand").value = g.brand || "";
      document.getElementById("form-model").value = g.model || "";
      document.getElementById("form-year").value = g.year || "";
      document.getElementById("form-serial").value = g.serialNumber || "";
      document.getElementById("form-gauge").value = g.stringGauge || "";
      document.getElementById("form-string-brand").value = g.stringBrand || "";
      document.getElementById("form-pickups").value = g.pickups || "";
      document.getElementById("form-neck").value = g.neckProfile || "";
      document.getElementById("form-setup").value = g.lastSetup || "";
      document.getElementById("form-lutherie").value = g.lutherieWork || "";
      document.getElementById("form-notes").value = g.notes || "";

      currentFormPhoto = g.photo || "";
      updatePhotoPreview();
      openModal("popup-form");
    }

    function resetForm() {
      activeEditingId = null;
      document.getElementById("form-panel-title").textContent = "Nuovo Strumento";
      document.getElementById("btn-save").textContent = "Salva in Rack";

      document.getElementById("form-brand").value = "";
      document.getElementById("form-model").value = "";
      document.getElementById("form-year").value = "";
      document.getElementById("form-serial").value = "";
      document.getElementById("form-gauge").value = "";
      document.getElementById("form-string-brand").value = "";
      document.getElementById("form-pickups").value = "";
      document.getElementById("form-neck").value = "";
      document.getElementById("form-setup").value = "";
      document.getElementById("form-lutherie").value = "";
      document.getElementById("form-notes").value = "";

      currentFormPhoto = "";
      updatePhotoPreview();
    }

    function handleFormPhotoUpload(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(evt) {
        currentFormPhoto = evt.target.result;
        updatePhotoPreview();
      };
      reader.readAsDataURL(file);
    }

    function removeFormPhoto() {
      currentFormPhoto = "";
      document.getElementById("form-input-photo").value = "";
      updatePhotoPreview();
    }

    function updatePhotoPreview() {
      const preview = document.getElementById("form-photo-preview");
      const removeBtn = document.getElementById("btn-remove-photo");
      if (currentFormPhoto) {
        preview.innerHTML = `<img src="${currentFormPhoto}" class="guitar-photo" alt="Anteprima">`;
        removeBtn.style.display = "inline-block";
      } else {
        preview.innerHTML = `
          <div class="photo-placeholder">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            Nessuna foto
          </div>`;
        removeBtn.style.display = "none";
      }
    }

    function saveFormGuitar() {
      const brand = document.getElementById("form-brand").value.trim();
      const model = document.getElementById("form-model").value.trim();

      if (!brand || !model) {
        alert("Marca e Modello sono campi obbligatori!");
        return;
      }

      const guitarData = {
        brand: brand,
        model: model,
        year: document.getElementById("form-year").value ? parseInt(document.getElementById("form-year").value) : "",
        serialNumber: document.getElementById("form-serial").value.trim(),
        stringGauge: document.getElementById("form-gauge").value.trim(),
        stringBrand: document.getElementById("form-string-brand").value.trim(),
        pickups: document.getElementById("form-pickups").value.trim(),
        neckProfile: document.getElementById("form-neck").value,
        lastSetup: document.getElementById("form-setup").value,
        lutherieWork: document.getElementById("form-lutherie").value.trim(),
        notes: document.getElementById("form-notes").value.trim(),
        photo: currentFormPhoto
      };

      if (activeEditingId) {
        const index = guitars.findIndex(g => g.id === activeEditingId);
        if (index !== -1) {
          guitars[index] = { ...guitars[index], ...guitarData };
        }
      } else {
        guitarData.id = "g-" + Date.now();
        guitars.unshift(guitarData);
      }

      closeModal("popup-form");
      resetForm();
      render();
    }

    function setDeleteState(id) {
      deletingId = id;
      render();
    }

    function cancelDelete() {
      deletingId = null;
      render();
    }

    function confirmDelete(id) {
      guitars = guitars.filter(g => g.id !== id);
      if (activeEditingId === id) resetForm();
      deletingId = null;
      render();
    }

    function openPhotoModal(photoUrl, title) {
      if (!photoUrl) return;
      document.getElementById("full-photo-img").src = photoUrl;
      document.getElementById("full-photo-caption").textContent = title || "";
      openModal("popup-photo");
    }

    function openModal(id) {
      document.getElementById(id).classList.add("active");
    }

    function closeModal(id) {
      document.getElementById(id).classList.remove("active");
    }

    // Inizializzazione
    render();
    checkStringChangeReminders(false);
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=900, scrolling=True)