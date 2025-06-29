from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

    @classmethod
    def get_user_choices(cls):
        return [(user_id, f'Пользователь {user_id}') for user_id in cls.objects.values_list('userId', flat=True).distinct().order_by('userId')]
