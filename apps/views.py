import os

from django.contrib.admin import actions
from django.core.serializers import get_serializer
from django.db.models import OuterRef, Exists, Value
from django.db.models.aggregates import Count
from django.db.models.fields import BooleanField
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.filters import PostFilter
from apps.models import Post, User
from apps.models.posts import Like, Product, Favorite
from apps.permissions import IsAuthorOrReadOnly
from apps.serializer import CustomTokenObtainPairSerializer, PostModelSerializer,  ProductSerializer, \
    UserModelSerializer
from root import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=['Post'])
class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            key = Exists(Like.objects.filter(post_id=OuterRef('pk'), user=user))
        else:
            key = Value(False, BooleanField())

        return qs.annotate(
            likes_count=Count('likes'),
            is_leked=key
        )

    @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
    def set_like(self, request, pk=None):
        Like.objects.get_or_create(user=request.user, post_id=pk)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'], url_path='unlike', serializer_class=None)
    def set_unlike(self, request, pk=None):
        Like.objects.filter(user=request.user, post_id=pk).delete()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['get'], url_path='my-posts',permission_classes=[IsAuthenticated],serializer_class = PostModelSerializer)
    def my_posts(self, request):
        user = request.user
        qs = self.get_queryset().filter(author=user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        response = self.get_serializer(qs, many=True).data
        return self.get_paginated_response(response)


@extend_schema(tags=['Post'])
class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PostFilter
    ordering_fields = 'created_at', 'views_count', 'likes_count'
    search_fields = 'title', 'content'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(likes_count=Count('likes'))


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer


# -------------------------------------------------------------------------------------------------------------------------

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        queryset = Product.objects.select_related(
            'category'
        ).annotate(
            favorites_count=Count(
                'favorites',
                distinct=True
            )
        )

        # user authenticated bolsa
        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    Favorite.objects.filter(
                        user=user,
                        product=OuterRef('pk')
                    )
                )
            )

        else:
            queryset = queryset.annotate(
                is_favorited=Value(
                    False,
                    output_field=BooleanField()
                )
            )

        return queryset
 # ---------------------------------------------------------------------------------------------------------------------------------------------

class ExcelAPIView(APIView):
    permission_classes = []
    def get(self, request):

        return FileResponse(open(os.path.join(settings.BASE_DIR, 'static/img/logo.png'), 'rb'))
    pass

# -----------------------------------------------------------------------------------------------------------------------------

class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = []






