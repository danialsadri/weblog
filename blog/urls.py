from django.urls import path
from .import views


app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_list, name="post_list"),
    path('post/<int:post_id>/', views.post_detail, name="post_detail"),
    path('post/<int:post_id>/comment/', views.post_comment, name="post_comment"),
    path('ticket/', views.ticket, name="ticket"),
]
