// State management
const state = {
    language: 'ru', // 'ru' or 'eng' - Russian by default
    color: 'black', // 'gray' or 'black'
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
const iphoneModelSelect = document.getElementById('iphone-model');
const apiUrlInput = document.getElementById('api-url');
const copyBtn = document.getElementById('copy-btn');
const navLeft = document.getElementById('nav-left');
const navRight = document.getElementById('nav-right');
const descriptionText = document.getElementById('description-text');

// Modal text elements
const modalTitle = document.getElementById('modal-title');
const instructionsTitle = document.getElementById('instructions-title');
const instructionsSubtitle = document.getElementById('instructions-subtitle');
const section1Title = document.getElementById('section-1-title');
const section2Title = document.getElementById('section-2-title');
const section3Title = document.getElementById('section-3-title');
const section4Title = document.getElementById('section-4-title');
const section5Title = document.getElementById('section-5-title');
const section6Title = document.getElementById('section-6-title');
const section7Title = document.getElementById('section-7-title');
const birthDateLabel = document.getElementById('birth-date-label');
const iphoneModelLabel = document.getElementById('iphone-model-label');
const urlLabel = document.getElementById('url-label');
const step1Text = document.getElementById('step-1-text');
const step1App = document.getElementById('step-1-app');
const step2Text = document.getElementById('step-2-text');
const step3Text = document.getElementById('step-3-text');
const step4Action = document.getElementById('step-4-action');
const step5Text = document.getElementById('step-5-text');
const step5Text2 = document.getElementById('step-5-text-2');
const step6Text = document.getElementById('step-6-text');
const step6Text2 = document.getElementById('step-6-text-2');
const step7Text = document.getElementById('step-7-text');
const step7Text2 = document.getElementById('step-7-text-2');
const tipTitle = document.getElementById('tip-title');
const tipText = document.getElementById('tip-text');
// Info block elements
const step4Time = document.getElementById('step-4-time');
const step4Repeat = document.getElementById('step-4-repeat');
const step4Run = document.getElementById('step-4-run');
const step6Image = document.getElementById('step-6-image');
const step6Screen = document.getElementById('step-6-screen');
const step6Preview = document.getElementById('step-6-preview');
const step6Crop = document.getElementById('step-6-crop');
const yearLabel = document.getElementById('year-label');
const monthLabel = document.getElementById('month-label');
const dayLabel = document.getElementById('day-label');
const dateError = document.getElementById('date-error');

// Update preview image based on current state
function updatePreview() {
    const imageName = `img/${state.color}_${state.language}.png`;
    previewImage.src = imageName;
    previewImage.alt = `Preview ${state.color} ${state.language}`;
}

// Translations
const translations = {
    eng: {
        modalTitle: '0-90 calendar',
        instructionsTitle: 'Auto-update wallpapers',
        instructionsSubtitle: 'Set up automation so wallpapers update every week',
        section1Title: '1. Open "Shortcuts" app',
        section2Title: '2. Go to "Automation"',
        section3Title: '3. Create new automation',
        section4Title: '4. Set schedule',
        section5Title: '5. Add download action',
        section6Title: '6. Add wallpaper setup',
        section7Title: '7. Save',
        birthDateLabel: 'Date of Birth',
        iphoneModelLabel: 'iPhone Model',
        urlLabel: 'Link for automation',
        yearLabel: 'Year',
        monthLabel: 'Month',
        dayLabel: 'Day',
        dateErrorInvalid: 'Invalid date',
        dateErrorFuture: 'Date cannot be in the future',
        step1Text: 'This is a built-in Apple app. If you can\'t find it — swipe down on the home screen and type <span class="highlight">Shortcuts</span>',
        step1App: 'Find the <strong>"Shortcuts"</strong> app',
        step2Text: 'At the bottom of the screen there\'s an <span class="highlight">Automation</span> tab — tap on it',
        step3Text: 'Tap <span class="highlight">+</span> in the top right corner, then select <span class="highlight">Time of Day</span>',
        step4Action: 'Tap <span class="highlight">Next</span>, new automation',
        step4Time: 'Time: <strong>any convenient</strong> (e.g., 7:00)',
        step4Repeat: 'Repeat: <strong>By day</strong>',
        step4Run: 'Run: <strong>Immediately</strong>',
        step5Text: 'In the search type <span class="highlight">Get Contents of URL</span>',
        step5Text2: 'In the URL field paste the link (link above)',
        step6Text: 'In the search type <span class="highlight">wallpaper</span> and select <span class="highlight">Set Wallpaper</span>',
        step6Text2: 'Tap the arrow in circle and disable:',
        step6Image: 'Image: <strong>Contents of URL</strong> (will be set automatically)',
        step6Screen: 'Screen: select <strong>Lock Screen</strong>',
        step6Preview: '<strong>Show preview</strong> — disable',
        step6Crop: '<strong>Crop to theme</strong> — disable',
        step7Text: 'Tap <span class="highlight">Done</span>',
        step7Text2: 'Important: change <span class="highlight">Run after confirmation</span> to <span class="highlight">Run immediately</span>',
        tipTitle: '💡 Tip',
        tipText: 'To check everything works — in the automations list tap on the created one and select <strong>Run</strong>. Wallpapers should update immediately.'
    },
    ru: {
        modalTitle: '0-90 календарь',
        instructionsTitle: 'Автообновление обоев',
        instructionsSubtitle: 'Настрой автоматизацию, чтобы обои обновлялись каждую неделю',
        section1Title: '1. Открой приложение «Команды»',
        section2Title: '2. Перейди в «Автоматизация»',
        section3Title: '3. Создай новую автоматизацию',
        section4Title: '4. Настрой расписание',
        section5Title: '5. Добавь действие загрузки',
        section6Title: '6. Добавь установку обоев',
        section7Title: '7. Сохрани',
        birthDateLabel: 'Дата рождения',
        iphoneModelLabel: 'Модель iPhone',
        urlLabel: 'Ссылка для автоматизации',
        yearLabel: 'Год',
        monthLabel: 'Месяц',
        dayLabel: 'День',
        dateErrorInvalid: 'Неверная дата',
        dateErrorFuture: 'Дата не может быть в будущем',
        step1Text: 'Это встроенное приложение Apple. Если не можешь найти — потяни вниз на домашнем экране и напиши <span class="highlight">Команды</span>',
        step1App: 'Найди приложение <strong>«Команды»</strong> (Shortcuts)',
        step2Text: 'Внизу экрана есть вкладка <span class="highlight">Автоматизация</span> — нажми на неё',
        step3Text: 'Нажми <span class="highlight">+</span> в правом верхнем углу, затем выбери <span class="highlight">Время суток</span>',
        step4Action: 'Нажми <span class="highlight">Далее</span>, новая автоматизация',
        step4Time: 'Время: <strong>любое удобное</strong> (например, 7:00)',
        step4Repeat: 'Повтор: <strong>По дням</strong>',
        step4Run: 'Запуск: <strong>Немедленный запуск</strong>',
        step5Text: 'В поиске введите <span class="highlight">Получить содержимое URL</span>',
        step5Text2: 'В поле URL адрес вставьте ссылку (ссылка выше)',
        step6Text: 'В поиске напиши <span class="highlight">обои</span> и выбери <span class="highlight">Задать обои</span>',
        step6Text2: 'Нажми на стрелочку в кружке и отключи:',
        step6Image: 'Изображение: <strong>Содержимое URL</strong> (подставится автоматически)',
        step6Screen: 'Экран: выбери <strong>Экран блокировки</strong>',
        step6Preview: '<strong>Показать окно просмотра</strong> — отключи',
        step6Crop: '<strong>Обрезать до темы</strong> — отключи',
        step7Text: 'Нажми <span class="highlight">Готово</span>',
        step7Text2: 'Важно: измени <span class="highlight">Запуск после подтверждения</span> на <span class="highlight">Немедленный запуск</span>',
        tipTitle: '💡 Совет',
        tipText: 'Чтобы проверить, что всё работает — в списке автоматизаций нажми на созданную и выбери <strong>Выполнить</strong>. Обои должны сразу обновиться.'
    }
};

// Update modal translations
function updateModalTranslations() {
    const t = translations[state.language];
    if (modalTitle) modalTitle.textContent = t.modalTitle;
    if (instructionsTitle) instructionsTitle.textContent = t.instructionsTitle;
    if (instructionsSubtitle) instructionsSubtitle.textContent = t.instructionsSubtitle;
    if (section1Title) section1Title.textContent = t.section1Title;
    if (section2Title) section2Title.textContent = t.section2Title;
    if (section3Title) section3Title.textContent = t.section3Title;
    if (section4Title) section4Title.textContent = t.section4Title;
    if (section5Title) section5Title.textContent = t.section5Title;
    if (section6Title) section6Title.textContent = t.section6Title;
    if (section7Title) section7Title.textContent = t.section7Title;
    if (birthDateLabel) birthDateLabel.textContent = t.birthDateLabel;
    if (iphoneModelLabel) iphoneModelLabel.textContent = t.iphoneModelLabel;
    if (urlLabel) urlLabel.textContent = t.urlLabel;
    if (yearLabel) yearLabel.textContent = t.yearLabel;
    if (monthLabel) monthLabel.textContent = t.monthLabel;
    if (dayLabel) dayLabel.textContent = t.dayLabel;

    // Update step texts
    if (step1Text) step1Text.innerHTML = t.step1Text;
    if (step1App) step1App.innerHTML = t.step1App;
    if (step2Text) step2Text.innerHTML = t.step2Text;
    if (step3Text) step3Text.innerHTML = t.step3Text;
    if (step4Action) step4Action.innerHTML = t.step4Action;
    if (step5Text) step5Text.innerHTML = t.step5Text;
    if (step5Text2) step5Text2.innerHTML = t.step5Text2;
    if (step6Text) step6Text.innerHTML = t.step6Text;
    if (step6Text2) step6Text2.innerHTML = t.step6Text2;
    if (step7Text) step7Text.innerHTML = t.step7Text;
    if (step7Text2) step7Text2.innerHTML = t.step7Text2;
    if (tipTitle) tipTitle.textContent = t.tipTitle;
    if (tipText) tipText.innerHTML = t.tipText;

    // Update info block texts
    if (step4Time) step4Time.innerHTML = t.step4Time;
    if (step4Repeat) step4Repeat.innerHTML = t.step4Repeat;
    if (step4Run) step4Run.innerHTML = t.step4Run;
    if (step6Image) step6Image.innerHTML = t.step6Image;
    if (step6Screen) step6Screen.innerHTML = t.step6Screen;
    if (step6Preview) step6Preview.innerHTML = t.step6Preview;
    if (step6Crop) step6Crop.innerHTML = t.step6Crop;

    // Update API URL
    updateApiUrl();
}

// iPhone screen resolutions
const iphoneResolutions = {
    iphone13mini: { w: 1080, h: 2340 },
    iphone13: { w: 1170, h: 2532 },
    iphone13promax: { w: 1284, h: 2778 },
    iphone15: { w: 1179, h: 2556 },
    iphone15plus: { w: 1290, h: 2796 },
    iphone16pro: { w: 1206, h: 2622 },
    iphone16promax: { w: 1320, h: 2868 },
    iphone17: { w: 1179, h: 2556 },
    iphone17pro: { w: 1206, h: 2622 },
    iphone17promax: { w: 1320, h: 2868 }
};

// Update API URL based on current settings
function updateApiUrl() {
    const year = state.birthYear || 2009;
    const month = String(state.birthMonth || 8).padStart(2, '0');
    const day = String(state.birthDay || 1).padStart(2, '0');

    const birthDate = `${year}-${month}-${day}`;
    const lifespan = state.lifeDuration || 90;

    const model = state.iphoneModel || 'iphone15';
    const resolution = iphoneResolutions[model];

    const theme = state.color;      // black | gray
    const lang = state.language;    // eng | ru

    const baseUrl = window.location.origin;

    const url =
        `${baseUrl}/api/cal` +
        `?type=life` +
        `&theme=${theme}` +
        `&lang=${lang}` +
        `&birth=${birthDate}` +
        `&lifespan=${lifespan}` +
        `&w=${resolution.w}` +
        `&h=${resolution.h}` +
        `&fs=60`;

    apiUrlInput.value = url;
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
        colorLabel.textContent = state.language === 'eng' ? 'Gray wallpaper' : 'Серые обои';
    }
    
    // Update button text
    const buttonText = state.language === 'eng' 
        ? `CREATE ${state.color.toUpperCase()} WALLPAPER`
        : `СОЗДАТЬ ${state.color === 'black' ? 'ЧЕРНЫЕ' : 'СЕРЫЕ'} ОБОИ`;
    generateBtn.textContent = buttonText;
    
    // Update description text
    if (descriptionText) {
        descriptionText.innerHTML = state.language === 'eng'
        ? 'Create iPhone wallpapers that update every day. Track your life in weeks — from 0 to 90 years —<br>and see how much time you still have.'
        : 'Создавайте обои для iPhone, которые обновляются каждый день. Отслеживайте свою жизнь по неделям — от 0 до 90 лет —<br>и смотрите, сколько времени <br> у вас еще есть.';
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
            ? 'Gray wallpaper'
            : 'Серые обои';
    }

    // Update button text
    generateBtn.textContent = state.language === 'eng'
        ? `CREATE ${state.color.toUpperCase()} WALLPAPER`
        : `СОЗДАТЬ ${state.color === 'black' ? 'ЧЕРНЫЕ' : 'СЕРЫЕ'} ОБОИ`;

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
    state.color = 'gray';
    updateColorOnly();
});

