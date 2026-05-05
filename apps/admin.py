from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Post, Category, Tag
from .models.posts import Like

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [LikeInline]

    readonly_fields = (
        'views_count',
    )

    list_display = (
        'id',
        'title',
        'category',
        'is_published',
    )

    list_filter = (
        'category',
        'is_published',
    )

    search_fields = (
        'title',
        'content',
    )


admin.site.register(Category)
admin.site.register(Tag)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username','email','is_staff',
    )
    search_fields = (
        'username',
        'email',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name')
    search_fields = ( 'title', 'slug')






