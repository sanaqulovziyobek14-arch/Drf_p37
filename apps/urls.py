from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.views import CustomTokenObtainPairView, PostModelViewSet, PostViewSet, ProductViewSet, UserCreateApiView

router = SimpleRouter(trailing_slash=False)
router.register('posts', PostModelViewSet)
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register', UserCreateApiView.as_view()),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('posts', PostListCreateAPIView.as_view(), name='posts'),

]




# from django.urls import path, include
# from rest_framework.routers import SimpleRouter
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
#
#
# from apps.views import PostModelViewSet
#
# router = SimpleRouter(trailing_slash=False)
# router.register('posts', PostModelViewSet)
#
# urlpatterns = [
#     path('posts', PostListCreateAPIView.as_view()),
#     path('students/', StudentListCreateAPIView.as_view()),
#     path('posts/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view()),
#     path('posts/<int:pk>/comments', PostCommentListAPIView.as_view()),
#     path('', include(router.urls)),
#     path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
#     path('posts/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view()),
#     path('posts', PostListCreateView.as_view()),
#     path('users', UserListCreateView.as_view()),
# ]

