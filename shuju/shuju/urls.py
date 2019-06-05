"""shuju URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('api/login/', views.api_login),
    path('api/get_city/', views.get_city),
    path('api/get_salesMonthly/', views.get_salesMonthly),  #1. 某个城市 销售月报接口
    path('api/get_orders/', views.get_signDetails), #2. 某个城市 某月份的签约详细表
    path('api/export/', views.export),
    path('api/uploadFile/', views.uploadFile)
]
