from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from django.db.models import Q
import requests
from django.db import transaction

# Create your views here.

def bubble_sort(posts, key, reverse=False):
    """
    Сортировка пузырьком для списка постов
    :param posts: список постов
    :param key: ключ для сортировки ('id' или 'title')
    :param reverse: направление сортировки (True - по убыванию, False - по возрастанию)
    :return: отсортированный список
    """
    posts = list(posts)
    n = len(posts)

    # Для сортировки по заголовку используем нижний регистр
    if key == 'title':
        for i in range(n):
            for j in range(0, n-i-1):
                if (posts[j].title.lower() > posts[j+1].title.lower()) != reverse:
                    posts[j], posts[j+1] = posts[j+1], posts[j]
    else:
        # Для сортировки по ID
        for i in range(n):
            for j in range(0, n-i-1):
                if (getattr(posts[j], key) > getattr(posts[j+1], key)) != reverse:
                    posts[j], posts[j+1] = posts[j+1], posts[j]
    return posts

def binary_search(posts, target_id):
    left, right = 0, len(posts) - 1
    while left <= right:
        mid = (left + right) // 2
        if posts[mid].id == target_id:
            return posts[mid]
        elif posts[mid].id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return None

def parse_posts():
    try:
        # Получаем данные с API
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        posts_data = response.json()

        # Используем транзакцию для атомарного обновления
        with transaction.atomic():
            # Очищаем существующие посты
            Post.objects.all().delete()

            # Создаем новые посты
            for post_data in posts_data:
                Post.objects.create(
                    id=post_data['id'],
                    userId=post_data['userId'],
                    title=post_data['title'],
                    body=post_data['body']
                )

        return True, "Посты успешно обновлены"
    except Exception as e:
        return False, f"Ошибка при обновлении постов: {str(e)}"

def post_list(request):
    # Парсим посты при каждом запросе списка
    success, message = parse_posts()

    # Получаем параметры поиска и сортировки
    search_query = request.GET.get('search', '')
    id_query = request.GET.get('id', '')
    sort_by = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    page = request.GET.get('page', 1)

    # Базовый queryset
    posts = Post.objects.all()

    # Применяем фильтры поиска
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    if id_query:
        posts = posts.filter(id=id_query)

    # Применяем сортировку пузырьком
    posts = bubble_sort(posts, sort_by, order == 'desc')

    # Пагинация
    paginator = Paginator(posts, 100)  # Показываем 100 постов на странице
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'message': message if not success else None,
        'error': message if not success else None,
        'search': search_query,
        'id': id_query,
        'sort': sort_by,
        'order': order,
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})
