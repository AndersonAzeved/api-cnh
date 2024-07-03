from rest_framework import serializers
from .models import File

class FileSerializers(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = ['id','file','file_name']
        
    def get_file_name(self, obj):
        return obj.file.name
    