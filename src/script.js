// State management
const state = {
    language: 'eng', // 'ru' or 'eng'
    color: 'black', // 'white' or 'black'
    birthYear: 2000,
    birthMonth: 1,
    birthDay: 1,
    lifeDuration: 90,
    iphoneModel: 'iphone15'
};

// DOM elements
const languageToggle = document.getElementById('language-toggle');
const colorBlack = document.getElementById('color-black');
const colorWhite = document.getElementById('color-white');
const colorLabel = document.getElementById('color-label');
const previewImage = document.getElementById('preview-image');
const generateBtn = document.getElementById('generate-btn');
const modalOverlay = document.getElementById('modal-overlay');
const modalClose = document.getElementById('modal-close');
const birthYearInput = document.getElementById('birth-year');
const birthMonthInput = document.getElementById('birth-month');
const birthDayInput = document.getElementById('birth-day');
const lifeExpectancySelect = document.getElementById('life-expectancy');
const iphoneModelSelect = document.getElementById('iphone-model');
const apiUrlInput = document.getElementById('api-url');
const copyBtn = document.getElementById('copy-btn');
const navLeft = document.getElementById('nav-left');
const navRight = document.getElementById('nav-right');
const descriptionText = document.getElementById('description-text');

// Modal text elements
const modalTitle = document.getElementById('modal-title');
const modalDescription = document.getElementById('modal-description');
const section1Title = document.getElementById('section-1-title');
const section2Title = document.getElementById('section-2-title');
const section3Title = document.getElementById('section-3-title');
const birthDateLabel = document.getElementById('birth-date-label');
const lifeExpectancyLabel = document.getElementById('life-expectancy-label');
const iphoneModelLabel = document.getElementById('iphone-model-label');
const automationInstruction = document.getElementById('automation-instruction');
const shortcutInstruction = document.getElementById('shortcut-instruction');
const action1Text = document.getElementById('action-1-text');
const action2Text = document.getElementById('action-2-text');
const importantNote = document.getElementById('important-note');

// Update preview image based on current state
function updatePreview() {
    const imageName = `img/${state.color}_${state.language}.png`;
    previewImage.src = imageName;
    previewImage.alt = `Preview ${state.color} ${state.language}`;
}

// Translations
const translations = {
    eng: {
        modalTitle: 'Life Calendar',
        modalDescription: 'Visualize your entire life in weeks. Each box represents one week of your life.',
        section1Title: 'Configure',
        section2Title: 'Create Automation',
        section3Title: 'Create Shortcut',
        birthDateLabel: 'Date of Birth',
        lifeExpectancyLabel: 'Life Expectancy',
        iphoneModelLabel: 'iPhone Model',
        automationInstruction: 'Open Shortcuts app → Automation → New → Time of Day → 6:00 AM → Repeat "Daily" → "Run Immediately" → "Create New Shortcut"',
        shortcutInstruction: 'ADD THESE ACTIONS:',
        action1Text: '3.1 "Get Contents of URL" → paste URL:',
        action2Text: '3.2 "Set Wallpaper Photo" → "Lock Screen"',
        importantNote: 'Important: In "Set Wallpaper Photo", tap arrow → disable "Crop to Subject" and "Show Preview".'
    },
    ru: {
        modalTitle: 'Календарь жизни',
        modalDescription: 'Визуализируйте всю свою жизнь по неделям. Каждый квадрат представляет одну неделю вашей жизни.',
        section1Title: 'Настройка',
        section2Title: 'Создать автоматизацию',
        section3Title: 'Создать ярлык',
        birthDateLabel: 'Дата рождения',
        lifeExpectancyLabel: 'Продолжительность жизни',
        iphoneModelLabel: 'Модель iPhone',
        automationInstruction: 'Откройте приложение Ярлыки → Автоматизация → Новый → Время дня → 6:00 → Повторять "Ежедневно" → "Запускать немедленно" → "Создать новый ярлык"',
        shortcutInstruction: 'ДОБАВЬТЕ ЭТИ ДЕЙСТВИЯ:',
        action1Text: '3.1 "Получить содержимое URL" → вставьте URL:',
        action2Text: '3.2 "Установить фото обоев" → "Экран блокировки"',
        importantNote: 'Важно: В "Установить фото обоев" нажмите стрелку → отключите "Обрезка по объекту" и "Показать предпросмотр".'
    }
};

