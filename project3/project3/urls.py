"""project3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app3 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.signup,name='signup_api'),
    path('login', views.login, name='login_api'),
    path('create_medicine', views.create_medicine, name='createmedicineapi'),
    path('list_medicines', views.list_medicines, name='retrievemedicineapi'),
    path('<int:pk>/update_medicine', views.update_medicine, name='updatemedicineapi'),
    path('<int:pk>/delete_medicine', views.delete_medicine, name='deletemedicineapi'),
    path('search/',views.Search, name='search'),
]
