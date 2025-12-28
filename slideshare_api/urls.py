from django.urls import path
from .views import *

urlpatterns = [
    path('download-images/', DownloadImagesView.as_view(), name='download_images'),
    path('download-pdf/', DownloadPDFView.as_view(), name='download_pdf'),
    path('download-ppt/', DownloadPPTView.as_view(), name='download_ppt'),
    path('download-word/', DownloadWordView.as_view(), name='download_word')
]