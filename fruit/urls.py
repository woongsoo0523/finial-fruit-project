from django.urls import path

from . import views

app_name = 'fruit'

urlpatterns = [  
    path("", views.index, name="index"),
    path("login/", views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path("signup/", views.signup, name='signup'),
    path("upload/", views.upload, name="upload"),
    path("detail/", views.detail, name="detail"),
    path("fruitlist/", views.fruitlist, name="fruitlist"),
    path("detail2/<int:id>/", views.detail2, name="detail2"),
    path("delete/<int:id>/", views.delete, name="delete"),
]
