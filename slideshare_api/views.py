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
