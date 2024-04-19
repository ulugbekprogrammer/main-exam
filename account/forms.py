from django import forms 
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password', min_length=8, max_length=32)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat Your Password', min_length=8, max_length=32)

    def clean_password2(self):
        cd = self.cleaned_data    
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password didn't match")
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email = data).exists():
            raise forms.ValidationError("Email already exists")
        return data 

class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email = data).exists():
            raise forms.ValidationError("Email already in use")
        return data  

