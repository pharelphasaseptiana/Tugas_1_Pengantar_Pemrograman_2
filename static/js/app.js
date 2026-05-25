const ICONS = {
  arithmetic: '<img class="icon-sm generated-icon generated-icon-arithmetic" src="/static/img/arithmetic_generated.png" alt="">',
  logic: '<svg class="icon-sm" viewBox="0 0 96 84" fill="none"><path d="M24 21h21c16 0 27 9 27 21S61 63 45 63H24V21Z" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/><path d="M8 31h16M8 53h16M72 42h13" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="78" cy="42" r="5" fill="white" stroke="currentColor" stroke-width="4"/></svg>',
  base: '<img class="icon-sm generated-icon generated-icon-base" src="/static/img/base_generated.png" alt="">',
  temperature: '<img class="icon-sm generated-icon generated-icon-temperature" src="/static/img/temperature_generated.png" alt="">',
  currency: '<img class="icon-sm generated-icon generated-icon-currency" src="/static/img/currency_generated.png" alt="">',
  factorial: '<svg class="icon-sm" viewBox="0 0 96 84" fill="none"><text x="20" y="60" font-size="50" font-weight="800" fill="currentColor" font-family="Arial">n!</text></svg>',
  fibonacci: '<img class="icon-sm generated-icon generated-icon-fibonacci" src="/static/img/fibonacci_generated.png" alt="">'
};

const CHEVRON = '<svg class="chevron" viewBox="0 0 24 24" fill="none"><path d="m9 6 6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';


function boolLabel(value) {
  return value ? '1 (TRUE)' : '0 (FALSE)';
}

function logicGateSvg(op, p, q, result) {
  const in1 = p ? '1' : '0';
  const in2 = q ? '1' : '0';
  const out = result ? '1' : '0';
  const bubble = ['NAND', 'NOR', 'XNOR'].includes(op) ? '<circle cx="330" cy="112" r="8" fill="#fff" stroke="#111" stroke-width="3"/>' : '';
  let gateBody = '';
  if (op === 'NOT') {
    gateBody = '<path d="M145 78 L145 146 L230 112 Z" fill="#fff" stroke="#111" stroke-width="4" stroke-linejoin="round"/>' + '<circle cx="243" cy="112" r="8" fill="#fff" stroke="#111" stroke-width="3"/>';
  } else if (op === 'AND' || op === 'NAND') {
    gateBody = '<path d="M150 62 H218 C266 62 300 84 300 112 C300 140 266 162 218 162 H150 Z" fill="#fff" stroke="#111" stroke-width="4" stroke-linejoin="round"/>' + bubble;
  } else if (op === 'OR' || op === 'NOR' || op === 'XOR' || op === 'XNOR') {
    const extra = (op === 'XOR' || op === 'XNOR') ? '<path d="M133 62 C154 82 154 142 133 162" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>' : '';
    gateBody = extra + '<path d="M146 62 C188 66 236 78 294 112 C236 146 188 158 146 162 C164 140 164 84 146 62 Z" fill="#fff" stroke="#111" stroke-width="4" stroke-linejoin="round"/>' + bubble;
  }
  const input2 = op === 'NOT' ? '' : '<line x1="86" y1="136" x2="150" y2="136" stroke="#111" stroke-width="4" stroke-linecap="round"/><text x="66" y="141" font-size="24" font-weight="700" text-anchor="middle" fill="#111">' + in2 + '</text><text x="28" y="141" font-size="13" font-weight="700" fill="#555">Q</text>';
  const outputStart = op === 'NOT' ? 251 : (['NAND','NOR','XNOR'].includes(op) ? 338 : 300);
  return `
  <svg viewBox="0 0 420 220" class="gate-svg" aria-hidden="true">
    <rect x="1.5" y="1.5" width="417" height="217" rx="14" fill="#fff" stroke="#111" stroke-width="3"/>
    <text x="24" y="28" font-size="14" font-weight="800" fill="#555">DIAGRAM GERBANG LOGIKA</text>
    <line x1="86" y1="88" x2="150" y2="88" stroke="#111" stroke-width="4" stroke-linecap="round"/>
    ${input2}
    <text x="66" y="93" font-size="24" font-weight="700" text-anchor="middle" fill="#111">${in1}</text>
    <text x="28" y="93" font-size="13" font-weight="700" fill="#555">P</text>
    ${gateBody}
    <line x1="${outputStart}" y1="112" x2="382" y2="112" stroke="#111" stroke-width="4" stroke-linecap="round"/>
    <text x="395" y="118" font-size="24" font-weight="700" fill="#111">${out}</text>
    <text x="210" y="193" font-size="24" font-weight="800" text-anchor="middle" fill="#111">${op}</text>
    <text x="337" y="193" font-size="13" font-weight="700" fill="#555">OUTPUT</text>
  </svg>`;
}

