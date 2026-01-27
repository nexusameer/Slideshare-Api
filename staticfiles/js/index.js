// ==================== NAVBAR FUNCTIONALITY ====================
console.log('index.js loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    const navbar = document.querySelector('.navbar');

    // Scroll effect for navbar
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('shadow');
        } else {
            navbar.classList.remove('shadow');
        }
    });

    // Active section link highlighting
    function updateActiveLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link[href^="/#"]');
        
        let currentSection = null;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.scrollY >= sectionTop - 200 && window.scrollY < sectionTop + sectionHeight - 200) {
                currentSection = section.id;
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `/#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }
    
    // Update active link on scroll
    window.addEventListener('scroll', updateActiveLink);
    window.addEventListener('load', updateActiveLink);
});

// ==================== DOWNLOAD FUNCTIONALITY ====================
console.log('Setting up download functions');

let lastImageUrls = [];
let selectedFormat = null;

// Make functions global so onclick can access them
window.startImagesDownload = startImagesDownload;
window.selectFormat = selectFormat;
window.downloadSelectedFormat = downloadSelectedFormat;

function getSelectedImages() {
    const cards = document.querySelectorAll('.slide-card.selected');
    return Array.from(cards).map(card => card.dataset.url);
}

function setError(msg) {
    const errorDiv = document.getElementById('errorMsg');
    if (msg) {
        errorDiv.innerText = msg;
        errorDiv.classList.add('show');
    } else {
        errorDiv.innerText = '';
        errorDiv.classList.remove('show');
    }
}

function showImages(urls) {
    console.log('showImages called with', urls.length, 'URLs');
    const preview = document.getElementById('imagesPreview');
    const previewSection = document.getElementById('previewSection');
    
    if (!preview) {
        console.error('imagesPreview element not found!');
        return;
    }
    if (!previewSection) {
        console.error('previewSection element not found!');
        return;
    }
    
    preview.innerHTML = '';

    if (urls.length === 0) {
        console.log('No URLs, hiding preview section');
        previewSection.classList.remove('active');
        return;
    }

    console.log('Showing preview section with active class');
    previewSection.classList.add('active');

    urls.forEach((url, idx) => {
        console.log(`Creating slide card ${idx + 1}:`, url);
        const card = document.createElement('div');
        card.className = 'slide-card selected';
        card.dataset.url = url;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'slide-checkbox';
        checkbox.checked = true;
        checkbox.addEventListener('change', (e) => {
            e.stopPropagation();
            if (checkbox.checked) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });

        const img = document.createElement('img');
        img.src = url;
        img.alt = `Slide ${idx + 1}`;
        img.loading = 'lazy';

        card.addEventListener('click', () => {
            checkbox.checked = !checkbox.checked;
            if (checkbox.checked) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });

        card.appendChild(checkbox);
        card.appendChild(img);
        preview.appendChild(card);
    });
    
    console.log('Preview section HTML:', preview.innerHTML.substring(0, 200));
}

async function startImagesDownload() {
    console.log('startImagesDownload called');
    setError('');
    showImages([]);
    const url = document.getElementById('slideshareUrl').value.trim();
    const loader = document.getElementById('customLoader');

    if (!url) {
        setError('Please enter a SlideShare URL.');
        return;
    }

    console.log('Fetching images for URL:', url);
    loader.style.display = 'flex';

    try {
        const res = await fetch('/api/slideshare/download-images/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        console.log('Response status:', res.status);
        const data = await res.json();
        console.log('Response data:', data);
        
        if (!res.ok) throw new Error(data.error || 'Failed to fetch images.');
        
        lastImageUrls = data.image_urls;
        console.log('Image URLs received:', lastImageUrls.length);
        showImages(lastImageUrls);
    } catch (e) {
        console.error('Error in startImagesDownload:', e);
        setError(e.message);
    } finally {
        loader.style.display = 'none';
    }
}

function selectFormat(format) {
    selectedFormat = format;
    
    // Update button states
    document.getElementById('btnPdf').classList.remove('active');
    document.getElementById('btnPpt').classList.remove('active');
    document.getElementById('btnWord').classList.remove('active');

    if (format === 'pdf') {
        document.getElementById('btnPdf').classList.add('active');
    } else if (format === 'ppt') {
        document.getElementById('btnPpt').classList.add('active');
    } else if (format === 'word') {
        document.getElementById('btnWord').classList.add('active');
    }
}

async function downloadSelectedFormat() {
    setError('');

    const selectedImages = getSelectedImages();

    if (!selectedImages.length) {
        setError('Please select at least one image.');
        return;
    }

    if (!selectedFormat) {
        setError('Please select a format (PDF, PPT, or Word).');
        return;
    }

    const loader = document.getElementById('customLoader');
    loader.style.display = 'flex';

    let apiPath, filename;
    if (selectedFormat === 'pdf') {
        apiPath = '/api/slideshare/download-pdf/';
        filename = 'slideshare.pdf';
    } else if (selectedFormat === 'ppt') {
        apiPath = '/api/slideshare/download-ppt/';
        filename = 'slideshare.pptx';
    } else {
        apiPath = '/api/slideshare/download-word/';
        filename = 'slideshare.docx';
    }

    try {
        const res = await fetch(apiPath, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image_urls: selectedImages })
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.error || 'Download failed.');
        }

        const blob = await res.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (e) {
        setError(e.message);
    } finally {
        loader.style.display = 'none';
    }
}
// ==================== THEME TOGGLE ====================
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        // Check for saved theme preference or default to 'dark'
        const currentTheme = localStorage.getItem('theme') || 'dark';
        
        // Apply the theme
        if (currentTheme === 'light') {
            document.body.classList.add('light-theme');
        }
        
        // Update icon based on current theme
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
        
        // Toggle theme on button click
        themeToggle.addEventListener('click', function() {
            const isLight = document.body.classList.contains('light-theme');
            
            if (isLight) {
                document.body.classList.remove('light-theme');
                localStorage.setItem('theme', 'dark');
                if (icon) icon.className = 'fas fa-sun';
            } else {
                document.body.classList.add('light-theme');
                localStorage.setItem('theme', 'light');
                if (icon) icon.className = 'fas fa-moon';
            }
        });
    }
});
