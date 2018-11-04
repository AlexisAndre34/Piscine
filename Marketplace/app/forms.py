from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Formulaire pour la connexion au site
class SignInForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


#-----Formulaire de creation ---

#Formulaire de creation d'un compte client
class SignUpFormClient(UserCreationForm):
    datenaissanceclient = forms.DateField()
    telephoneclient = forms.CharField()
    codepostalclient = forms.IntegerField()
    villeclient = forms.CharField()
    rueclient = forms.CharField()
    class Meta:
        model = User
        fields = ('username','first_name','last_name','datenaissanceclient','email','telephoneclient','codepostalclient','villeclient','rueclient','password1', 'password2', )

#Formulaire de creation de compte commercant
class SignUpFormCommercant(UserCreationForm):
    telephonecommercant = forms.CharField()
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','telephonecommercant', 'password1', 'password2', )

#-----Formulaire de mise à jour ---