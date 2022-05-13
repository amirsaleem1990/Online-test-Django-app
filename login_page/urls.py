# from django.urls import path
# from . import views
# app_name = "login_page"
# urlpatterns = [
#     # ex: /login_page/
#     path('', views.index_2, name='index_2'),
#     path('auth', views.auth, name="auth"),
# ]


from django.conf.urls import url
from login_page.views import dashboard
from django.urls import include

urlpatterns = [
    url("dashboard/", dashboard, name="dashboard"), # myapp.views.hello
    url("accounts/", include("django.contrib.auth.urls")),
]