function renderLogicGate(category, payload, data) {
  const section = document.getElementById('gateSection');
  const holder = document.getElementById('gateDiagram');
  if (!section || !holder) return;
  if (category !== 'logic') {
    section.hidden = true;
    holder.innerHTML = '';
    return;
  }
  const op = String(payload.operation || 'AND').toUpperCase();
  const p = String(payload.p || 'false').toLowerCase() === 'true';
  const q = String(payload.q || 'false').toLowerCase() === 'true';
  const result = String(data.result || '').toLowerCase() === 'true';
  holder.innerHTML = logicGateSvg(op, p, q, result);
  section.hidden = false;
}

function fitReferenceLayout() {
  const designWidth = 1672;
  const baseHeight = document.body.classList.contains('calculator-view')
    ? 1120
    : (document.body.classList.contains('history-view') ? 1080 : 960);
  const shell = document.getElementById('appShell');
  let contentBottom = baseHeight;
  if (shell) {
    const children = Array.from(shell.children || []);
    for (const child of children) {
      contentBottom = Math.max(contentBottom, child.offsetTop + child.offsetHeight + 80);
    }
    shell.style.minHeight = `${contentBottom}px`;
  }
  const availableWidth = document.documentElement.clientWidth || window.innerWidth;
  const scale = Math.min(1, availableWidth / designWidth);
  document.documentElement.style.setProperty('--app-scale', scale.toFixed(6));
  document.documentElement.style.setProperty('--design-height', String(contentBottom));
  const stage = document.getElementById('fitStage');
  if (stage) stage.style.height = `${Math.ceil(contentBottom * scale)}px`;
}

window.addEventListener('resize', fitReferenceLayout);

function syncThemeToggleUi(theme) {
  const toggle = document.getElementById('themeToggle');
  if (toggle) {
    const isDark = theme === 'dark';
    toggle.setAttribute('aria-pressed', String(isDark));
    toggle.setAttribute('aria-checked', String(isDark));
    toggle.dataset.theme = theme;
  }
}

function setTheme(theme) {
  document.body.classList.toggle('theme-dark', theme === 'dark');
  localStorage.setItem('calcspace-theme', theme);
  syncThemeToggleUi(theme);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>\"]/g, char => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[char]));
}

function renderHistory(items) {
  const list = document.getElementById('historyList');
  window.CALCSPACE_HISTORY = Array.isArray(items) ? items : [];
  if (!list) return;
  if (!items || !items.length) {
    list.innerHTML = '<div class="empty-history">Belum ada riwayat perhitungan.</div>';
    return;
  }
  list.innerHTML = items.map((item, index) => `
    <button type="button" class="history-item" data-history-index="${index}">
      <span class="history-symbol">${ICONS[item.icon] || ICONS.arithmetic}</span>
      <span class="history-text"><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(item.detail)}</small></span>
      <time>${escapeHtml(item.time || '')}</time>
      ${CHEVRON}
    </button>
  `).join('');
}

function closeMenu() {
  const menu = document.getElementById('menuPopover');
  const toggle = document.getElementById('menuToggle');
  if (!menu || !toggle) return;
  menu.hidden = true;
  toggle.setAttribute('aria-expanded', 'false');
}

function toggleMenu() {
  const menu = document.getElementById('menuPopover');
  const toggle = document.getElementById('menuToggle');
  if (!menu || !toggle) return;
  const willOpen = menu.hidden;
  menu.hidden = !willOpen;
  toggle.setAttribute('aria-expanded', String(willOpen));
}

window.calcspaceToggleMenu = function(event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
    if (typeof event.stopImmediatePropagation === 'function') event.stopImmediatePropagation();
  }
  toggleMenu();
};

function showHistoryPanel() {
  const panel = document.getElementById('historyPanel');
  const unhide = document.getElementById('historyUnhide');
  panel?.classList.add('is-visible');
  if (unhide) unhide.hidden = true;
}

function hideHistoryPanel() {
  const panel = document.getElementById('historyPanel');
  const unhide = document.getElementById('historyUnhide');
  panel?.classList.remove('is-visible');
  if (unhide && !document.body.classList.contains('home-view')) unhide.hidden = false;
}

