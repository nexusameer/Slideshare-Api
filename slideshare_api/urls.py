# slideshare_api/urls.py
from django.urls import path
from .views import SlideShareDownloadView

urlpatterns = [
    path('download/', SlideShareDownloadView.as_view(), name='download_slideshare'),
]
