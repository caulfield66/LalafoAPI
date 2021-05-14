from django.urls import path

from post.views import CategoriesListView, TagsListView, PostViewSet

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories-list'),
    path('tags/', TagsListView.as_view(), name='tags-list'),
]