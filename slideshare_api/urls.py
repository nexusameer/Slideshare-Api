# slideshare_api/urls.py
from django.urls import path
from .views import SlideShareDownloadView
from . import views

urlpatterns = [
    path('download/', SlideShareDownloadView.as_view(), name='download_slideshare'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]
