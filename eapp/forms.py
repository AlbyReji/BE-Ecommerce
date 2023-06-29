from django.forms import ModelForm
from django import forms 
from django.contrib.auth import authenticate, get_user_model
from django.forms import ValidationError
from .models import Category,Product

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    phone_number = forms.CharField(label='Phone number')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'password',
            'password2',
        ]
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email has already been registered")
        
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'