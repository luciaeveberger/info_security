import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from . import forms
from django.core import serializers
from secretsmodules.models import Secret, UserProfile
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
# Create your views here.


def duplicate_mail(email):
    users = list(User.objects.filter(email = email))
    if len(users) > 0:
        return True
    return False



# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):

        secrets = Secret.objects.all()
        my_dict = {'all_secrets':secrets}
        return render(request, 'secretmodules/index.html', context=my_dict)


def add_to_cart(request, secret_id):
    cart = request.session.get('cart', {})
    secret = Secret.objects.get(pk=secret_id)
    serialized_obj = serializers.serialize('json', [secret])
    cart[len(cart)] = serialized_obj
    request.session['cart'] = cart
    my_cart = request.session['cart']
    return render(request, 'secretmodules/cart.html', context=my_cart)


class RegisterForm(TemplateView):

    def get(self, request, **kwargs):
        form = forms.UserForm()
        return render(request, 'secretmodules/register.html', context={'form': form})
    def post(self, request, **kwargs):
        form = forms.UserForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            try:
                if(duplicate_mail(data['email'])):
                    form.add_error(field = 'email', error = "Email already in user")
                try:
                    validate_password(data['password'])
                except ValidationError as ve:
                    form.add_error(field = 'password', error = ve.messages)
                if len(form.errors) > 0:
                    return render(request, 'secretmodules/register.html', context={'form': form})
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
                return render(request, 'secretmodules/register.html', context={'form': form})
            except Exception as e:
                form.add_error(field = None, error = "Unspecified Integrity error, try again later" )
                return render(request, 'secretmodules/register.html', context={'form': form})
            profile = UserProfile(user = user, address = data['address'], phone = data['phone'])
            profile.save()
            return HttpResponse('success')
        else:
            return render(request, 'secretmodules/register.html', context={'form': form})
