from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name='default'),
    path('post/', views.posts, name='posts'),
    path('post/addPost/', views.add_post, name='add_post'),
    path('post/delPost/<int:post_id>', views.delete_post, name='delete_post'),
    path('post/putPost/', views.put_post, name='put_post'),
]