function toggleHistoryPanel() {
  const panel = document.getElementById('historyPanel');
  if (!panel) return;
  if (panel.classList.contains('is-visible')) hideHistoryPanel();
  else showHistoryPanel();
}

async function clearHistory() {
  const scope = window.CALCSPACE_HISTORY_SCOPE || 'all';
  const response = await fetch('/api/history/clear', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category: scope })
  });
  const data = await response.json();
  renderHistory(data.history);
}

function openHistoryDetail(index) {
  const items = Array.isArray(window.CALCSPACE_HISTORY) ? window.CALCSPACE_HISTORY : [];
  const item = items[index];
  if (!item) return;
  const modal = document.getElementById('historyDetailModal');
  if (!modal) return;
  document.getElementById('historyDetailTitle').textContent = item.title || 'Detail Riwayat';
  document.getElementById('historyDetailMeta').textContent = [item.detail || '', item.time || ''].filter(Boolean).join(' • ');
  document.getElementById('historyDetailResult').textContent = item.result || '-';
  document.getElementById('historyDetailFormula').textContent = item.formula || '-';
  const stepsList = document.getElementById('historyDetailSteps');
  const steps = Array.isArray(item.steps) ? item.steps : [];
  stepsList.innerHTML = steps.length ? steps.map(step => `<li>${escapeHtml(step)}</li>`).join('') : '<li>Tidak ada detail langkah.</li>';
  modal.hidden = false;
  document.body.classList.add('modal-open');
}

function closeHistoryDetail() {
  const modal = document.getElementById('historyDetailModal');
  if (!modal) return;
  modal.hidden = true;
  document.body.classList.remove('modal-open');
}

function handleGlobalMenuClick(event) {
  const toggle = event.target.closest && event.target.closest('[data-menu-toggle]');
  if (toggle) {
    window.calcspaceToggleMenu(event);
  }
}

document.addEventListener('click', handleGlobalMenuClick, true);

function bootChrome() {
  const savedTheme = localStorage.getItem('calcspace-theme');
  if (savedTheme === 'dark') setTheme('dark');
  else setTheme('light');

  document.getElementById('menuToggle')?.addEventListener('click', (event) => {
    window.calcspaceToggleMenu(event);
  });
  document.addEventListener('click', (event) => {
    const wrap = document.querySelector('.menu-wrap');
    if (wrap && !wrap.contains(event.target)) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeMenu();
      closeHistoryDetail();
    }
  });

  document.addEventListener('click', (event) => {
    const historyButton = event.target.closest('.history-item[data-history-index]');
    if (historyButton) {
      event.preventDefault();
      openHistoryDetail(Number(historyButton.dataset.historyIndex || 0));
      return;
    }
    if (event.target.closest('[data-history-detail-close]') || event.target.closest('#historyDetailClose')) {
      closeHistoryDetail();
    }
  });

  document.getElementById('themeToggle')?.addEventListener('click', () => {
    setTheme(document.body.classList.contains('theme-dark') ? 'light' : 'dark');
    closeMenu();
  });
  document.getElementById('historyPanelToggle')?.addEventListener('click', () => {
    toggleHistoryPanel();
    closeMenu();
  });
  document.getElementById('historyClose')?.addEventListener('click', hideHistoryPanel);
  document.getElementById('historyUnhide')?.addEventListener('click', showHistoryPanel);
  document.getElementById('clearHistory')?.addEventListener('click', clearHistory);
}

function formToObject(form) {
  const data = new FormData(form);
  const object = {};
  for (const [key, value] of data.entries()) {
    const field = form.elements[key];
    if (field && field.disabled) continue;
    object[key] = value;
  }
  return object;
}

function closeCustomSelects(except = null) {
  document.querySelectorAll('.custom-select.is-open').forEach((box) => {
    if (box !== except) box.classList.remove('is-open');
  });
}

