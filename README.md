# Slideshare-Api

A Django REST API that allows users to download SlideShare presentations as images and convert them into various formats such as PDF, PowerPoint (PPTX), or Word (DOCX) documents.

## Features

- **Fetch Slides**: Extracts images from SlideShare presentation URLs.
- **Download as PDF**: Converts SlideShare images to a PDF file.
- **Download as PPTX**: Converts SlideShare images to a PowerPoint presentation.
- **Download as DOCX**: Converts SlideShare images to a Word document.
- **Compression**: Supports compressing the output files into ZIP archives.
- **REST API**: Provides endpoints for all the above features.
- **CORS enabled**: Allows cross-origin requests for easy integration with front-end applications.

## How it Works

1. **Extract Images**: The API fetches all slide images from a given SlideShare URL.
2. **Convert**: The images are converted into the desired document format (PDF, PPTX, DOCX).
3. **Download**: The converted file is served as a download via the API.

## Endpoints

- `POST /api/slideshare/pdf/` — Get a PDF from SlideShare images.
- `POST /api/slideshare/ppt/` — Get a PPTX from SlideShare images.
- `POST /api/slideshare/word/` — Get a DOCX from SlideShare images.
- `POST /api/slideshare/compressed-ppt/` — Get a compressed PPTX (ZIP).

Each endpoint expects a JSON payload:
```json
{
  "image_urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ]
}
```

## Quickstart

### Prerequisites

- Python 3.13+
- Docker (Optional, for containerized setup)

### Setup

#### With Docker

```sh
docker build -t slideshare-api .
docker run -p 8000:8000 slideshare-api
```

#### Without Docker

```sh
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Usage

Send a POST request to any API endpoint with a list of image URLs. You can fetch image URLs from a SlideShare presentation using the API's utility or by scraping manually.

Example using `curl`:
```sh
curl -X POST http://localhost:8000/api/slideshare/pdf/ \
     -H "Content-Type: application/json" \
     -d '{"image_urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]}'
```

## Project Structure

- `slideshare_api/` — Core API logic, views, and utilities.
- `slideshare_project/` — Django project settings and configuration.
- `Dockerfile` — For building Docker images.
- `requirements.txt` — Python dependencies.

## License

This project does not specify a license by default.

---

**Note:** Always respect SlideShare's Terms of Service when downloading and converting presentations.
