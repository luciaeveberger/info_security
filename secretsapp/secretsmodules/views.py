import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from . import models
from django.core import serializers
from secretsmodules.models import Secret, UserProfile
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def duplicate_mail(email):
    users = list(User.objects.filter(email = email))
    if len(users) > 0:
        return True
    return False



# Create your views here.
# class HomePageView(TemplateView):
#     template_name = 'secretsmodules/index.html'
#     def get(self, request, **kwargs):
#         secrets = Secret.objects.all()
#         my_dict = {'all_secrets':secrets}
#         return render(request, 'secretsmodules/index.html', context=my_dict)
# class HomePageView(TemplateView):
#     template_name = 'secretsmodules/index.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         secrets = Secret.objects.all()
#         context['all_secrets'] = secrets
#         return context
class HomePageView(ListView):
    template_name = 'secretsmodules/index.html'
    context_object_name = 'all_secrets'  #default: objectname_list
    model = models.Secret

class DetailsView(DetailView):
    model = models.Secret
    template_name = 'secretsmodules/details.html'
    context_object_name = 'secret'    #default: objectname.


def add_to_cart(request, secret_id):
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
        secret = Secret.objects.get(pk=secret_id)
        serialized_obj = serializers.serialize('json', [secret])
        cart[len(cart)] = (serialized_obj)
        request.session['cart'] = cart
        my_cart = request.session['cart']
        # need to change this because the action adds to cart every time
        return render(request, 'secretsmodules/cart.html', context=my_cart)
    else:
        return HttpResponseRedirect(reverse('login'))


class RegisterForm(TemplateView):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        form = forms.UserForm()
        return render(request, 'secretsmodules/register.html', context={'form': form})
    def post(self, request, **kwargs):
        form = forms.UserForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            try:
                if duplicate_mail(data['email']):
                    form.add_error(field = 'email', error = "Email already in user")
                try:
                    validate_password(data['password'])
                except ValidationError as ve:
                    form.add_error(field = 'password', error = ve.messages)
                if len(form.errors) > 0:
                    return render(request, 'secretsmodules/register.html', context={'form': form})
                user = User.objects.create_user(username=data['username'],
                                             email=data['email'],
                                             password=data['password'],
                                             first_name = data['first_name'],
                                             last_name = data['last_name'])

            except IntegrityError as e:

                if 'unique constraint' in str(e).lower():
                    form.add_error(field = 'username', error="Username already in use")
                else:
                    form.add_error(field = none, error = "Unspecified error, try again later")
                return render(request, 'secretsmodules/register.html', context={'form': form})
            except Exception as e:
                form.add_error(field = None, error = "Unspecified Integrity error, try again later" )
                return render(request, 'secretsmodules/register.html', context={'form': form})
            profile = UserProfile(user = user, address = data['address'], phone = data['phone'])
            profile.save()

            login(request=request,user=user)
            return HttpResponseRedirect(reverse('index'))   #change later to profile page
        else:
            return render(request, 'secretsmodules/register.html', context={'form': form})


class LoginForm(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'secretsmodules/login.html')
    def post(self, request, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        botcarcher = request.POST.get('bctch')
        if len(botcarcher) > 0:
            return HttpResponse('Bot caught!') #here we must implement captcha
        for sesskey in request.session.keys():
            del request.session[sesskey]
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('User not active')
        else:
            return HttpResponse('invalid login details')


@login_required
def user_logout(request):
    logout(request)
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return HttpResponseRedirect(reverse('index'))
