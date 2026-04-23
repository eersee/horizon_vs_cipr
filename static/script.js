let currentSlidesList = [];
let currentSlideIndex = 0;
let intervalId = null;
let isPlaying = true;
let currentSectionStart = null;

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

async function loadMainSlide() {
    const resp = await fetch('/api/slide/1');
    const data = await resp.json();
    document.getElementById('mainSlideTitle').innerText = data.title;
    const mainContent = document.getElementById('mainSlideContent');
    if (data.has_image) {
        mainContent.innerHTML = `<img src="${data.image_url}" alt="Слайд 1" style="max-width:100%; border-radius:1rem;">`;
    } else {
        mainContent.innerHTML = data.content;
    }
}

async function displaySlide(slideNum, updateCounter = true) {
    const resp = await fetch(`/api/slide/${slideNum}`);
    const data = await resp.json();
    slideTitleDiv.innerText = data.title;
    if (data.has_image) {
        slideContentDiv.innerHTML = `<img src="${data.image_url}" alt="Слайд ${slideNum}">`;
    } else {
        slideContentDiv.innerHTML = data.content;
    }
    if (updateCounter && currentSlidesList.length) {
        const idx = currentSlidesList.indexOf(slideNum);
        if (idx !== -1) slideCounterSpan.innerText = `Слайд ${idx+1} из ${currentSlidesList.length}`;
    }
}

function stopCarousel() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    isPlaying = false;
    playPauseBtn.innerText = '▶ Пуск';
}

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

async function startSection(sectionStart) {
    currentSectionStart = sectionStart;
    currentSlidesList = window.sectionsData[sectionStart];
    if (!currentSlidesList || currentSlidesList.length === 0) {
        alert('В этом разделе нет слайдов');
        return;
    }
    currentSlideIndex = 0;
    modal.style.display = 'flex';
    await displaySlide(currentSlidesList[0], true);
    if (intervalId) stopCarousel();
    startCarousel();
}

document.querySelectorAll('.tile').forEach(tile => {
    tile.addEventListener('click', () => {
        const start = parseInt(tile.getAttribute('data-section-start'));
        if (!isNaN(start)) startSection(start);
    });
});

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