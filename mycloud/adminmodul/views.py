from rest_framework.authtoken.models import Token
from venv import logger
from django.contrib.auth.models import User
from .models import RolePerson
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView

from filesstorage.models import File
from filesstorage.serializers import FileSerializer
from .serializers import PersonsSerializer,PersonsFilesSerializer, UseLoginSerializer,PersonsDataSerializer
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.views import APIView
from rest_framework import viewsets, mixins,permissions,status
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django.contrib.auth import authenticate, login,logout
from datetime import timedelta

 


# class PersonViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
#     queryset=Person.objects.all()
#     serializer_class=PersonsSerializer

class PersonViewSet(ModelViewSet):
    queryset=User.objects.all()
    serializer_class=PersonsSerializer
    def get_permissions(self):
        """
        Устанавливает различные права доступа в зависимости от действия (action).
        """
        if self.action == 'destroy' or self.action == 'update':
            # Доступно только аутентифицированным пользователям со статусом персонала (is_staff)
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'create':
            # Доступ разрешен всем пользователям 
            permission_classes = [permissions.AllowAny]

        else:
            # Для всех остальных действий (list retrieve) доступ разрешен аутентифицированным пользователям
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]

# Список файлов для конкретного пользователя

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_file_list(request, user_name):
    try:
    
        user = User.objects.filter(username = user_name)
        serializer = PersonsFilesSerializer(user, many=True)
        data = serializer.data
        if len(data[0]["files"])==0:
            return Response("Нет файлов")
        else: 
         return Response(data[0]["files"], status=200)

    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}", exc_info=True)
        return Response({'error': 'Произошла ошибка при получении файлов.'}, status=500)

    
    # try:
    #     files = File.objects.filter(user=int(user_id))
    #     serializer = FileSerializer(files, many=True)
    #     return JsonResponse({'files': serializer.data}, status=200)

    # except Exception as e:
    #     logger.error(f"Error fetching files: {str(e)}", exc_info=True)
    #     return JsonResponse({'error': 'Произошла ошибка при получении файлов.'}, status=500)

    # def create(self, request, *args, **kwargs):
            
    #     # Вызов стандартного метода DRF
    #     response = super().create(request, *args, **kwargs)
        
    #     # Ваша кастомная логика ПОСЛЕ создания
    #     response.data['path'] = f"/{response.data['id']}/"
        
        
    #     return response
    
### Аутентификация 
# Вход пользователя

class LoginView(APIView):
    serializer_class = UseLoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data =request.data)
        if serializer.is_valid():
         username = serializer.validated_data['username']
         password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'message':'Login successful'}, status=status.HTTP_200_OK),
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)
#     if user:
#         login(request, user)

#         #role = "admin" if user.is_staff else "user"

#         response = JsonResponse({
#             "message": "Вход выполнен успешно",
#             "is_staff": user.is_staff,
#            # "role": role, 
#             "username": user.username,
#         })

#         response.set_cookie(
#             key="sessionid",
#             value=request.session.session_key,
#             httponly=True,
#             secure=False,
#             max_age=timedelta(days=7),
#             samesite='Lax'
#         )

#         return response

#     return JsonResponse({"error": "Неправильный логин или пароль"}, status=400)


# Выход пользователя
# @api_view(["POST"])
# def logout_user(request):
#     response = Response({"message": "Вы вышли из системы"})
#     response.delete_cookie("access_token")
#     response.delete_cookie("refresh_token")
#     return response
class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'message':'Logout successful'}, status=status.HTTP_200_OK)







# def my_view(request):
#     data = {'name': 'Иван', 'age': 30}
#     return JsonResponse (data)


# # Регистрация пользователя

# def register_user(request):
#     data = {'username': 'Oleg', 'fullname': 'Oleg', 'email':'oleg@gmail.com',
#             'path':'/oleg/,'}
    
#     user = Person.objects.create(**data)
#     return JsonResponse ({'message': 'Пользователь успешно зарегистрирован.'},status=201)

# #Удаление пользователя
# def delete_user(request):
#      user = Person.objects.get(id=3)
#      user.delete()

    
#      return JsonResponse ({'message': 'Пользователь успешно удален.'},status=201)

    


#     # print("Received data:", data)

#     # username = data.get('username')
#     # fullname = data.get('fullname')
#     # email = data.get('email')
#     # password = data.get('password')
    

#     # if not username or not password or not email:
#     #     return JsonResponse({'message': 'Все поля обязательны!'}, status=400)

#     # try:
#     #     user = Person.objects.create_user(
#     #         username=username,
#     #         fullname=fullname,
#     #         email=email,
#     #         password=password)
#     #     print("User created successfully:", user)
#     #     return JsonResponse({'message': 'Пользователь успешно зарегистрирован.'}, status=201)
#     # except Exception as e:
#     #     print("Error creating user:", e)
#     #     return JsonResponse({'message': 'Ошибка при создании пользователя.'}, status=500)'''

# # Получение списка пользователей
# # #@method_decorator(csrf_exempt, name='dispatch')
# # @api_view(['GET'])
# # #@permission_classes([AllowAny])
# # def list_user(request):
# #     users = Person.objects.all()
# #     ser =PersonsSerializer(users, many = True)
    
# #     return Response(ser.data)

# class ListUser(ListAPIView):
#    queryset=Person.objects.all()
#    serializer_class =PersonsSerializer


# # аутентификация пользователя
# @api_view(['POST'])
# def login_user(request):
#    data=request.data
#    #data ={'username': 'Oleg', 'path':'/oleg/'}
#    if Person.objects.filter(username = data['username'], path =data['path']).exists():
#     return JsonResponse ({'message': 'its ok'},status=201)
#    else:
#     return JsonResponse ({'message': 'its no'},status=201)
   
# @api_view(['GET'])
# def hell(request):
#     return Response ("Hello")







# Получаем все активные сессии, срок действия которых еще не истек
# def active_sessions ():
#     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    

#     # for session in active_sessions:
#     #    print(f"Session Key: {session.session_key}")
#     #    data=session.get_decoded()
#     # Раскодируем данные сессии в обычный словарь
#     return Response(active_sessions) 




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request,token):
    
    tokens = Token.objects.get(key=token) 
    user=User.objects.get(id = tokens.user.id )
    role = RolePerson.objects.get(userpath = user)
    user1 =   {
     'username':user.username,
     'first_name':user.first_name,
     'email':user.email,
     'id':user.id,
     'role':role.role}
    # 
    # serializer = PersonsDataSerializer(user, many=True)
    return Response(user1)
         #{
    #  'username':user.username,
    #  'first_name':user.first_name,
    #  'email':user.email,
    #  'id':user.id,
    #  'role':user.role
    # })

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_user_status(request, user_id):
    """
    Обновление статуса администратора (is_staff) для пользователя.
    """
    try:
        user = User.objects.get(id=user_id)

        if user == request.user:
            return Response({'error': 'Вы не можете изменить собственный статус.'}, status=status.HTTP_403_FORBIDDEN)

        is_staff = request.data.get("is_staff")

        if is_staff is not None:
            user.is_staff = is_staff
            user.save()
            return Response({'message': f"Статус пользователя {user.username} обновлен."}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Параметр is_staff не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    