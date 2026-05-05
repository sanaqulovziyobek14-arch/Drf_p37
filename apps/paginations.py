from rest_framework.pagination import  CursorPagination, LimitOffsetPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-created_at'

class BlogPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 25