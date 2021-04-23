from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('create_comment', views.create_comment),
    path('myaccount/<int:user_id>', views.myaccount),
    path('back', views.back),
    path('user/<int:user_id>', views.user_comments),
    path('update', views.update),
    path('delete_comment/<int:comment_id>', views.delete_comment),
    path('like/<int:comment_id>', views.add_like),
    path('about', views.about),
]