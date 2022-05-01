from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from fcuser.models import Fcuser

# Create your views here.

def index(request):
    return render(request,'index.html', {'email':request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    # 유효성 검사가 끝났을 때 회원을 가입시킴
    def form_valid(self, form):
        fcuser = Fcuser(
            email = form.data.get('email'),
            password = make_password(form.data.get('password')),
            level='user'
        )
        fcuser.save()

        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    # 폼의 유효성 검사 후 사용하는 함수다.
    def form_valid(self,form):
        self.request.session['user'] = form.data.get('email')
        # 
        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/login')