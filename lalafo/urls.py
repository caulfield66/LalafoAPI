"""lalafo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from post.views import PostViewSet, api_root, CommentCreateView, CategoriesListView, TagsListView

router = DefaultRouter()
router.register('posts', PostViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Lalafo API',
        default_version='v1',
        description='Lalafo\'s API'
    ), public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include('post.urls')),
    path('', api_root),
    path('api/v1/comments/', CommentCreateView.as_view(), name="create-comment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v1/categories/', CategoriesListView.as_view(), name='categories-list'),
#     path('api/v1/tags/', TagsListView.as_view(), name='tags-list'),
#     # path('', api_root),
#     path('api/v1/posts/', PostViewSet.as_view(
#         {'post': 'create', 'get': 'list'}
#     ), name='post-list'),
#     path('api/v1/posts/<slug:slug>/', PostViewSet.as_view(
#         {'put': 'update', 'patch': 'partial_update', 'get': 'retrieve', 'delete': 'destroy' }
#     )),
#     path('api/v1/', include('account.urls'))
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)