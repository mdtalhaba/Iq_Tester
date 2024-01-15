from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from quiz.models import Quiz, Category

def home(req, category_slug = None) :
    data = Quiz.objects.all()
    if category_slug is not None :
        cate = Category.objects.get(slug=category_slug)
        data = Quiz.objects.filter(category=cate)
    
    category = Category.objects.all()
    return render(req, 'index.html', {'data' : data, 'category' : category})


def quizes(req, quiz_id) :
    quiz = Quiz.objects.get(id=quiz_id)

    return render(req, 'quiz.html', {'quiz' : quiz})


class RegistrationView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/register/active/{uid}/{token}"
        message = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        send_email = EmailMultiAlternatives("Registration Message", '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        return super().form_valid(form)
    

def update_profile(req) :
    if req.method == 'POST' :
        form = UserUpdateForm(req.POST, instance=req.user)
        if form.is_valid() :
            messages.success(req, 'Your Information is Successfully Changed')
            form.save()
            return redirect('profile')
    else : 
        form = UserUpdateForm(instance=req.user)
    return render(req, 'profile.html', {'form' : form, 'type' : 'Profile'})

    
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None :
        user.is_active = True
        user.save()
        return redirect('register')
    else:
        return redirect('register')


class UserLoginView(LoginView) :
    template_name = './login.html'

    def get_success_url(self) :
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Log In'
        return context


class UserLogoutView(LogoutView) :
    def get_success_url(self):
        return reverse_lazy('login')