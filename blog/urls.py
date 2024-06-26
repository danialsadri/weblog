from django.urls import path
from . import views
from django.contrib.auth.views import *

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post_list, name="post_list"),
    path('post/<str:category>/', views.post_list, name='post_list_category'),
    path('post/detail/<int:post_id>/', views.post_detail, name="post_detail"),
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
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('account/edit/', views.edit_account, name='edit_account'),
]
