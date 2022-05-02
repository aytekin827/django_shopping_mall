from django.views.generic import ListView,FormView,DetailView
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins

from fcuser.decorators import admin_required
from .models import Product
from .forms import RegisterForm
from .serializers import ProductSerializer
from order.forms import RegisterForm as OrderForm

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.all().order_by('id')

    # listmodelmixin을 사용하기 때문에 아래처럼 사용해도 된다.?
    def get(self,request,*args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.all().order_by('id')

    # listmodelmixin을 사용하기 때문에 아래처럼 사용해도 된다.?
    def get(self,request,*args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# listview는 model만 넘겨주면 리스트로 뷰를 만들어준다.
class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    # 원래 object_lsit라는 변수명으로 template에서 리스트값들을 불러올 수 있음. 다른 변수명을 사용하고 싶을 땐 context_object_name을 사용해서 원하는 변수명 설정 가능.
    context_object_name = 'product_list' 

@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self,form):
        product = Product(
            name = form.data.get('name'),
            price = form.data.get('price'),
            description = form.data.get('description'),
            stock = form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)

class Productdetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all() # SQL filter를 줄 수도 있음. 
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request) # form이라는 변수에 OrderForm의 내용이 반영됨.
        return context