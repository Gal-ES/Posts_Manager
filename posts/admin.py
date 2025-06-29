from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.html import format_html
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'title', 'actions_column')
    list_display_links = None
    search_fields = ('title', 'body')
    list_filter = ('userId',)
    ordering = ('id',)
    fields = ('userId', 'title', 'body')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:post_id>/view/',
                self.admin_site.admin_view(self.view_post),
                name='post-view',
            ),
        ]
        return custom_urls + urls

    def view_post(self, request, post_id):
        post = self.get_object(request, post_id)
        context = {
            'title': f'Просмотр поста #{post.id}',
            'post': post,
            'opts': self.model._meta,
            'is_popup': False,
            'is_nav_sidebar_enabled': True,
            'has_permission': self.has_view_permission(request, post),
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/posts/post/view.html', context)

    def actions_column(self, obj):
        return format_html(
            '<a class="button" style="background-color: #4CAF50; color: white; padding: 5px 10px; margin-right: 5px; text-decoration: none; border-radius: 3px;" href="{}">View</a> '
            '<a class="button" style="background-color: #2196F3; color: white; padding: 5px 10px; margin-right: 5px; text-decoration: none; border-radius: 3px;" href="{}">Edit</a> '
            '<a class="button" style="background-color: #f44336; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;" href="{}">Delete</a>',
            f'/admin/posts/post/{obj.id}/view/',
            f'/admin/posts/post/{obj.id}/change/',
            f'/admin/posts/post/{obj.id}/delete/'
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
