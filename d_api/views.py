# slideshare_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideShareURLSerializer
from .utils import download_and_convert  # Assuming you have this function

class SlideShareDownloadView(APIView):
    def post(self, request):
        serializer = SlideShareURLSerializer(data=request.data)
        
        if serializer.is_valid():
            url = serializer.validated_data['url']
            
            try:
                # Call your download_and_convert function here
                result = download_and_convert(url)
                
                # Return a successful response
                return Response({"message": "Download and conversion successful", "data": result}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
