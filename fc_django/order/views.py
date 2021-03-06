from asyncore import dispatcher
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from django.views.generic.edit import FormView
from .forms import RegisterForm
from .models import Order
from django.utils.decorators import method_decorator
from fcuser.decorators import login_required,admin_required
from django.db import transaction
from product.models import Product
from fcuser.models import Fcuser

# Create your views here.
@method_decorator(admin_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self,form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity = form.data.get('quantity'),
                product = Product.objects.get(pk=form.data.get('product')),
                fcuser = Fcuser.objects.get(email=self.request.session.get('user'))
            )
            order.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()

        return super().form_valid(form)

    # form의 유효성 검사 통과 못했을 때 redirection해줄 주소 설정하는 부분.
    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    # session정보 가져오기.
    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request' : self.request
        })
        return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list' 

    # model을 가져오지 않고 get_queryset함수를 오버라이딩 하여 사용하는 이유는 접속한 사용자의 주문정보만 가져오기 위함. 이렇게 안하면 모든 사용자의 주문정보가 조회됨. 
    # ForeignKey를 filter를 걸어줄 땐 아래처럼 __를 주고 원래 모델에서 조회하고자 하는 테이블명을 넣어주면 된다. 아무런 테이블명을 넣어주지 않으면 default로 id값을 조회한다.
    def get_queryset(self,**kwargs):
        queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
        return queryset
