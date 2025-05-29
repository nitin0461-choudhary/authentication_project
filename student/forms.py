
from django import forms 
class Registration(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField()
class New_Profile_form(forms.Form):
    name=forms.CharField()    
    email=forms.EmailField()
    password=forms.CharField()
    resume_file=forms.FileField()
    image_file=forms.ImageField()
class forget_password_form(forms.Form):
    name=forms.CharField()    
    email=forms.EmailField()
