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

      --body-bg: #f8f9fa;
      --primary: #2563eb;
      --on-primary: #ffffff;
      --primary-container: #dbeafe;
      --surface: #ffffff;
      --surface-container: #f1f5f9;
      --surface-container-high: #e2e8f0;
      --surface-container-highest: #cbd5e1;
      --on-surface-default: #0f172a;
      --on-surface-de-emphasis: #475569;
      --outline: #64748b;
      --outline-variant: #cbd5e1;
      --stroke-default: #e2e8f0;
      --negative: #dc2626;
      --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    }

    @media (prefers-color-scheme: dark) {
      :root {
        --body-bg: #0f172a;
        --surface: #1e293b;
        --surface-container: #334155;
        --surface-container-high: #475569;
        --surface-container-highest: #64748b;
        --on-surface-default: #f8fafc;
        --on-surface-de-emphasis: #cbd5e1;
        --primary: #3b82f6;
        --on-primary: #ffffff;
        --primary-container: #1e3a8a;
        --outline: #94a3b8;
        --outline-variant: #475569;
        --stroke-default: #334155;
        --negative: #ef4444;
        --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      }
    }

    :root[data-theme="dark"] {
      --body-bg: #0f172a;
      --surface: #1e293b;
      --surface-container: #334155;
      --surface-container-high: #475569;
      --surface-container-highest: #64748b;
      --on-surface-default: #f8fafc;
      --on-surface-de-emphasis: #cbd5e1;
      --primary: #3b82f6;
      --on-primary: #ffffff;
      --primary-container: #1e3a8a;
      --outline: #94a3b8;
      --outline-variant: #475569;
      --stroke-default: #334155;
      --negative: #ef4444;
      --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    body, .widget-container {
      background-color: var(--body-bg);
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: var(--ff-sans);
      color: var(--on-surface-default);
    }

    .widget-container {
      max-width: 960px;
      width: 100%;
      margin: 0 auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      border-radius: 16px;
    }

    .title {
      font-size: 26px;
      font-weight: var(--fw-semibold);
      line-height: 30px;
      margin: 0;
      color: var(--on-surface-default);
    }

    .subtitle {
      font-size: 14px;
      font-weight: var(--fw-normal);
      color: var(--on-surface-de-emphasis);
      margin: 4px 0 0 0;
    }

    .split-layout {
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }

    @media (min-width: 680px) {
      .split-layout {
        grid-template-columns: 340px 1fr;
        align-items: start;
      }
    }

    .form-panel {
      background: var(--surface);
      border: 1px solid var(--stroke-default);
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      position: sticky;
      top: 16px;
      box-shadow: var(--card-shadow);
    }

    .panel-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--stroke-default);
      padding-bottom: 12px;
    }

    .panel-title {
      font-size: 16px;
      font-weight: var(--fw-semibold);
      color: var(--on-surface-default);
      margin: 0;
    }

    .right-section {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .dashboard-hud {
      display: flex;
      background: var(--surface);
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
      width: 100%;
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
      gap: 12px;
    }

    .guitar-card {
      background: var(--surface);
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

    .guitar-card.selected {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px var(--primary-container);
    }

    .guitar-card.fade-out {
      opacity: 0;
      transform: scale(0.95);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .guitar-brand-model {
      font-size: 16px;
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
      height: 140px;
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
  </style>
</head>
<body>

  <div class="widget-container">
    <div>
      <h1 class="title">Guitar Rack</h1>
      <p class="subtitle">Gestione inventario, scalature e setup chitarre</p>
    </div>

    <div class="split-layout">
      <!-- LEFT FORM MASK PANEL -->
      <div class="form-panel" id="form-panel">
        <div class="panel-title-row">
          <h2 class="panel-title" id="form-panel-title">Nuovo Strumento</h2>
          <button class="btn-text" id="btn-reset-form" onclick="resetForm()" style="display:none;">+ Nuovo</button>
        </div>

        <div class="form-group full-width">
          <label class="form-label">Foto Strumento</label>
          <div class="guitar-photo-wrapper" id="form-photo-preview">
            <div class="photo-placeholder">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
              Nessuna foto
            </div>
          </div>
          <div style="display: flex; gap: 8px; margin-top: 4px;">
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
            <input type="text" class="input-field" id="form-brand" placeholder="es. Fender" oninput="liveUpdateForm()">
          </div>
          <div class="form-group">
            <label class="form-label">Modello *</label>
            <input type="text" class="input-field" id="form-model" placeholder="es. Stratocaster" oninput="liveUpdateForm()">
          </div>
          <div class="form-group">
            <label class="form-label">Anno</label>
            <input type="number" class="input-field mono" id="form-year" placeholder="2023" oninput="liveUpdateForm()">
          </div>
          <div class="form-group">
            <label class="form-label">Num. Serial</label>
            <input type="text" class="input-field mono" id="form-serial" placeholder="US123456" oninput="liveUpdateForm()">
          </div>
          <div class="form-group">
            <label class="form-label">Scalatura Corde</label>
            <input type="text" class="input-field mono" id="form-gauge" placeholder="0.010-0.046" oninput="liveUpdateForm()">
          </div>
          <div class="form-group">
            <label class="form-label">Ultimo Setup</label>
            <input type="date" class="input-field mono" id="form-setup" oninput="liveUpdateForm()">
          </div>
          <div class="form-group full-width">
            <label class="form-label">Note</label>
            <input type="text" class="input-field" id="form-notes" placeholder="Drop D, action bassa..." oninput="liveUpdateForm()">
          </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 4px;">
          <button class="btn-primary" id="btn-save" onclick="saveFormGuitar()">Salva in Rack</button>
          <button class="btn-text" id="btn-cancel" onclick="resetForm()" style="width:100%; text-align:center;">Pulisci Campi</button>
        </div>
      </div>

      <!-- RIGHT SECTION: STATS & GUITAR LIST -->
      <div class="right-section">
        <!-- HUD Dashboard Stats -->
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
        </div>

        <!-- Guitar List Container -->
        <div class="guitar-list" id="guitar-list-container">
          <!-- Cards injected dynamically -->
        </div>
      </div>
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
        lastSetup: "2026-05-10",
        notes: "Setup per mi standard, action bassa",
        photo: ""
      },
      {
        id: "g-2",
        brand: "PRS",
        model: "Custom 24",
        year: 2019,
        serialNumber: "19 28374",
        stringGauge: "0.010-0.046",
        lastSetup: "2026-07-02",
        notes: "10-Top acero fiammato",
        photo: ""
      },
      {
        id: "g-3",
        brand: "Gibson",
        model: "Les Paul Standard '60s",
        year: 2022,
        serialNumber: "22091004",
        stringGauge: "0.010-0.052",
        lastSetup: "2026-04-15",
        notes: "Bourbon Burst",
        photo: ""
      }
    ];

    let activeEditingId = null;
    let deletingId = null;
    let currentFormPhoto = "";

    const container = document.getElementById("guitar-list-container");
    const statTotal = document.getElementById("stat-total");
    const statCommon = document.getElementById("stat-common");
    const statSetups = document.getElementById("stat-setups");

    const formTitle = document.getElementById("form-panel-title");
    const btnResetForm = document.getElementById("btn-reset-form");
    const inputBrand = document.getElementById("form-brand");
    const inputModel = document.getElementById("form-model");
    const inputYear = document.getElementById("form-year");
    const inputSerial = document.getElementById("form-serial");
    const inputGauge = document.getElementById("form-gauge");
    const inputSetup = document.getElementById("form-setup");
    const inputNotes = document.getElementById("form-notes");
    const photoPreview = document.getElementById("form-photo-preview");
    const btnRemovePhoto = document.getElementById("btn-remove-photo");

    function updateStats() {
      statTotal.textContent = guitars.length;

      if (guitars.length === 0) {
        statCommon.textContent = "-";
        statSetups.textContent = "0";
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
    }

    function render() {
      container.innerHTML = "";

      guitars.forEach(guitar => {
        const card = document.createElement("div");
        card.className = "guitar-card" + (activeEditingId === guitar.id ? " selected" : "");
        card.setAttribute("data-id", guitar.id);

        if (deletingId === guitar.id) {
          card.innerHTML = `
            <div class="confirm-banner">
              <span class="confirm-text">Rimuovere definitivamente <strong>${guitar.brand} ${guitar.model}</strong>?</span>
              <div style="display:flex; gap:6px;">
                <button class="btn-text" onclick="event.stopPropagation(); cancelDelete()">Annulla</button>
                <button class="btn-danger" onclick="event.stopPropagation(); confirmDelete('${guitar.id}')">Rimuovi</button>
              </div>
            </div>
          `;
        } else {
          card.onclick = () => selectGuitarForEdit(guitar.id);
          card.innerHTML = `
            ${guitar.photo ? `<div class="guitar-photo-wrapper" style="margin-bottom:10px;"><img src="${guitar.photo}" class="guitar-photo" alt="${guitar.brand} ${guitar.model}" loading="lazy"></div>` : ''}
            <div class="card-header">
              <div>
                <h3 class="guitar-brand-model">${guitar.brand || 'Senza Marca'} ${guitar.model || 'Senza Modello'}</h3>
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
                <span class="info-label">Ultimo Setup</span>
                <span class="info-value mono">${guitar.lastSetup || 'N/D'}</span>
              </div>
              <div class="info-group">
                <span class="info-label">Note</span>
                <span class="info-value">${guitar.notes || '-'}</span>
              </div>
            </div>
            <div class="card-actions">
              <button class="btn-text" onclick="event.stopPropagation(); setDeleteState('${guitar.id}')">Elimina</button>
              <button class="btn-tonal" onclick="event.stopPropagation(); selectGuitarForEdit('${guitar.id}')">Modifica</button>
            </div>
          `;
        }

        container.appendChild(card);
      });

      updateStats();
    }

    function selectGuitarForEdit(id) {
      const g = guitars.find(item => item.id === id);
      if (!g) return;

      activeEditingId = id;
      deletingId = null;

      formTitle.textContent = "Modifica Strumento";
      btnResetForm.style.display = "inline-block";

      inputBrand.value = g.brand || "";
      inputModel.value = g.model || "";
      inputYear.value = g.year || "";
      inputSerial.value = g.serialNumber || "";
      inputGauge.value = g.stringGauge || "";
      inputSetup.value = g.lastSetup || "";
      inputNotes.value = g.notes || "";

      currentFormPhoto = g.photo || "";
      updatePhotoPreview();

      render();
    }

    function resetForm() {
      activeEditingId = null;
      deletingId = null;

      formTitle.textContent = "Nuovo Strumento";
      btnResetForm.style.display = "none";

      inputBrand.value = "";
      inputModel.value = "";
      inputYear.value = "";
      inputSerial.value = "";
      inputGauge.value = "";
      inputSetup.value = new Date().toISOString().split('T')[0];
      inputNotes.value = "";

      currentFormPhoto = "";
      updatePhotoPreview();

      render();
    }

    function updatePhotoPreview() {
      if (currentFormPhoto) {
        photoPreview.innerHTML = `<img src="${currentFormPhoto}" class="guitar-photo" alt="Anteprima">`;
        btnRemovePhoto.style.display = "inline-block";
      } else {
        photoPreview.innerHTML = `
          <div class="photo-placeholder">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            Nessuna foto
          </div>`;
        btnRemovePhoto.style.display = "none";
      }
    }

    window.handleFormPhotoUpload = function(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
          const canvas = document.createElement('canvas');
          const maxDim = 800;
          let width = img.width;
          let height = img.height;

          if (width > height && width > maxDim) {
            height = Math.round((height * maxDim) / width);
            width = maxDim;
          } else if (height > maxDim) {
            width = Math.round((width * maxDim) / height);
            height = maxDim;
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          currentFormPhoto = canvas.toDataURL('image/jpeg', 0.82);
          updatePhotoPreview();
          liveUpdateForm();
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    };

    window.removeFormPhoto = function() {
      currentFormPhoto = "";
      document.getElementById('form-input-photo').value = "";
      updatePhotoPreview();
      liveUpdateForm();
    };

    function liveUpdateForm() {
      if (!activeEditingId) return;

      const idx = guitars.findIndex(g => g.id === activeEditingId);
      if (idx !== -1) {
        guitars[idx].brand = inputBrand.value.trim();
        guitars[idx].model = inputModel.value.trim();
        guitars[idx].year = parseInt(inputYear.value, 10) || null;
        guitars[idx].serialNumber = inputSerial.value.trim();
        guitars[idx].stringGauge = inputGauge.value.trim();
        guitars[idx].lastSetup = inputSetup.value;
        guitars[idx].notes = inputNotes.value.trim();
        guitars[idx].photo = currentFormPhoto;
        render();
      }
    }

    function saveFormGuitar() {
      const brand = inputBrand.value.trim() || "Chitarra";
      const model = inputModel.value.trim() || "Senza Nome";

      if (activeEditingId) {
        const idx = guitars.findIndex(g => g.id === activeEditingId);
        if (idx !== -1) {
          guitars[idx] = {
            id: activeEditingId,
            brand,
            model,
            year: parseInt(inputYear.value, 10) || null,
            serialNumber: inputSerial.value.trim(),
            stringGauge: inputGauge.value.trim(),
            lastSetup: inputSetup.value,
            notes: inputNotes.value.trim(),
            photo: currentFormPhoto
          };
        }
      } else {
        const newGuitar = {
          id: "g-" + Date.now(),
          brand,
          model,
          year: parseInt(inputYear.value, 10) || null,
          serialNumber: inputSerial.value.trim(),
          stringGauge: inputGauge.value.trim(),
          lastSetup: inputSetup.value || new Date().toISOString().split('T')[0],
          notes: inputNotes.value.trim(),
          photo: currentFormPhoto
        };
        guitars.unshift(newGuitar);
      }

      resetForm();
    }

    window.setDeleteState = function(id) {
      deletingId = id;
      render();
    };

    window.cancelDelete = function() {
      deletingId = null;
      render();
    };

    window.confirmDelete = function(id) {
      const card = document.querySelector(`.guitar-card[data-id="${id}"]`);
      if (card) {
        card.classList.add("fade-out");
        setTimeout(() => {
          guitars = guitars.filter(g => g.id !== id);
          if (activeEditingId === id) resetForm();
          else { deletingId = null; render(); }
        }, 300);
      } else {
        guitars = guitars.filter(g => g.id !== id);
        if (activeEditingId === id) resetForm();
        else { deletingId = null; render(); }
      }
    };

    inputSetup.value = new Date().toISOString().split('T')[0];
    render();

    window.addEventListener('message', e => {
      if (e.data && (e.data.type === 'set-theme' || e.data.type === 'APPLY_THEME')) {
        document.documentElement.setAttribute('data-theme', e.data.theme);
      }
    });

    (function autoResize() {
      let lastHeight = 0;
      let timer = null;
      function notifyHeight() {
        const c = document.querySelector('.widget-container');
        if (!c) return;
        const h = Math.ceil(document.documentElement.scrollHeight);
        if (Math.abs(h - lastHeight) > 2) {
          lastHeight = h;
          window.parent.postMessage({type: 'widget-resize', height: h}, '*');
        }
      }
      window.addEventListener('load', () => setTimeout(notifyHeight, 120));
      new ResizeObserver(() => {
        clearTimeout(timer);
        timer = setTimeout(notifyHeight, 60);
      }).observe(document.querySelector('.widget-container'));
    })();
  </script>
</body>
</html>"""

st.components.v1.html(html_code, height=900, scrolling=True)