# slideshare_api/serializers.py

from rest_framework import serializers

class SlideShareURLSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255)
 