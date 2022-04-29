import imp
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm

# Create your views here.
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    # form의 유효성 검사 통과 못했을 때 redirection해줄 주소 설정하는 부분.
    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request' : self.request
        })
        return kw