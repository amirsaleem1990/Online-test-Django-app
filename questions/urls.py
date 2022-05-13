from django.urls import path
from . import views
app_name = "questions"
urlpatterns = [
    # ex: /questions/
    # path('', views.index, name='index'),
    # path("index", views.auth, name='auth'),
    # path("next_quest", views.next_quest, name='next_quest'),
    path("create_post", views.create_post, name='create_post'),
    path("thank_you", views.thank_you, name='thank_you'),
]


