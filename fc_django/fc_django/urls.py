"""fc_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from fcuser.views import index,RegisterView,LoginView, logout
from product.views import ProductList, ProductCreate, Productdetail, ProductListAPI,ProductDetailAPI
from order.views import OrderCreate, OrderList

urlpatterns = [
    re_path(r'^admin/manual/$', 
        TemplateView.as_view(template_name='admin/manual.html', 
        extra_context={'title':'메뉴얼','site_title' : '!!페스트캠퍼스!!', 'site_header' : '!  페스트캠퍼스 !'})),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),    
    path('', index),
    path('register/',RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('product/',ProductList.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),
    path('product/<int:pk>/',Productdetail.as_view()),
    path('logout', logout),

    path('api/product/', ProductListAPI.as_view()),
    path('api/product/<int:pk>', ProductDetailAPI.as_view()),
]
