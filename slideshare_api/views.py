from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import os
from django.http import FileResponse
from .slideshare_utils import *


class DownloadImagesView(APIView):
    def post(self, request):
        slideshare_url = request.data.get("url")
        if not slideshare_url:
            return Response({"error": "URL parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch image URLs
            image_urls = fetch_image_urls(slideshare_url)
            if not image_urls:
                return Response({"error": "No images found in the SlideShare URL."}, status=status.HTTP_404_NOT_FOUND)

            # Return image URLs
            return Response({"image_urls": image_urls}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadPDFView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download images and convert to PDF
            image_paths = download_images(image_urls)
            pdf_path = convert_images_to_pdf(image_paths)

            # Serve the PDF for download
            response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="output.pdf"'

            # Cleanup the temporary PDF file
            os.remove(pdf_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DownloadPPTView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download images and convert to PPT
            image_paths = download_images(image_urls)
            ppt_path = convert_images_to_ppt(image_paths)

            # Serve the PPT for download
            with open(ppt_path, 'rb') as ppt_file:
                response = HttpResponse(ppt_file.read(), content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                response['Content-Disposition'] = 'attachment; filename="output.pptx"'

            # Cleanup the temporary PPT file
            os.remove(ppt_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadWordView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download images and convert to Word
            image_paths = download_images(image_urls)
            word_path = convert_images_to_word(image_paths)

            # Serve the Word document for download
            with open(word_path, 'rb') as word_file:
                response = HttpResponse(word_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="output.docx"'

            # Cleanup the temporary Word file
            os.remove(word_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadCompressedPDFView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download images and convert to PDF
            image_paths = download_images(image_urls)
            pdf_path = convert_images_to_pdf(image_paths)

            # Compress the PDF
            zip_path = compress_file(pdf_path)

            # Serve the compressed PDF for download
            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="output.pdf.zip"'

            # Cleanup the temporary ZIP file
            os.remove(zip_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadCompressedPPTView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download images and convert to PPT
            image_paths = download_images(image_urls)
            ppt_path = convert_images_to_ppt(image_paths)

            # Compress the PPT
            zip_path = compress_file(ppt_path)

            # Serve the compressed PPT for download
            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="output.pptx.zip"'

            # Cleanup the temporary ZIP file
            os.remove(zip_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadCompressedWordView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download images and convert to Word
            image_paths = download_images(image_urls)
            word_path = convert_images_to_word(image_paths)

            # Compress the Word document
            zip_path = compress_file(word_path)

            # Serve the compressed Word document for download
            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="output.docx.zip"'

            # Cleanup the temporary ZIP file
            os.remove(zip_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)