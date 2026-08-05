from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# class Person(AbstractUser):
    
#     # username = models.CharField(max_length=50, unique=True)
#     # fullname = models.CharField(max_length=255, blank=True, null=True)
#     # email = models.EmailField(max_length=100, unique=True)
#     path = models.CharField(max_length=255, null=True, blank=True) 
#     # is_admin = models.BooleanField(default=False)
def file_count(self):
        return self.files.count()
User.add_to_class("file_count",file_count)

def total_file_size(self):
        return self.files.aggregate(total_size=Sum('size'))['total_size'] or 0
User.add_to_class("total_file_size",total_file_size)
class PathPerson(models.Model):
    userpath = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="path",
        null=True, blank=True
    )
    path = models.CharField(max_length=255, null=True, blank=True) 

class RolePerson(models.Model):
    userpath = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="role",
        null=True, blank=True
    )
    role = models.CharField(max_length=255, null=True, blank=True)

    
#     # username = models.CharField(max_length=50, unique=True)
#     # fullname = models.CharField(max_length=255, blank=True, null=True)
#     # email = models.EmailField(max_length=100, unique=True)
#     path = models.CharField(max_length=255, null=True, blank=True) 
#     # is_admin = models.BooleanField(default=False)



    # def save(self, *args, **kwargs):
        
    #     self.path = f'/{self.id}/'
    #     super().save(*args, **kwargs)

    
    
    
