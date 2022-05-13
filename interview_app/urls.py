from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
	# path("", include("login_page.urls")),
	# path("login_page/", include("login_page.urls")),
	path("admin/", admin.site.urls),
	url("questions/", include("questions.urls")),
    url("",           include("login_page.urls")),
    # url("create_post",include("login_page.urls")),
]

