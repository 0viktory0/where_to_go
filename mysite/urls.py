from django.contrib import admin
from django.urls import path
from mysite import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_main),
]
