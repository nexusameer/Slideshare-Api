# slideshare_api/serializers.py

from rest_framework import serializers # type: ignore

class SlideShareURLSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255)