# from django.contrib.admin import actions
# from django.db.models.aggregates import Count
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.decorators import action
# from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework_simplejwt.views import TokenObtainPairView
#
# from apps.filters import PostFilter
# from apps.models import Post
# from apps.models.posts import Like
# from apps.serializer import CustomTokenObtainPairSerializer, PostModelSerializer
#
#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
#
#
# class PostModelViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     http_method_names = ['get', 'post']
#
#     @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
#     def set_like(self, request, pk=None):
#         Like.objects.get_or_create(user=request.user, post_id=pk)
#         return Response({'status': 'ok'})
#
#     @action(detail=True, methods=['post'], url_path='unlike', serializer_class=None)
#     def set_unlike(self, request, pk=None):
#         Like.objects.filter(user=request.user, post_id=pk).delete()
#         return Response({'status': 'ok'})
#
# # class PostListCreateAPIView(ListCreateAPIView):
# #     queryset = Post.objects.all()
# #     serializer_class = PostModelSerializer
# #     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
# #     filterset_class = PostFilter
# #     ordering_fields = 'created_at', 'views_count', 'likes_count'
# #     search_fields = 'title', 'content'
# #
# #     def get_queryset(self):
# #         qs = super().get_queryset()
# #         return qs.annotate(likes_count=Count('likes'))
# #
# #
#
#
#
#
#
#
#
#
#
#
#
#
#
# # @extend_schema(tags=['Post'])
# # class PostListCreateAPIView(ListCreateAPIView):
# #     queryset = Post.objects.order_by('-id')
# #     serializer_class = PostModelSerializer
# #     filter_backends = (DjangoFilterBackend,)
# #     # filterset_fields = ('userId', )
# #     filterset_class = PostFilter
# #
# # @extend_schema(tags=['Post'])
# # class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
# #     queryset = Post.objects.all()
# #     serializer_class = PostModelSerializer
# #
# # @extend_schema(tags=['Post'])
# # class PostCommentListAPIView(ListAPIView):
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentModelSerializer
# #
# #     def get_queryset(self):
# #         qs = super().get_queryset()
# #         pk = self.kwargs.get['pk']
# #         return qs.filter(postId=pk)
# #
# #
# # # <-------------------------------------------------------------------------------------------------------------
# #
# # @extend_schema(tags=['Comment'])
# # class CommentListCreateAPIView(ListAPIView):
# #     queryset = Comment.objects.order_by('-id')
# #     serializer_class = CommentModelSerializer
# #     filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
# #     filterset_fields = ('postId','email')
# #     search_fields = ('email',)
# #     ordering_fields = ('id','postId')
# #
# # @extend_schema(tags=['Comment'])
# # class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentModelSerializer
# #
# #
# # # <-------------------------------------------------------------------------------------------------------------
# # @extend_schema(tags=['Album'])
# # class AlbumListCreateAPIView(ListCreateAPIView):
# #     queryset = Album.objects.order_by('-id')
# #     serializer_class = AlbumModelSerializer
# #     filter_backends = (DjangoFilterBackend,)
# #     filterset_class = AlbumFilter
# #
# # @extend_schema(tags=['Album'])
# # class AlbumRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
# #     queryset = Album.objects.all()
# #     serializer_class = AlbumModelSerializer
# #
# # @extend_schema(tags=['Album'])
# # class AlbumCommentListAPIView(ListAPIView):
# #     queryset = Photo.objects.all()
# #     serializer_class = PhotoModelSerializer
# #
# #     def get_queryset(self):
# #         qs = super().get_queryset()
# #         pk = self.kwargs.get['pk']
# #         return qs.filter(albumId=pk)
# #
# #
# # # <-------------------------------------------------------------------------------------------------------------
# #
# #
# # @extend_schema(tags=['Photo'])
# # class PhotoListAPIView(ListAPIView):
# #     queryset = Photo.objects.all()
# #     serializer_class = PhotoModelSerializer
# #
# # # <-------------------------------------------------------------------------------------------------------------
# #
# #
# # @extend_schema(tags=['Todo'])
# # class TodoListAPIView(ListAPIView):
# #     queryset = Todo.objects.all()
# #     serializer_class = TodoModelSerializer
# #
# # # <-------------------------------------------------------------------------------------------------------------
# #
# #
# # @extend_schema(tags=['User'])
# # class UserListAPIView(ListAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserModelSerializer
# #
# # # <--------------------------------------------------------------------------------------------------------------
# #
# # @extend_schema(tags=['Book'])
# # class BookListCreateAPIView(ListCreateAPIView):
# #     queryset = Book.objects.order_by('-id')
# #     serializer_class = BookModelSerializer
# #
# #     def get_serializer_class(self):
# #         if self.request.method == 'POST':
# #             return BookListCreateAPIView
# #         return super().get_serializer_class()
# #
# # @extend_schema(tags=['Book'])
# # class UserRetrieveAPIView(RetrieveAPIView):
# #     queryset = User.objects.order_by('-id')
# #     serializer_class = BookDetailModelSerializer
# #
# #
# # # <--------------------------------------------------------------------------------------------------------------
# #
# # @extend_schema(tags=['Student'])
# # class StudentListCreateAPIView(ListCreateAPIView):
# #     serializer_class = StudentSerializer
# #     queryset = Student.objects.all()
# #
# #     filter_backends = [DjangoFilterBackend, OrderingFilter]
# #     ordering_fields = ['age', 'created_at']
# #     ordering = ['id']
# #
# #     def get_queryset(self):
# #         queryset = Student.objects.all()
# #
# #         name = self.request.query_params.get('name')
# #         grade = self.request.query_params.get('grade')
# #         min_age = self.request.query_params.get('min_age')
# #         active = self.request.query_params.get('active')
# #
# #         if name:
# #             queryset = queryset.filter(name__icontains=name)
# #
# #         if grade:
# #             queryset = queryset.filter(grade=grade)
# #
# #         if min_age:
# #             queryset = queryset.filter(age__gte=min_age)
# #
# #         if active:
# #             if active.lower() == 'true':
# #                 queryset = queryset.filter(is_active=True)
# #             elif active.lower() == 'false':
# #                 queryset = queryset.filter(is_active=False)
# #
# #         return queryset
# #
# #
# # # <--------------------------------------------------------------------------------------------------------------
# #
# #
# # @extend_schema(tags=['Product'])
# # class ProductListCreateAPIView(ListCreateAPIView):
# #     queryset = Product.objects.order_by('-id')
# #     serializer_class =ProductListCreateModelSerializer
# #
# # # ----------------------------------------------------------------------------------------------
# #
# # class CustomTokenObtainPairView(TokenObtainPairView):
# #     serializer_class = CustomTokenObtainPairSerializer
# #
# #
# # class PostModelViewSet(ModelViewSet):
# #     queryset = Post.objects.all()
# #     serializer_class = PostModelSerializer
# #     http_method_names = ['get', 'post']
# #
# #     @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
# #     def set_like(self, request, pk=None):
# #         Like.objects.get_or_create(user=request.user, post_id=pk)
# #         return Response({'status': 'ok'})
# #
# #     @action(detail=True, methods=['post'], url_path='unlike', serializer_class=None)
# #     def set_unlike(self, request, pk=None):
# #         Like.objects.filter(user=request.user, post_id=pk).delete()
# #         return Response({'status': 'ok'})
#
# # class PostListCreateAPIView(ListCreateAPIView):
# #     queryset = Post.objects.all()
# #     serializer_class = PostModelSerializer
# #     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
# #     filterset_class = PostFilter
# #     ordering_fields = 'created_at', 'views_count', 'likes_count'
# #     search_fields = 'title', 'content'
# #
# #     def get_queryset(self):
# #         qs = super().get_queryset()
# #         return qs.annotate(likes_count=Count('likes'))
# #
# #
#
# #
# # @extend_schema(tags=['post'])
# # class PostListCreateView(ListCreateAPIView):
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# #
# #     filter_backends = (DjangoFilterBackend, SearchFilter)
# #     filterset_class = PostFilter
# #     search_fields = ('title', 'content')
# #
# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)
# #
# #
# # @extend_schema(tags=['post'])
# # class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# ##
# #
# # @extend_schema(tags=['user'])
# # class UserListCreateView(ListCreateAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
