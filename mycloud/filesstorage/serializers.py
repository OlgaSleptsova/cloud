from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import File



class FileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = File
        fields = ['id','user', 'name', 'file', 'uploaded_at', 'size','comment','public_link','last_downloaded']


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'user', 'name', 'size', 'uploaded_at','comment']
        read_only_fields = ['id', 'user', 'name', 'size', 'uploaded_at']
       
