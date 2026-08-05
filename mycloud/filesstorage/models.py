import uuid

from django.db import models


from mycloud import settings
#from django.utils import timezone
from django.contrib.auth.models import User



class File(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="files",
        null=True, blank=True
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()
    #upload_date = models.DateTimeField(default=timezone.now)
    last_downloaded = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    public_link = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.name and self.file:
            self.name = self.file.name
        if not self.size and self.file:
            self.size = self.file.size
        if not self.public_link:
            self.public_link = self.generate_public_link()
        super().save(*args, **kwargs)

    def generate_public_link(self):
        """
        Генерация уникальной публичной ссылки для скачивания файла.
        Ссылка должна быть уникальной и безопасной для доступа.
        """
        # Генерация уникального идентификатора для ссылки
        file_uuid = uuid.uuid4()
        #return f"{settings.BASE_URL}/files/{file_uuid}/"
        return file_uuid


