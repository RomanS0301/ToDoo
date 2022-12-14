from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio/images/')  # при установке параметра yes добавляется папка media
    url = models.URLField(blank=True)  # позволяет открывать ссылку в новом окне

# Каждый раз после создания модели или измененения необходимо проводить миграции
