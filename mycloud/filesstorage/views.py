from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from adminmodul.permissions import IsOwner
from django.contrib.auth.models import User

from adminmodul.serializers import PersonsFilesSerializer
from adminmodul.models import PathPerson

from .serializers import FileSerializer, FileUploadSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import File
from django.shortcuts import render, redirect

from .forms import FileUploadForm
from rest_framework import status,permissions
from rest_framework.decorators import api_view
from venv import logger
from rest_framework.parsers import MultiPartParser, FormParser

import uuid

class FilesViewSet(ModelViewSet):
    queryset=File.objects.all()
    serializer_class= FileSerializer


#список файлов
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request,path=None):
    try:
        if request.user.is_staff:
            user=PathPerson.objects.get(path=f"/{path}/")
            files = File.objects.filter(user=user.userpath)

        else:
            files = File.objects.filter(user=request.user)
        if len(files)>0:
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response("файлы отсутствуют")

    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Произошла ошибка при получении файлов.'}, status=500)




# def hendle_uploaded_file(f):
#     with open(f"media/files/{f.name}","wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# Загрузка файла

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]  # добавляем проверку
    
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            # user берем из request
            file_obj = serializer.save(user=request.user)
            return Response(FileSerializer(file_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#удаление файла 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def delete_file(request, file_id):
  
    try:
        file = File.objects.get(id=file_id)
        if file.user ==request.user or request.user.is_staff:
         file.delete()
         return Response({'message':'Файл удален'}, status=200)
        else: 
            return Response({'error': 'Нет прав на совершение данной операции'}, status=403)
    except File.DoesNotExist:
        return JsonResponse({'error': 'Файл не найден.'}, status=404)
    

# переименование файла
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rename_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)
        if file.user ==request.user or request.user.is_staff:
            new_name = request.data.get('name')

            if new_name:
                file.name = new_name
                file.save()
                return Response({'message': 'Имя файла успешно обновлено.'},status =200)
            else:
                return Response({'error': 'Новое имя не предоставлено.'}, status=400)
        else:
            return Response({'error': 'Нет прав на совершение данной операции'}, status=403)


    except File.DoesNotExist:
        return JsonResponse({'error': 'Файл не найден.'}, status=404)
#измениение комментария к файлу

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])

def update_comment(request, file_id):
    try:
        file = File.objects.get(id=file_id)
        if file.user ==request.user or request.user.is_staff:
            if 'comment' in request.data:
                new_comment = request.data['comment']

                if not new_comment:
                    return Response({'detail': 'Комментарий не может быть пустым.'}, status=status.HTTP_400_BAD_REQUEST)

                if len(new_comment) > 500:
                    return Response({'detail': 'Комментарий не может быть длиннее 500 символов.'},
                                status=status.HTTP_400_BAD_REQUEST)

                file.comment = new_comment
                file.save()

                serializer = FileSerializer(file)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({'detail': 'Комментарий не был передан.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'У вас нет прав для редактирования комментария этого файла.'},
                            status=status.HTTP_403_FORBIDDEN)
            
    except File.DoesNotExist:
        return Response({'detail': 'Файл не найден.'}, status=status.HTTP_404_NOT_FOUND)   


#получение внешней ссылки
def generate_file_link(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        print(f"File URL: {file.public_link}")

        file_url = file.public_link

        return JsonResponse({'link': file_url})

    except File.DoesNotExist:
        return JsonResponse({'error': 'Файл не найден.'}, status=404)


# скачивание файла

def download_file(request, file_id):
    doc = get_object_or_404(File, pk=file_id)
    
    # Проверка существования файла на диске
    if os.path.exists(doc.file.path):
        doc.last_downloaded = datetime.now()
        doc.save()
        return FileResponse(open(doc.file.path, 'rb'), as_attachment=True)
    else:
        raise Http404("Файл не найден")
    

# скачивание файла по внешней ссылке

def download_file2(request,op1):
    # doc2 = File.objects.get(public_link=op1)
    doc2 = get_object_or_404(File, public_link=op1)
    if os.path.exists(doc2.file.path):
        doc2.last_downloaded = datetime.now()
        doc2.save()
        return FileResponse(open(doc2.file.path, 'rb'), as_attachment=True,filename=doc2.name)
    else:
        raise Http404("Файл не найден")


   #количество всех файлов пользователя

def sum_of_files(request):
    # file = File.objects.filter(user = request.user)
    return Response('Jrfgh')

