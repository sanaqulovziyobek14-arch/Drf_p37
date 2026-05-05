from django.db.models import Count
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter

from apps.models import Post


class PostFilter(FilterSet):
    category = CharFilter(
        field_name='category__name',
        lookup_expr='icontains'
    )

    tags = CharFilter(method='filter_tags')

    created_at = DateFromToRangeFilter()
    class Meta:
        model = Post
        fields = 'category', 'tags'

    def filter_tags(self, queryset, name, value):
        tags = value.split(',')
        return queryset.filter(
            tags__slug__in=tags
        ).distinct()

    #
    # def filter_comment_count(self, queryset, key, value):
    #     return queryset.annotate(
    #         comment_count=Count('comments')
    #     ).filter(comment_count__gte=value)






# from django.db.models import Count
# from django_filters import FilterSet, NumberFilter
# from apps.models import Post, User
#
# class PostFilter(FilterSet):
#     # min_id = NumberFilter(field_name='userId', lookup_expr='gte')
#     # max_id = NumberFilter(field_name='userId', lookup_expr='lte')
#     comment_count = NumberFilter(method='filter_comment_count')
#
#     class Meta:
#         model = Post
#         fields = ()
#     def filter_comment_count(self, queryset, key, value):
#         return queryset.annotate(comment_count=Count('comment_id')).filter(comment_count__gte=value)
#
# class AlbumFilter(FilterSet):
#     album_count = NumberFilter(method='filter_album_count')
#
#     class Meta:
#         model = Album
#         fields = ()
#     def filter_album_count(self, queryset, key, value):
#         return queryset.annotate(album_count=Count('photo_id')).filter(album_count__gte=value)
#
#
# class PhotoFilter(FilterSet):
#     photo_count = NumberFilter(method='filter_photo_count')
#     class Meta:
#         model = Photo
#         fields = ()
#     def filter_photo_count(self, queryset, key, value):
#         return queryset.annotate(photo_count=Count('photo_id')).filter(photo_count__gte=value)
#
# class TodoFilter(FilterSet):
#     todo_count = NumberFilter(method='filter_todo_count')
#     class Meta:
#         model = Todo
#         fields = ()
#     def filter_todo_count(self, queryset, key, value):
#         return queryset.annotate(todo_count=Count('todo_id')).filter(todo_count__gte=value)
#
# class UserFilter(FilterSet):
#     user_count = NumberFilter(method='filter_user_count')
#     class Meta:
#         model = User
#         fields = ()
#     def filter_user_count(self, queryset, key, value):
#         return queryset.annotate(user_count=Count('user_id')).filter(user_count__gte=value)


