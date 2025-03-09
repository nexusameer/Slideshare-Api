from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, FileResponse
import os
import tempfile
from .slideshare_utils import *

class DownloadImagesView(APIView):
    def post(self, request):
        slideshare_url = request.data.get("url")
        if not slideshare_url:
            return Response({"error": "URL parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_urls = fetch_image_urls(slideshare_url)
            if not image_urls:
                return Response({"error": "No images found in the SlideShare URL."}, status=status.HTTP_404_NOT_FOUND)

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

            # Open the file and keep it open until the response is sent
            pdf_file = open(pdf_path, 'rb')
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="output.pdf"'

            # Use a callback to clean up the file after the response is sent
            response.closed.connect(lambda: os.remove(pdf_path))
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

            # Open the file and keep it open until the response is sent
            ppt_file = open(ppt_path, 'rb')
            response = HttpResponse(ppt_file, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            response['Content-Disposition'] = 'attachment; filename="output.pptx"'

            # Use a callback to clean up the file after the response is sent
            response.closed.connect(lambda: os.remove(ppt_path))
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DownloadWordView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_paths = download_images(image_urls)
            word_path = convert_images_to_word(image_paths)

            with open(word_path, 'rb') as word_file:
                response = HttpResponse(word_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="output.docx"'

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
            image_paths = download_images(image_urls)
            pdf_path = convert_images_to_pdf(image_paths)
            zip_path = compress_file(pdf_path)

            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="output.pdf.zip"'

            os.remove(zip_path)
            os.remove(pdf_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadCompressedPPTView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_paths = download_images(image_urls)
            ppt_path = convert_images_to_ppt(image_paths)
            zip_path = compress_file(ppt_path)

            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="output.pptx.zip"'

            os.remove(zip_path)
            os.remove(ppt_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadCompressedWordView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_paths = download_images(image_urls)
            word_path = convert_images_to_word(image_paths)
            zip_path = compress_file(word_path)

            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="output.docx.zip"'

            os.remove(zip_path)
            os.remove(word_path)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)