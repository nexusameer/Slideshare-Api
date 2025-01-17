# slideshare_api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideShareURLSerializer
from .slideshare_utils import download_images
import os
from django.http import HttpResponse

class SlideShareDownloadView(APIView):
    def post(self, request):
        # Get the URL from the request
        serializer = SlideShareURLSerializer(data=request.data)

        if serializer.is_valid():
            url = serializer.validated_data['url']
            try:
                # Call your function to download images and convert them to PDF
                pdf_path = download_images(url)

                # Ensure the generated PDF exists
                if not os.path.exists(pdf_path):
                    return Response({"error": "Generated PDF file not found."}, status=status.HTTP_404_NOT_FOUND)

                # Serve the PDF file for download
                with open(pdf_path, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'

                # Cleanup the PDF file after serving
                os.remove(pdf_path)

                return response

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
