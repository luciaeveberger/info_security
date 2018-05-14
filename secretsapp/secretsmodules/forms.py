from django import forms
from django.core import validators

class UserForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    email_repeat = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)
    password_repeat = forms.CharField(widget = forms.PasswordInput)
    address = forms.CharField(max_length = 264, required = False)
    phone = forms.CharField(max_length = 20, required = False)
    botcatcher = forms.CharField(required = False, widget = forms.HiddenInput)  #this is to catch bots: hidden field, so actual user won't fill it, bot will

    def clean(self):
        clean_data = super().clean()
        botcatcher = clean_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("Bot caught")
        if clean_data['email']!=clean_data['email_repeat']:
            raise forms.ValidationError("Emails don't match")
        if clean_data['password']!=clean_data['password_repeat']:
            raise forms.ValidationError("Passwords don't match")

    # def clean_botcatcher(self):  #custom validator
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("Bot caught")
    #     return botcatcher
