let lastImageUrls = [];
function setError(msg) {
    const errorDiv = document.getElementById('errorMsg');
    if (msg) {
        errorDiv.innerText = msg;
        errorDiv.classList.remove('d-none');
    } else {
        errorDiv.innerText = '';
        errorDiv.classList.add('d-none');
    }
}
function showImages(urls) {
    const preview = document.getElementById('imagesPreview');
    preview.innerHTML = '';
    if (urls.length === 0) {
        preview.style.display = 'none';
        return;
    }
    preview.style.display = 'block';
    const row = document.createElement('div');
    row.className = 'row g-3';
    urls.forEach((url, idx) => {
        const col = document.createElement('div');
        col.className = 'col-12 col-md-6';
        const card = document.createElement('div');
        card.className = 'card h-100';
        card.style.padding = '10px';
        card.style.display = 'flex';
        card.style.alignItems = 'center';
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = url;
        checkbox.checked = true;
        checkbox.className = 'form-check-input image-checkbox me-2';
        checkbox.style.marginRight = '8px';
        const img = document.createElement('img');
        img.src = url;
        img.className = 'img-fluid rounded';
        img.alt = 'Slide preview';
        img.style.maxHeight = '250px';
        card.appendChild(checkbox);
        card.appendChild(img);
        col.appendChild(card);
        row.appendChild(col);
    });
    preview.appendChild(row);
}
async function downloadImages() {
    setError('');
    showImages([]);
    const url = document.getElementById('slideshareUrl').value.trim();
    const loader = document.getElementById('customLoader');
    loader.style.display = 'flex';
    if (!url) { setError('Please enter a SlideShare URL.'); loader.style.display = 'none'; return; }
    try {
        const res = await fetch('/api/slideshare/download-images/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to fetch images.');
        lastImageUrls = data.image_urls;
        showImages(lastImageUrls);
    } catch (e) {
        setError(e.message);
    } finally {
        loader.style.display = 'none';
    }
}
function getSelectedImages() {
    const checkboxes = document.querySelectorAll('.image-checkbox');
    return Array.from(checkboxes).filter(cb => cb.checked).map(cb => cb.value);
}
async function downloadFile(apiPath, filename) {
    setError('');
    if (!lastImageUrls.length) { setError('Please download images first.'); return; }
    const selectedImages = getSelectedImages();
    if (!selectedImages.length) { setError('Please select at least one image.'); return; }
    const loader = document.getElementById('customLoader');
    loader.style.display = 'flex';
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
function downloadPDF() {
    downloadFile('/api/slideshare/download-pdf/', 'slideshare.pdf');
}
function downloadPPT() {
    downloadFile('/api/slideshare/download-ppt/', 'slideshare.pptx');
}
function downloadWord() {
    downloadFile('/api/slideshare/download-word/', 'slideshare.docx');
}
function downloadCompressedPDF() {
    downloadFile('/api/slideshare/download-compressed-pdf/', 'slideshare_compressed.pdf');
}
function downloadCompressedPPT() {
    downloadFile('/api/slideshare/download-compressed-ppt/', 'slideshare_compressed.pptx');
}
function downloadCompressedWord() {
    downloadFile('/api/slideshare/download-compressed-word/', 'slideshare_compressed.docx');
}