// Update modal translations
function updateModalTranslations() {
    const t = translations[state.language];
    if (modalTitle) modalTitle.textContent = t.modalTitle;
    if (modalDescription) modalDescription.textContent = t.modalDescription;
    if (section1Title) section1Title.textContent = t.section1Title;
    if (section2Title) section2Title.textContent = t.section2Title;
    if (section3Title) section3Title.textContent = t.section3Title;
    if (birthDateLabel) birthDateLabel.textContent = t.birthDateLabel;
    if (lifeExpectancyLabel) lifeExpectancyLabel.textContent = t.lifeExpectancyLabel;
    if (iphoneModelLabel) iphoneModelLabel.textContent = t.iphoneModelLabel;
    if (automationInstruction) {
        if (state.language === 'eng') {
            automationInstruction.innerHTML = 'Open <a href="#" class="shortcuts-link">Shortcuts</a> app → Automation → New → Time of Day → 6:00 AM → Repeat "Daily" → "Run Immediately" → "Create New Shortcut"';
        } else {
            automationInstruction.innerHTML = 'Откройте приложение <a href="#" class="shortcuts-link">Ярлыки</a> → Автоматизация → Новый → Время дня → 6:00 → Повторять "Ежедневно" → "Запускать немедленно" → "Создать новый ярлык"';
        }
    }
    if (shortcutInstruction) shortcutInstruction.innerHTML = `<strong>${t.shortcutInstruction}</strong>`;
    if (action1Text) action1Text.textContent = t.action1Text;
    if (action2Text) action2Text.textContent = t.action2Text;
    if (importantNote) {
        const importantParts = t.importantNote.split(': ');
        importantNote.innerHTML = `<strong>${importantParts[0]}:</strong> ${importantParts[1]}`;
    }
    
    // Update API URL
    updateApiUrl();
}

// Update API URL based on current settings
function updateApiUrl() {
    const year = state.birthYear || 2009;
    const month = String(state.birthMonth || 8).padStart(2, '0');
    const day = String(state.birthDay || 1).padStart(2, '0');
    const birthDate = `${year}-${month}-${day}`;
    const lifeDuration = state.lifeDuration || 90;
    const url = `https://lifedie.vercel.app/api/generate?type=life&birth=${birthDate}&lifes=${lifeDuration}`;
    if (apiUrlInput) apiUrlInput.value = url;
}

// Update UI based on state
function updateUI() {
    // Update language toggle
    languageToggle.checked = state.language === 'eng';
    
    // Update color selection
    if (state.color === 'black') {
        colorBlack.classList.add('selected');
        colorWhite.classList.remove('selected');
        colorLabel.textContent = state.language === 'eng' ? 'Black wallpaper' : 'Черные обои';
    } else {
        colorWhite.classList.add('selected');
        colorBlack.classList.remove('selected');
        colorLabel.textContent = state.language === 'eng' ? 'White wallpaper' : 'Белые обои';
    }
    
    // Update button text
    const buttonText = state.language === 'eng' 
        ? `CREATE ${state.color.toUpperCase()} WALLPAPER`
        : `СОЗДАТЬ ${state.color === 'black' ? 'ЧЕРНЫЕ' : 'БЕЛЫЕ'} ОБОИ`;
    generateBtn.textContent = buttonText;
    
    // Update description text
    if (descriptionText) {
        descriptionText.textContent = state.language === 'eng'
            ? 'Create iPhone wallpapers that update every day. Track your life in weeks — from 0 to 90 years — and see how much time you still have.'
            : 'Создавайте обои для iPhone, которые обновляются каждый день. Отслеживайте свою жизнь по неделям — от 0 до 90 лет — и смотрите, сколько времени у вас еще есть.';
    }
    
    // Update modal translations
    updateModalTranslations();
    
    // Update preview
    updatePreview();
}

// Update only color-related UI (without changing language)
function updateColorOnly() {
    // Update color selection
    if (state.color === 'black') {
        colorBlack.classList.add('selected');
        colorWhite.classList.remove('selected');
        colorLabel.textContent = state.language === 'eng'
            ? 'Black wallpaper'
            : 'Черные обои';
    } else {
        colorWhite.classList.add('selected');
        colorBlack.classList.remove('selected');
        colorLabel.textContent = state.language === 'eng'
            ? 'White wallpaper'
            : 'Белые обои';
    }

    // Update button text
    generateBtn.textContent = state.language === 'eng'
        ? `CREATE ${state.color.toUpperCase()} WALLPAPER`
        : `СОЗДАТЬ ${state.color === 'black' ? 'ЧЕРНЫЕ' : 'БЕЛЫЕ'} ОБОИ`;

    // Update wrapper background
    const wrapper = document.getElementById('preview-button-wrapper');
    if (wrapper) {
        wrapper.classList.remove('color-black', 'color-white');
        wrapper.classList.add(`color-${state.color}`);
    }

    // Update button style
    generateBtn.classList.remove('color-black', 'color-white');
    generateBtn.classList.add(`color-${state.color}`);

    // Update preview
    updatePreview();
}


