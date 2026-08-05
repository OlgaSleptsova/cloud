from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import PathPerson, RolePerson
from filesstorage.serializers import FileSerializer
from django.contrib.auth.models import User

# Создаем валидатор: только латиница и цифры, первый символ буква
alphanumeric = RegexValidator(
    regex=r'^[a-zA-Z][a-zA-Z0-9]+$',
    message='Разрешены только латинские буквы и цифры, первый символ-буква',
    code='invalid_alphanumeric'
)
# Создаем валидатор пароля
password_volidator = RegexValidator(
    regex=r'^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$',
    message='Пароль должен содержать не менее 6 символов, минимум одна заглавная буква, одна цифра и один спецсимвол ',
    code='invalid_password_volidater'
)

class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathPerson
        fields = ['path']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePerson
        fields = ['role']


class PersonsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[alphanumeric],
        min_length=4,
        max_length=20
    )
    email = serializers.EmailField()
    password=serializers.CharField(
        validators =[password_volidator]  
    )
    path = PathSerializer(many=True, read_only=True)
    role = RoleSerializer(many=True, read_only=True)
    file_count = serializers.SerializerMethodField()
    total_size = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'first_name', 'is_staff','path','role','file_count', 'total_size']
        extra_kwargs = {'password': {'write_only': True}}


    def get_file_count(self, obj):
       
        return obj.file_count()

    def get_total_size(self, obj):
        return obj.total_file_size()
    
    def create(self, validated_data):
        # Извлекаем пароль из проверенных данных
        password = validated_data.pop('password')
        print(validated_data)
        # Создаем пользователя без пароля
        user = User.objects.create(**validated_data)
       
        # Устанавливаем хешированный пароль
        user.set_password(password)
        user.save()
        another_obj = PathPerson(userpath=user,path =f"/{user.username}/" )
        another_obj.save()
        role = "admin" if user.is_staff else "user"
        role_obj = RolePerson(userpath=user,role=role)
        role_obj.save()
        
        
        return user


class PersonsFilesSerializer(serializers.ModelSerializer):
    
    files = FileSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['files']

class UseLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']


class PersonsDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'is_staff']
        
  
