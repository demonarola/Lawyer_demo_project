from django import forms
from django.contrib.auth.models import User
from lawyer.models import Lawyer,State
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

class LoginForm(forms.ModelForm):
    # username = forms.CharField(max_length=128)
    # email = forms.EmailField(max_length=128)
    # password = forms.CharField(widget = forms.PasswordInput())
   
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
                'email':forms.EmailInput(
                    attrs={
                        'class': 'form-control'
                    }
                ),
                'password':forms.PasswordInput(
                    attrs={
                        'class': 'form-control'
                    }
                )
        }

        

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,validators=[
        RegexValidator(regex='^[A-Za-z]{2}[a-z]{1,30}',message='First Name should only contain letters and must atleast 2 characters')
    ])
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,validators=[
        RegexValidator(regex='^[A-Za-z]{2}[a-z]{1,30}',message='Last Name should only contain letters and  must atleast 2 characters')
    ])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=True)
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,validators=[
        RegexValidator(regex='.{6,10}',message='Password must be between 6 to 10 characters long')
    ])
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,validators=[
        RegexValidator(regex='.{6,10}',message='Confirm Password must be between 6 to 10 characters long')
    ])
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password','confirm_password')
        widgets = {
            'username': forms.TextInput(
				attrs={
					'class': 'form-control'
					},
                   
				),        
        }
      
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return email
    

class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = '__all__'
        exclude = ('user','confirm_password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return email