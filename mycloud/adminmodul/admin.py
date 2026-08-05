from django.contrib import admin

from .models import PathPerson, RolePerson

#zfrom django.contrib.auth.models import User


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Отменяем стандартную регистрацию
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем 'id' в список отображаемых полей
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    # Делаем поле id доступным только для чтения на странице редактирования
    readonly_fields = ('id',)


class PathPersonAdmin(admin.ModelAdmin):
 list_display = ('id','userpath','path')

class RolePersonAdmin(admin.ModelAdmin):
 list_display = ('id','userpath','role')
    




admin.site.register(PathPerson, PathPersonAdmin)
admin.site.register(RolePerson, RolePersonAdmin)

