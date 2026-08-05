from django.urls import include, path
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

#from adminmodul.views import ListUser, PersonViewSet,my_view,register_user,delete_user,login_user
from .views import  FilesViewSet, generate_file_link,download_file, download_file2,list_files, FileUploadView,rename_file,delete_file,update_comment,sum_of_files
from django.conf import settings
from django.conf.urls.static import static
r=DefaultRouter()
r.register('files', FilesViewSet)

urlpatterns = [
path('files/',list_files, name='list_files'),
path('files/<path>/',list_files, name='list_files_path'),

 #path('upload/', DocumentUploadView.as_view(), name='document-upload'), 
 path('upload/',FileUploadView.as_view() , name='file-upload'),
# path('upload/',upload_file , name='file-upload'),
 path('files/delete/<int:file_id>/',delete_file, name='delete_file'),
 path('files/rename/<int:file_id>/', rename_file, name='rename_file'),
 path('files/comment/<int:file_id>/', update_comment, name='update_comment'),
 path('file_link/<int:file_id>/', generate_file_link),# формирование специальной ссылки
 path('download_file/<int:file_id>/', download_file),
 path('pablic/<uuid:op1>/', download_file2),

] +r.urls 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)