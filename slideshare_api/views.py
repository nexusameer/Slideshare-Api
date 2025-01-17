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
            try:
                # Generate PDF
                pdf_path = download_images(url)
                
                if not os.path.exists(pdf_path):
                    return Response({
                        "status": "error",
                        "message": "PDF generation failed"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Open the file and create a FileResponse
                pdf_file = open(pdf_path, 'rb')
                response = FileResponse(
                    pdf_file,
                    content_type='application/pdf',
                    as_attachment=True,
                    filename=os.path.basename(pdf_path)
                )
                
                # Add header to force download
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
                
                # File will be deleted after response is sent
                def delete_file_after_response():
                    pdf_file.close()
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                
                response.close = delete_file_after_response
                
                return response
                
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)