// Language toggle handler
languageToggle.addEventListener('change', (e) => {
    state.language = e.target.checked ? 'eng' : 'ru';
    updateUI();
});

// Color selection handlers (only change color, not language)
colorBlack.addEventListener('click', () => {
    state.color = 'black';
    updateColorOnly();
});

colorWhite.addEventListener('click', () => {
    state.color = 'white';
    updateColorOnly();
});

// Navigation arrows (cycle through previews)
// Color-only navigation (arrows + swipe)
const previewColors = ['black', 'white'];

function getColorIndex() {
    return previewColors.indexOf(state.color);
}

// ← Arrow
navLeft.addEventListener('click', () => {
    const index =
        (getColorIndex() - 1 + previewColors.length) %
        previewColors.length;

    state.color = previewColors[index];
    updateColorOnly();
});

// → Arrow
navRight.addEventListener('click', () => {
    const index =
        (getColorIndex() + 1) %
        previewColors.length;

    state.color = previewColors[index];
    updateColorOnly();
});

// Swipe support on preview
const previewArea = document.getElementById('wallpaper-preview');

let touchStartX = 0;
let touchEndX = 0;

if (previewArea) {
    previewArea.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    previewArea.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
}

function handleSwipe() {
    const threshold = 40;
    const delta = touchEndX - touchStartX;

    if (Math.abs(delta) < threshold) return;

    const index = getColorIndex();

    if (delta > 0) {
        // swipe right → previous color
        state.color =
            previewColors[(index - 1 + previewColors.length) % previewColors.length];
    } else {
        // swipe left → next color
        state.color =
            previewColors[(index + 1) % previewColors.length];
    }

    updateColorOnly();
}


// Open modal
generateBtn.addEventListener('click', () => {
    updateStateFromInputs();
    updateApiUrl();
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
});

// Close modal
modalClose.addEventListener('click', () => {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
});

// Close modal on overlay click
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Update state from inputs
function updateStateFromInputs() {
    state.birthYear = parseInt(birthYearInput.value) || 2009;
    state.birthMonth = parseInt(birthMonthInput.value) || 8;
    state.birthDay = parseInt(birthDayInput.value) || 1;
    state.lifeDuration = parseInt(lifeExpectancySelect.value) || 90;
    state.iphoneModel = iphoneModelSelect.value || 'iphone15';
    updateApiUrl();
}

// Input change handlers
if (birthYearInput) {
    birthYearInput.addEventListener('input', updateStateFromInputs);
    birthYearInput.addEventListener('change', updateStateFromInputs);
}
if (birthMonthInput) {
    birthMonthInput.addEventListener('input', updateStateFromInputs);
    birthMonthInput.addEventListener('change', updateStateFromInputs);
}
if (birthDayInput) {
    birthDayInput.addEventListener('input', updateStateFromInputs);
    birthDayInput.addEventListener('change', updateStateFromInputs);
}
if (lifeExpectancySelect) {
    lifeExpectancySelect.addEventListener('change', updateStateFromInputs);
}
if (iphoneModelSelect) {
    iphoneModelSelect.addEventListener('change', updateStateFromInputs);
}

// Copy URL button
if (copyBtn) {
    copyBtn.addEventListener('click', () => {
        if (apiUrlInput) {
            apiUrlInput.select();
            apiUrlInput.setSelectionRange(0, 99999); // For mobile devices
            navigator.clipboard.writeText(apiUrlInput.value).then(() => {
                // Visual feedback
                const originalHTML = copyBtn.innerHTML;
                copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13.5 4.5L6 12L2.5 8.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                setTimeout(() => {
                    copyBtn.innerHTML = originalHTML;
                }, 1000);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        }
    });
}

// Generate wallpaper via API
async function generateWallpaper() {
    // Just close modal - the URL is already generated and can be copied
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Set default values
if (birthYearInput) birthYearInput.value = state.birthYear;
if (birthMonthInput) birthMonthInput.value = state.birthMonth;
if (birthDayInput) birthDayInput.value = state.birthDay;
if (lifeExpectancySelect) lifeExpectancySelect.value = state.lifeDuration;
if (iphoneModelSelect) iphoneModelSelect.value = state.iphoneModel;

// Initialize UI
updateUI();
updateApiUrl();

// Set initial wrapper and button colors
const wrapper = document.getElementById('preview-button-wrapper');
if (wrapper) {
    wrapper.classList.add(`color-${state.color}`);
}
generateBtn.classList.add(`color-${state.color}`);