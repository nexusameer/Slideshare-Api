# slideshare_api/views.py
# import download.js file in the same directory here








from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideShareURLSerializer
from .slideshare_utils import download_images  # Import your function

# class SlideShareDownloadView(APIView):
#     def post(self, request):
#         # Get the URL from the request
#         serializer = SlideShareURLSerializer(data=request.data)

#         if serializer.is_valid():
#             url = serializer.validated_data['url']
#             try:
#                 # Call your function to download images and convert them to PDF
#                 download_images(url)
#                 return Response({"message": "Download and conversion successful"}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.http import HttpResponse
import os

# def download_pdf(request):
#     # Replace with the URL you want to process
#     url = request.GET.get("url")
#     if not url:
#         return HttpResponse("URL parameter is missing.", status=400)

#     try:
#         # Generate the PDF from images
#         pdf_path = download_images(url)
        
#         # Serve the PDF file
#         with open(pdf_path, 'rb') as pdf_file:
#             response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
#             return response
#     except Exception as e:
#         return HttpResponse(f"Error occurred: {e}", status=500)
    

from django.http import HttpResponse
import os

def download_pdf(request):
    # Get the URL from the request
    url = request.GET.get("url")
    if not url:
        return HttpResponse("URL parameter is missing.", status=400)

    try:
        # Generate the PDF from images (implement download_images function as per your needs)
        pdf_path = download_images(url)

        # Ensure the file exists before serving
        if os.path.exists(pdf_path):
            # Open the file in binary mode and serve it
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            
            # Clean up the generated file after serving
            os.remove(pdf_path)
            return response
        else:
            return HttpResponse("Generated PDF file not found.", status=404)

    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideShareURLSerializer
from .slideshare_utils import download_images
import base64
import os
from django.http import FileResponse

class SlideShareDownloadView(APIView):
    def post(self, request):
        serializer = SlideShareURLSerializer(data=request.data)
        
        if serializer.is_valid():
            url = serializer.validated_data['url']
            pdf_path = None
            
            try:
                # Generate PDF
                pdf_path = download_images(url)
                
                if not os.path.exists(pdf_path):
                    return Response({
                        "status": "error",
                        "message": "PDF generation failed"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Read file in chunks
                chunk_size = 8192
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
                
                # Open file and write chunks to response
                with open(pdf_path, 'rb') as pdf_file:
                    for chunk in iter(lambda: pdf_file.read(chunk_size), b''):
                        response.write(chunk)
                
                # Clean up the file after sending
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                
                return response
                
            except Exception as e:
                # Clean up in case of error
                if pdf_path and os.path.exists(pdf_path):
                    os.remove(pdf_path)
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)