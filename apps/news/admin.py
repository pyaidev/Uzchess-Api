from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.news.models import NewArticle, NewArticleView


@admin.register(NewArticle)
class NewArticleModelAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created')
    list_filter = ('title', 'created', 'view')
    fields = ('title', 'image', 'description', 'view')
    exclude = ('slug',)
    search_fields = ('id', 'title', 'description')


@admin.register(NewArticleView)
class NewArticleViewModelAdmin(ModelAdmin):
    list_display = ('id', 'new_id', 'new', 'user_username', 'device_id')

    def new_view_id(self, obj):
        return obj.new.id

    new_view_id.short_description = 'NewView'

    def new_view_view(self, obj):
        return obj.new.view

    new_view_view.short_description = 'NewView'

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'User'
