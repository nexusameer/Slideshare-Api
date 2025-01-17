# slideshare_api/slideshare_utils.py

import os
import re
import requests 
from bs4 import BeautifulSoup
import img2pdf
from time import localtime, strftime
from os import walk
from django.http import HttpResponse
import os

from os.path import join

CURRENT = os.path.dirname(__file__)

def download_images(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    
    title = "".join(
        (CURRENT + "/pdf_images", strftime("/%Y%m%d_%H%M%S", localtime()))
    )  # temp img dir

    images = soup.find_all("img", {"data-testid": "vertical-slide-image"})
    image_url = ""

    for image in images:
        image_url = image.get("srcset").split("w, ")[-1].split(" ")[0]
        if image_url.endswith(".jpg"):
            break

    i = 1
    image_url_prefix = image_url.rstrip("-2048.jpg")
    image_url_prefix = image_url_prefix.rstrip("0123456789")  # remove last slide id
    image_url_prefix = image_url_prefix.rstrip("-")  # remove last -
    pdf_f = re.sub(
        "[^0-9a-zA-Z]+", "_", image_url_prefix.split("/")[-1]
    )  # Get pdf name from URL image
    pdf_f += ".pdf"
    
    print("1. Download Images:")
    for image in images:
        image_url = image_url_prefix + "-" + str(i) + "-2048.jpg"
        print(f"Downloading {image_url}")
        r = requests.get(image_url)

        if not os.path.exists(title):
            os.makedirs(title)

        filename = str(i) + ".jpg"
        i += 1

        with open(title + "/" + filename, "wb") as f:
            f.write(r.content)

    # Convert images to PDF
    pdf_path = convert_pdf(title, pdf_f)
    return pdf_path

def convert_pdf(img_dir_name, pdf_f):
    f = []
    for dirpath, dirnames, filenames in walk(join(CURRENT, img_dir_name)):
        f.extend(filenames)
        break
    f = ["%s/%s" % (img_dir_name, x) for x in f]

    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [atoi(c) for c in re.split(r"(\d+)", text)]

    f.sort(key=natural_keys)

    print("\n2. Convert Images to PDF")
    print(f)

    pdf_path = join(CURRENT, pdf_f)
    pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
    with open(pdf_path, "wb") as doc:
        doc.write(pdf_bytes)

    print(f"\n3. Done: {pdf_path}")

    # Delete images after conversion
    # delete_images(img_dir_name)
    download_pdf(pdf_path)
    return pdf_path


def delete_images(img_dir_name):
    # Delete all files in the directory after conversion to PDF
    for dirpath, dirnames, filenames in walk(join(CURRENT, img_dir_name)):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        break
    os.rmdir(img_dir_name)  # Remove the empty directory
    print(f"Deleted the directory: {img_dir_name}")


def download_pdf(request):
    # Get the URL from the request
    url = request.GET.get("url")
    if not url:
        return HttpResponse("URL parameter is missing.", status=400)

    try:
        # Generate the PDF from images
        pdf_path = download_images(url)

        # Ensure the file exists before serving
        if not os.path.exists(pdf_path):
            return HttpResponse("Generated PDF file not found.", status=404)

        # Serve the PDF
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
        
        # Cleanup after serving the response
        os.remove(pdf_path)
        return response

    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)
