from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post_list, name="post_list"),
    path('post/<int:post_id>/', views.post_detail, name="post_detail"),
    path('post/<int:post_id>/comment/', views.post_comment, name="post_comment"),
    path('post/create/', views.post_create, name="post_create"),
    path('post/edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post/delete/<int:post_id>/', views.post_delete, name="post_delete"),
    path('image/delete/<int:image_id>/', views.image_delete, name="image_delete"),
    path('ticket/', views.ticket, name="ticket"),
    path('search/', views.post_search, name="post_search"),
    path('profile/', views.profile, name='profile'),
    # path('login/', views.user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', views.logout_view, name='logout'),
    path('password_change/', PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
