# slideshare_api/slideshare_utils.py

import os
import re
import requests 
from bs4 import BeautifulSoup
import img2pdf
from time import localtime, strftime
from os import walk
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

    convert_pdf(title, pdf_f)

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

    pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
    doc = open(pdf_f, "wb")
    doc.write(pdf_bytes)
    doc.close()

    print(f"\n3. Done: {pdf_f}")

    # Delete images after conversion
    delete_images(img_dir_name)

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
