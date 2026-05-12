let currentSlidesList = [];
let currentSlideIndex = 0;
let intervalId = null;
let isPlaying = true;
let currentSectionName = null;

const modal = document.getElementById('carouselModal');
const closeBtn = document.querySelector('.close');
const prevBtn = document.getElementById('prevSlideBtn');
const nextBtn = document.getElementById('nextSlideBtn');
const playPauseBtn = document.getElementById('playPauseBtn');
const slideTitleDiv = document.getElementById('carouselSlideTitle');
const slideContentDiv = document.getElementById('carouselSlideContent');
const slideCounterSpan = document.getElementById('slideCounter');

const settingsToggle = document.getElementById('settingsToggle');
const settingsPanel = document.getElementById('settingsPanel');
const intervalSlider = document.getElementById('intervalSlider');
const intervalValueSpan = document.getElementById('intervalValue');

// Загрузка главного слайда (№1) - заголовок без номера
async function loadMainSlide() {
    const resp = await fetch('/api/slide/1');
    const data = await resp.json();
    document.getElementById('mainSlideTitle').innerText = 'АО "РТ-Информационные технологии"';
    const mainContent = document.getElementById('mainSlideContent');
    if (data.has_image) {
        mainContent.innerHTML = `<img src="${data.image_url}" alt="Слайд 1" style="max-width:100%; border-radius:1rem;">`;
    } else {
        mainContent.innerHTML = data.content || '<p>Нет данных</p>';
    }
}

// Отображение слайда в модальном окне
async function displaySlide(slideNum, updateCounter = true) {
    const resp = await fetch(`/api/slide/${slideNum}`);
    const data = await resp.json();
    
    // Заголовок — только название компании, без номера слайда
    slideTitleDiv.innerText = 'АО "РТ-Информационные технологии"';
    
    if (data.has_image) {
        slideContentDiv.innerHTML = `<img src="${data.image_url}" alt="Слайд ${slideNum}">`;
    } else {
        slideContentDiv.innerHTML = data.content || '<p>Нет содержимого</p>';
    }
    
    if (updateCounter && currentSlidesList.length) {
        const idx = currentSlidesList.indexOf(slideNum);
        if (idx !== -1) {
            const sectionInfo = currentSectionName ? `Раздел: ${currentSectionName} | ` : '';
            slideCounterSpan.innerText = `${sectionInfo}Слайд ${idx+1} из ${currentSlidesList.length}`;
        }
    }
}

// Остановка автопереключения
function stopCarousel() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    isPlaying = false;
    playPauseBtn.innerText = '▶ Пуск';
}

// Запуск автопереключения
function startCarousel() {
    if (intervalId) stopCarousel();
    const intervalSec = parseFloat(intervalSlider.value);
    intervalId = setInterval(() => {
        if (!isPlaying) return;
        let nextIndex = currentSlideIndex + 1;
        if (nextIndex >= currentSlidesList.length) {
            nextIndex = 0;
        }
        currentSlideIndex = nextIndex;
        const slideNum = currentSlidesList[currentSlideIndex];
        displaySlide(slideNum, true);
    }, intervalSec * 1000);
    isPlaying = true;
    playPauseBtn.innerText = '⏸ Пауза';
}

// Запуск раздела по имени плитки
async function startSection(sectionName) {
    const slides = window.sectionsData[sectionName];
    if (!slides || slides.length === 0) {
        alert('В этом разделе нет слайдов');
        return;
    }
    currentSectionName = sectionName;
    currentSlidesList = slides;
    currentSlideIndex = 0;
    modal.style.display = 'flex';
    await displaySlide(currentSlidesList[0], true);
    if (intervalId) stopCarousel();
    startCarousel();
}

// Обработчики плиток
document.querySelectorAll('.tile').forEach(tile => {
    tile.addEventListener('click', () => {
        const sectionName = tile.getAttribute('data-section-name');
        if (sectionName && window.sectionsData[sectionName]) {
            startSection(sectionName);
        }
    });
});

// Кнопки управления каруселью
prevBtn.addEventListener('click', async () => {
    if (!currentSlidesList.length) return;
    let newIndex = currentSlideIndex - 1;
    if (newIndex < 0) newIndex = currentSlidesList.length - 1;
    currentSlideIndex = newIndex;
    await displaySlide(currentSlidesList[currentSlideIndex], true);
});

nextBtn.addEventListener('click', async () => {
    if (!currentSlidesList.length) return;
    let newIndex = currentSlideIndex + 1;
    if (newIndex >= currentSlidesList.length) newIndex = 0;
    currentSlideIndex = newIndex;
    await displaySlide(currentSlidesList[currentSlideIndex], true);
});

playPauseBtn.addEventListener('click', () => {
    if (isPlaying) {
        stopCarousel();
    } else {
        startCarousel();
    }
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    isPlaying = false;
    currentSectionName = null;
});

settingsToggle.addEventListener('click', () => {
    settingsPanel.classList.toggle('show');
});

intervalSlider.addEventListener('input', (e) => {
    intervalValueSpan.innerText = parseFloat(e.target.value).toFixed(1);
    if (modal.style.display === 'flex' && intervalId) {
        startCarousel();
    }
});

loadMainSlide();