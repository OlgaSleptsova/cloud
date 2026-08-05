

from django.urls import include, path
# from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

#from adminmodul.views import ListUser, PersonViewSet,my_view,register_user,delete_user,login_user
from adminmodul.views import  PersonViewSet, users_file_list,LoginView,LogoutView,current_user,update_user_status
r=DefaultRouter()
r.register('persons', PersonViewSet)

urlpatterns = [
    path('persons/files/<str:user_name>/',users_file_list, name='users_file_list'),
    # path('login/',LoginView.as_view() , name='login_user'),
    # path('logout/',LogoutView.as_view(), name='logout_user'),
    path('user/me/<token>/',current_user, name='current_user'),
    # path('sessions/',active_sessions, name='active_sessions'),
    path('users/<int:user_id>/update-status/', update_user_status, name='update_user_status'),
  
    
] +r.urls