function enhanceSelects(form) {
  form.querySelectorAll('select').forEach((select) => {
    select.value = '';
    const placeholder = select.dataset.placeholder || 'Pilih';
    select.classList.add('native-select-hidden');
    select.tabIndex = -1;
    select.setAttribute('aria-hidden', 'true');

    const box = document.createElement('div');
    box.className = 'custom-select';

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'custom-select-button';
    button.innerHTML = `<span>${escapeHtml(placeholder)}</span><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

    const list = document.createElement('div');
    list.className = 'custom-select-list';

    Array.from(select.options).forEach((option) => {
      if (option.value === '') return;
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'custom-select-option';
      item.textContent = option.textContent;
      item.dataset.value = option.value;
      item.addEventListener('click', () => {
        select.value = option.value;
        button.querySelector('span').textContent = option.textContent;
        box.classList.add('has-value');
        box.classList.remove('is-open');
        select.dispatchEvent(new Event('change', { bubbles: true }));
      });
      list.appendChild(item);
    });

    button.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      const willOpen = !box.classList.contains('is-open');
      closeCustomSelects(box);
      box.classList.toggle('is-open', willOpen);
    });

    box.appendChild(button);
    box.appendChild(list);
    select.insertAdjacentElement('afterend', box);
  });
}

document.addEventListener('click', () => closeCustomSelects());

function bootCalculator() {
  const form = document.getElementById('calcForm');
  if (!form) return;
  form.noValidate = true;

  form.querySelectorAll('input').forEach((input) => {
    input.value = '';
    input.setAttribute('autocomplete', 'off');
    const hint = input.getAttribute('placeholder') || '';
    input.dataset.placeholder = hint;
    input.setAttribute('placeholder', '');
    input.addEventListener('focus', () => {
      if (!input.value) input.setAttribute('placeholder', input.dataset.placeholder || '');
    });
    input.addEventListener('blur', () => {
      input.setAttribute('placeholder', '');
    });
    input.addEventListener('input', () => {
      if (input.value) input.setAttribute('placeholder', '');
      else if (document.activeElement === input) input.setAttribute('placeholder', input.dataset.placeholder || '');
    });
  });

  enhanceSelects(form);

  const arithmeticOperation = document.getElementById('arithmeticOperation');
  const secondOperand = document.getElementById('secondOperand');
  const secondOperandField = document.getElementById('secondOperandField');
  function syncSecondOperandRequirement() {
    if (!arithmeticOperation || !secondOperand || !secondOperandField) return;
    const isSquareRoot = arithmeticOperation.value === 'akar';
    secondOperand.required = !isSquareRoot;
    secondOperand.disabled = isSquareRoot;
    secondOperandField.hidden = isSquareRoot;
    secondOperandField.classList.toggle('is-hidden-field', isSquareRoot);
    if (isSquareRoot) secondOperand.value = '';
    fitReferenceLayout();
  }
  arithmeticOperation?.addEventListener('change', syncSecondOperandRequirement);
  syncSecondOperandRequirement();

  const logicOperation = document.getElementById('logicOperation');
  const logicQ = document.getElementById('logicQ');
  const logicQField = document.getElementById('logicQField');
  function syncLogicOperandRequirement() {
    if (!logicOperation || !logicQ || !logicQField) return;
    const isNot = logicOperation.value === 'NOT';
    logicQ.required = !isNot;
    logicQ.disabled = isNot;
    logicQField.hidden = isNot;
    logicQField.classList.toggle('is-hidden-field', isNot);
    if (isNot) {
      logicQ.value = '';
      const box = logicQ.nextElementSibling;
      const placeholder = logicQ.dataset.placeholder || 'Pilih nilai Q';
      if (box && box.classList.contains('custom-select')) {
        box.classList.remove('has-value', 'is-open');
        const label = box.querySelector('.custom-select-button span');
        if (label) label.textContent = placeholder;
      }
    }
    fitReferenceLayout();
  }
  logicOperation?.addEventListener('change', syncLogicOperandRequirement);
  syncLogicOperandRequirement();
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const category = form.dataset.category;
    const resultCard = document.getElementById('resultCard');
    const resultValue = document.getElementById('resultValue');
    const formulaText = document.getElementById('formulaText');
    const stepsList = document.getElementById('stepsList');

    resultValue.textContent = 'Menghitung...';
    formulaText.textContent = '';
    stepsList.innerHTML = '';
    resultCard.hidden = false;

    try {
      const response = await fetch(`/api/calculate/${category}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formToObject(form))
      });
      const data = await response.json();
      if (!data.ok) throw new Error(data.error || 'Perhitungan gagal.');
      resultValue.textContent = data.result;
      formulaText.textContent = data.formula;
      stepsList.innerHTML = data.steps.map(step => `<li>${escapeHtml(step)}</li>`).join('');
      renderHistory(data.history);
      renderLogicGate(category, formToObject(form), data);
      showHistoryPanel();
      fitReferenceLayout();
    } catch (error) {
      resultValue.textContent = 'Error';
      formulaText.textContent = error.message;
      stepsList.innerHTML = '';
      renderLogicGate('', {}, {});
      fitReferenceLayout();
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  fitReferenceLayout();
  bootChrome();
  bootCalculator();
});
