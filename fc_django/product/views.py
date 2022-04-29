from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# Create your views here.

# listview는 model만 넘겨주면 리스트로 뷰를 만들어준다.
class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    # 원래 object_lsit라는 변수명으로 template에서 리스트값들을 불러올 수 있음. 다른 변수명을 사용하고 싶을 땐 context_object_name을 사용해서 원하는 변수명 설정 가능.
    context_object_name = 'product_list' 