// Navigation arrows (cycle through previews)
// Color-only navigation (arrows + swipe)
const previewColors = ['black', 'gray'];

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

// Validate date
function validateDate() {
    const year = parseInt(birthYearInput.value);
    const month = parseInt(birthMonthInput.value);
    const day = parseInt(birthDayInput.value);

    if (!year || !month || !day) {
        return true; // Allow empty fields
    }

    // Check valid ranges
    if (year < 1900 || year > 2100 || month < 1 || month > 12 || day < 1 || day > 31) {
        showDateError('dateErrorInvalid');
        return false;
    }

    // Check if date is valid
    const date = new Date(year, month - 1, day);
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
        showDateError('dateErrorInvalid');
        return false;
    }

    // Check if date is not in the future
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (date > today) {
        showDateError('dateErrorFuture');
        return false;
    }

    hideDateError();
    return true;
}

function showDateError(messageKey) {
    if (dateError) {
        const t = translations[state.language];
        dateError.textContent = t[messageKey];
        dateError.style.display = 'block';
    }
}

function hideDateError() {
    if (dateError) {
        dateError.style.display = 'none';
    }
}

// Update state from inputs
function updateStateFromInputs() {
    if (!validateDate()) {
        return; // Don't update if date is invalid
    }

    state.birthYear = parseInt(birthYearInput.value) || 2009;
    state.birthMonth = parseInt(birthMonthInput.value) || 8;
    state.birthDay = parseInt(birthDayInput.value) || 1;
    state.lifeDuration = 90; // Fixed value
    state.iphoneModel = iphoneModelSelect.value || 'iphone15';
    updateApiUrl();
}

// Input change handlers with validation
if (birthYearInput) {
    birthYearInput.addEventListener('input', () => {
        validateDate();
        updateStateFromInputs();
    });
    birthYearInput.addEventListener('change', () => {
        validateDate();
        updateStateFromInputs();
    });
}
if (birthMonthInput) {
    birthMonthInput.addEventListener('input', () => {
        validateDate();
        updateStateFromInputs();
    });
    birthMonthInput.addEventListener('change', () => {
        validateDate();
        updateStateFromInputs();
    });
}
if (birthDayInput) {
    birthDayInput.addEventListener('input', () => {
        validateDate();
        updateStateFromInputs();
    });
    birthDayInput.addEventListener('change', () => {
        validateDate();
        updateStateFromInputs();
    });
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
