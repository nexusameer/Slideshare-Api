from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, FileResponse
import os
from .slideshare_utils import *

class CleanupFileResponse(FileResponse):
    """Custom FileResponse that deletes the file when response is closed"""
    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.pop('file_path', None)
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
            except Exception as e:
                print(f"Error deleting file {self.file_path}: {str(e)}")

class CleanupHttpResponse(HttpResponse):
    """Custom HttpResponse that deletes files when response is closed"""
    def __init__(self, *args, **kwargs):
        self.file_paths = kwargs.pop('file_paths', [])
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()
        for path in self.file_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Error deleting file {path}: {str(e)}")

# ================== Main Views ==================
class DownloadImagesView(APIView):
    def post(self, request):
        slideshare_url = request.data.get("url")
        if not slideshare_url:
            return Response({"error": "URL parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_urls = fetch_image_urls(slideshare_url)
            if not image_urls:
                return Response({"error": "No images found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"image_urls": image_urls}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadPDFView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_paths = download_images(image_urls)
            pdf_path = convert_images_to_pdf(image_paths)
            
            file_handle = open(pdf_path, 'rb')
            response = CleanupFileResponse(
                file_handle,
                content_type='application/pdf',
                file_path=pdf_path
            )
            response['Content-Disposition'] = 'attachment; filename="slideshare.pdf"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadPPTView(APIView):
    def post(self, request):
        image_urls = request.data.get("image_urls", [])
        if not image_urls:
            return Response({"error": "No image URLs provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_paths = download_images(image_urls)
            ppt_path = convert_images_to_ppt(image_paths)
            
            file_handle = open(ppt_path, 'rb')
            response = CleanupFileResponse(
                file_handle,
                content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                file_path=ppt_path
            )
            response['Content-Disposition'] = 'attachment; filename="slideshare.pptx"'
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
            
            file_handle = open(word_path, 'rb')
            response = CleanupFileResponse(
                file_handle,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                file_path=word_path
            )
            response['Content-Disposition'] = 'attachment; filename="slideshare.docx"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)