from django.shortcuts import render
from rest_framework import generics, status, response
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializers
from .functions import extractCnhToImage

class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializers
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_instance = serializer.save()
        cnh = extractCnhToImage(file_instance.file.name)
        return Response(
            {"response": cnh},
            status=status.HTTP_201_CREATED,
        )