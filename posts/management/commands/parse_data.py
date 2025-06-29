import requests
from django.core.management.base import BaseCommand
from posts.models import Post

class Command(BaseCommand):
    help = 'Парсит данные с https://jsonplaceholder.typicode.com/posts и сохраняет их в базу данных.'

    def handle(self, *args, **kwargs):
        url = 'https://jsonplaceholder.typicode.com/posts'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            Post.objects.all().delete()  # Очищаем старые данные
            for item in data:
                Post.objects.create(
                    id=item['id'],
                    title=item['title'],
                    body=item['body'],
                    userId=item['userId']
                )
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены и сохранены.'))
        else:
            self.stdout.write(self.style.ERROR('Ошибка при получении данных.'))