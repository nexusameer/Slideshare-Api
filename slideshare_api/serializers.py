from rest_framework import serializers

class SlideShareURLSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255)


class SlideShareImageSerializer(serializers.Serializer):
    image_urls = serializers.ListField(child=serializers.URLField())