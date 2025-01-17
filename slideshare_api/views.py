# slideshare_api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideShareURLSerializer
from .slideshare_utils import download_images  # Import your function

class SlideShareDownloadView(APIView):
    def post(self, request):
        # Get the URL from the request
        serializer = SlideShareURLSerializer(data=request.data)

        if serializer.is_valid():
            url = serializer.validated_data['url']
            try:
                # Call your function to download images and convert them to PDF
                download_images(url)
                return Response({"message": "Download and conversion successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.http import HttpResponse
import os

def download_pdf(request):
    # Replace with the URL you want to process
    url = request.GET.get("url")
    if not url:
        return HttpResponse("URL parameter is missing.", status=400)

    try:
        # Generate the PDF from images
        pdf_path = download_images(url)
        
        # Serve the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            return response
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)

