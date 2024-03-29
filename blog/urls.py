from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('', PostListView.as_view(),name = 'blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(),name = 'user-posts'),
    path('post/<int:pk>/', get_post,name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(),name = 'post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(),name = 'post-delete'),
    path('about/', views.about,name = 'blog-about'),
    path('like/<int:pk>', views.likes,name = 'like_post'),
    path('unlike/<int:pk>', views.unlike,name = 'unlike_post'),
    path('search/', views.search,name = 'search'),

]