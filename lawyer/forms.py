from django import forms
from django.contrib.auth.models import User
from lawyer.models import Lawyer,State

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
    # username = forms.CharField(max_length=128)
    # email = forms.EmailField(max_length=128)
    # password = forms.CharField(widget = forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password','confirm_password')
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
                ),
                'confirm_password':forms.PasswordInput(
                    attrs={
                        'class': 'form-control'
                    }
                )
        }
      


class LawyerForm(forms.ModelForm):
    
    # password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = Lawyer
        fields = '__all__'
        exclude = ('user','confirm_password')
